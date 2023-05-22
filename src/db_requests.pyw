from __builtin__ import str
from configparser import RawConfigParser
import pymysql.cursors
from pymysql.connections import Connection
from datetime import datetime
import time
import json
import logging
from logging.handlers import TimedRotatingFileHandler
import requests
import os

config = {}

SCRIPT_WORK_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))

logger = logging.getLogger('db_requests')

prolon_server_address = "http://127.0.0.1:5000"

prolon_server_routes = {
    4: {"read": "get_input_registers"}
    , 3: {
        "read": "get_holding_registers"
        , "write": "write_holding_register"
    },
    'email': {
        "read": "get_alarm_email"
        , "write": "write_alarm_email"
    }
    , "alarm": {
        "read": "get_alarm_setup"
        , "write": "write_alarm_setup"
    }
}


def get_config():
    """
    get required parameters from config file 'sync_config.ini' in the script directory
    Returns
    -------
    dict of parameters
    """
    config_file_path = os.path.join(SCRIPT_WORK_DIR, 'resources', 'sync_config.ini')
    with open(config_file_path) as config_file:
        config_parser = RawConfigParser()
        config_parser.read_file(config_file)
        return dict(config_parser['DATABASE'])


def init_logger(logging_level=logging.DEBUG):
    file_handler = TimedRotatingFileHandler(
        filename=os.path.join(SCRIPT_WORK_DIR, 'logs', 'db_requests', 'sync_runtime.log')
        , when='midnight', interval=1, backupCount=3,
        encoding='utf-8',
        delay=False)

    console_logger = logging.StreamHandler()
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_logger.setFormatter(console_formatter)
    logging.basicConfig(
        filename=os.path.join(SCRIPT_WORK_DIR, "logs", "db_requests", datetime.today().strftime('%Y-%m-%d') + ".log")
        , format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s'
        , datefmt='%Y-%m-%d %H:%M:%S'
    )

    logging.getLogger('db_requests').addHandler(file_handler)
    logging.getLogger('db_requests').addHandler(console_logger)
    logging.getLogger('db_requests').setLevel(logging_level)


def get_read_http_requests_from_database(mysql_connection):
    """
    get read controller data requests from database
    Parameters
    ----------
    mysql_connection

    Returns
    -------
    list of dicts with request parameters
    """
    requests = []
    try:
        assert isinstance(mysql_connection, Connection)
        with mysql_connection.cursor() as cursor:
            sql = "SELECT " \
                  " controller_id" \
                  ",register_type" \
                  ",MIN(register_number) AS min_register" \
                  ", MAX(register_number) AS max_register" \
                  ",(MAX(register_number)-MIN(register_number)+1)AS count" \
                  ", exec_status " \
                  "FROM {} " \
                  "WHERE " \
                  "exec_status = 'read' " \
                  "GROUP BY controller_id,register_type".format(config['requests_table'])
            cursor.execute(sql)
            records = cursor.fetchall()

            for record in records:
                register_type = record["register_type"]
                if register_type in prolon_server_routes.keys():
                    request = {"route": prolon_server_routes[register_type]["read"],
                               "register_type": register_type,
                               "params": {"id": record["controller_id"], "start": record['min_register'],
                                          "count": record["count"]}}

                    requests.append(request)
                    logger.debug("Read request received:" + str(request))

    except BaseException as ex:
        logger.error("Error at get read requests info {}".format(ex))
    finally:
        return requests


def read_data_from_server_and_update_db(mysql_connection, requests_to_controllers):
    """
    executes all read controller data requests and update remote database
    Parameters
    ----------
    mysql_connection - mysql connection instance
    requests_to_controllers - list of requests to controllers

    Returns
    -------
    None
    """
    assert isinstance(mysql_connection, Connection)
    if len(read_requests_to_controller) == 0:
        return

    db_update_sql = "INSERT INTO {} (controller_id,register_type,register_number,value,update_time,exec_status)" \
                    " VALUES (%s,%s,%s,%s,%s,%s) " \
                    "ON DUPLICATE KEY UPDATE value=VALUES(value), update_time = VALUES(update_time)," \
                    " exec_status=VALUES(exec_status)".format(config['requests_table'])

    db_update_error_sql = "INSERT INTO {} (controller_id,register_type,register_number,value,update_time,exec_status)" \
                          " VALUES (%s,%s,%s,%s,%s,%s)" \
                          " ON DUPLICATE KEY UPDATE  exec_status=VALUES(exec_status)".format(config['requests_table'])

    with mysql_connection.cursor() as cursor:

        for request in requests_to_controllers:
            try:
                logger.debug("Execute request {}".format(request))
                parameters = request["params"]
                controller_id = parameters["id"]
                register_type = request["register_type"]
                response_text = requests.request("GET", "{}/{}".format(prolon_server_address, request["route"])
                                                 , params=parameters).text

                logger.debug("Data received:{}".format(response_text))
                response_json = json.loads(response_text)
                if "error" in response_json.keys():

                    logger.error("Error resp received:{}".format(response_json["error"]))

                    for register_number in range(int(parameters["start"]),
                                                 int(parameters["start"] + parameters["count"])):
                        cursor.execute(db_update_error_sql,
                                       (controller_id, register_type, register_number, '0', datetime.now(),
                                        'read_error'))
                        mysql_connection.commit()

                else:
                    for register_number in range(int(parameters["start"]),
                                                 int(parameters["start"] + parameters["count"])):
                        if str(register_number) in response_json.keys():
                            readed_data = response_json[str(register_number)]
                            value = readed_data["value"]
                            update_time = datetime.fromtimestamp(int(readed_data["timestamp"]))

                            cursor.execute(db_update_sql,
                                           (str(controller_id), str(register_type), str(register_number), str(value),
                                            str(update_time),
                                            'read_ok'))
                        else:
                            cursor.execute(db_update_error_sql,
                                           (str(controller_id), str(register_type), str(register_number), '0',
                                            str(datetime.now()),
                                            'read_empty'))

                        mysql_connection.commit()
            except BaseException as ex:
                logger.error("Read registers Request processing error:{}".format(ex))


def get_write_http_requests_from_database(mysql_connection):
    """
    get write controller data requests from database
    Parameters
    ----------
    mysql_connection

    Returns
    -------
    list of dicts with request parameters
    """
    requests = {}
    try:
        assert isinstance(mysql_connection, Connection)

        sql = "SELECT " \
              " controller_id" \
              ",register_type" \
              ",register_number" \
              ",value" \
              ", exec_status " \
              "FROM {} " \
              "WHERE " \
              "exec_status = 'write' " \
              "GROUP BY controller_id,register_type".format(config['requests_table'])
        with mysql_connection.cursor() as cursor:
            cursor.execute(sql)
        records = cursor.fetchall()

        requests = []

        for record in records:
            register_type = record["register_type"]
            if register_type in prolon_server_routes.keys():
                request = {"route": prolon_server_routes[register_type]["write"],
                           "register_type": register_type,
                           "params": {"id": record["controller_id"], "start": record['register_number'],
                                      "value": record["value"]}}

                requests.append(request)
                logger.debug("Write request received:" + str(request))

    except BaseException as ex:
        logger.error("Error at get write requests info {}".format(ex))
    finally:
        return requests


def write_data_to_server_and_update_db(mysql_connection, requests_to_controllers):
    """
        executes all write controller data requests and update remote database
        Parameters
        ----------
        mysql_connection - mysql connection instance
        requests_to_controllers - list of requests to controllers

        Returns
        -------
        None
    """

    assert isinstance(mysql_connection, Connection)
    if len(requests_to_controllers) == 0:
        return

    db_update_sql = "INSERT INTO {} (controller_id,register_type,register_number,value,update_time,exec_status)" \
                    " VALUES (%s,%s,%s,%s,%s,%s)" \
                    " ON DUPLICATE KEY UPDATE value=VALUES(value), update_time = VALUES(update_time)," \
                    " exec_status=VALUES(exec_status)".format(config['requests_table'])

    db_update_error_sql = "INSERT INTO {} (controller_id,register_type,register_number,value,update_time,exec_status)" \
                          " VALUES (%s,%s,%s,%s,%s,%s) " \
                          "ON DUPLICATE KEY UPDATE  exec_status=VALUES(exec_status)".format(config['requests_table'])

    with mysql_connection.cursor() as cursor:
        for request in requests_to_controllers:
            try:
                logger.debug("Execute write request {}".format(request))
                parameters = request["params"]
                controller_id = str(parameters["id"])
                register_type = str(request["register_type"])
                register_number = str(parameters["start"])
                response_text = requests.request("GET", "{}/{}".format(prolon_server_address, request["route"])
                                                 , params=parameters).text

                logger.debug("Data received:{}".format(response_text))
                response_json = json.loads(response_text)
                if "error" in response_json.keys():

                    logger.error("Error resp received:{}".format(response_json["error"]))

                    cursor.execute(db_update_error_sql,
                                   (controller_id, register_type, register_number, '0', datetime.now(), 'read_error'))

                    mysql_connection.commit()

                else:

                    if str(register_number) in response_json.keys():
                        readed_data = response_json[str(register_number)]
                        value = readed_data["value"]
                        update_time = datetime.fromtimestamp(int(readed_data["timestamp"]))

                        cursor.execute(db_update_sql,
                                       (controller_id, register_type, register_number, value, update_time, 'write_ok'))
                    else:
                        cursor.execute(db_update_error_sql,
                                       (
                                           controller_id, register_type, register_number, 0, datetime.now(),
                                           'write_empty'))

                    mysql_connection.commit()
            except BaseException as ex:
                logger.error("Write register Request processing error:{}".format(ex))


def read_write_email_requests_from_database(mysql_connection):
    """
    get all write notification email requests from database
    Parameters
    ----------
    mysql_connection

    Returns
    -------
    list of requests parameters
    """
    requests = []
    try:
        assert isinstance(mysql_connection, Connection)
        with mysql_connection.cursor() as cursor:
            sql = "SELECT " \
                  " controller_id" \
                  ",register_number" \
                  ",exec_status " \
                  ", string_value " \
                  "FROM {} " \
                  "WHERE " \
                  "exec_status = 'write_alarm_email' ".format(config['requests_table'])
            cursor.execute(sql)
            records = cursor.fetchall()

            for record in records:
                email_number = record["register_number"]
                new_email = record["string_value"]
                if new_email == "remove":
                    new_email = ""
                request = {"route": prolon_server_routes["email"]["write"],
                           "params": {"id": record["controller_id"],
                                      "number": email_number, "email": new_email},
                           }

                requests.append(request)
                logger.debug("Write alarm email request received:" + str(request))
    except BaseException as ex:
        logger.error("Error at get write alarm requests info {}".format(ex))
    finally:
        return requests


def write_email_data_to_server_and_update_db(mysql_connection, requests_to_controllers):
    """
    executes all write notification email requests
    Parameters
    ----------
    mysql_connection
        mysql connection instance
    requests_to_controllers
        list of requests

    Returns
    -------
    None
    """
    assert isinstance(mysql_connection, Connection)
    if len(requests_to_controllers) == 0:
        return

    db_update_sql = "INSERT INTO {} (controller_id,register_type,register_number,string_value,update_time,exec_status)" \
                    " VALUES (%s,%s,%s,%s,%s,%s) " \
                    "ON DUPLICATE KEY UPDATE string_value=VALUES(string_value), " \
                    "update_time = VALUES(update_time)," \
                    " exec_status=VALUES(exec_status)".format(config['requests_table'])

    db_update_error_sql = "INSERT INTO {} " \
                          "(controller_id,register_type,register_number,string_value,update_time,exec_status)" \
                          " VALUES (%s,%s,%s,%s,%s,%s) " \
                          "ON DUPLICATE KEY UPDATE  exec_status=VALUES(exec_status)".format(config['requests_table'])

    with mysql_connection.cursor() as cursor:

        for request in requests_to_controllers:
            try:
                logger.debug("Execute write request {}".format(request))
                parameters = request["params"]
                controller_id = str(parameters["id"])
                register_number = str(parameters["number"])
                response_text = requests.request("GET", "{}/{}".format(prolon_server_address, request["route"])
                                                 , params=parameters).text

                logger.debug("Data received:{}".format(response_text))
                response_json = json.loads(response_text)
                if "error" in response_json.keys():
                    logger.error("Error resp received:{}".format(response_json["error"]))
                    cursor.execute(db_update_error_sql,
                                   (controller_id, '30', register_number, '0', datetime.now(),
                                    'write_alarm_email_error'))
                    mysql_connection.commit()
                else:
                    value = response_json["email"]
                    update_time = datetime.fromtimestamp(int(response_json["timestamp"]))
                    cursor.execute(db_update_sql,
                                   (controller_id, 30, register_number, value, update_time, 'write_alarm_email_ok'))

                mysql_connection.commit()
            except BaseException as ex:
                logger.error("Write email Request processing error:{}".format(ex))


def read_email_requests_from_database(mysql_connection):
    """
    get all read nptification email requests from database
    Parameters
    ----------
    mysql_connection
        mysql connection instance

    Returns
    -------
    List of dicts with requests parameters

    """
    requests = []
    try:
        assert isinstance(mysql_connection, Connection)
        with mysql_connection.cursor() as cursor:
            sql = "SELECT " \
                  " controller_id" \
                  ",register_number" \
                  ",exec_status " \
                  "FROM {} " \
                  "WHERE " \
                  "exec_status = 'read_alarm_email' ".format(config['requests_table'])
            cursor.execute(sql)
            records = cursor.fetchall()

            for record in records:
                email_number = record["register_number"]
                request = {"route": prolon_server_routes["email"]["read"],
                           "params": {"id": record["controller_id"],
                                      "number": email_number}}

                requests.append(request)
                logger.debug("Read alarm email request received:" + str(request))

    except BaseException as ex:
        logger.error("Error at get read requests info {}".format(ex))
    finally:
        return requests


def read_alarm_emails_from_server_and_update_db(mysql_connection, requests_to_controllers):
    """
    execute all read notification emails requests and update database
    Parameters
    ----------
    mysql_connection
        mysql connection instance
    requests_to_controllers
        list of controllers requests

    Returns
    -------
        None

    """
    assert isinstance(mysql_connection, Connection)
    if len(requests_to_controllers) == 0:
        return

    db_update_sql = "INSERT INTO {}" \
                    " (controller_id,register_type,register_number,string_value,update_time,exec_status)" \
                    " VALUES (%s,%s,%s,%s,%s,%s) " \
                    "ON DUPLICATE KEY UPDATE string_value=VALUES(string_value)," \
                    " update_time = VALUES(update_time)," \
                    " exec_status=VALUES(exec_status)".format(config['requests_table'])

    db_update_error_sql = "INSERT INTO {} " \
                          "(controller_id,register_type,register_number,string_value,update_time,exec_status)" \
                          " VALUES (%s,%s,%s,%s,%s,%s) " \
                          "ON DUPLICATE KEY UPDATE  exec_status=VALUES(exec_status)".format(config['requests_table'])

    with mysql_connection.cursor() as cursor:
        for request in requests_to_controllers:
            try:
                logger.debug("Execute request {}".format(request))
                parameters = request["params"]
                controller_id = str(parameters["id"])
                number = str(parameters["number"])
                response_text = requests.request("GET", "{}/{}".format(prolon_server_address, request["route"])
                                                 , params=parameters).text

                logger.debug("Data received:{}".format(response_text))
                response_json = json.loads(response_text)
                if "error" in response_json.keys():
                    cursor.execute(db_update_error_sql,
                                   (controller_id, '30', number, '0', datetime.now(), 'read_alarm_email__error'))
                    mysql_connection.commit()

                else:
                    readed = response_json["email"]
                    update_time = datetime.fromtimestamp(int(response_json["timestamp"]))
                    email = response_json["email"]
                    cursor.execute(db_update_sql,
                                   (controller_id, '30', number, email, update_time, 'read_alarm_email_ok'))
                mysql_connection.commit()
            except BaseException as ex:
                logger.error("Read alarm email Request processing error:{}".format(ex))


def get_read_alarms_setup_requests_from_database(mysql_connection):
    """
    get read alarms requests from database
    Parameters
    ----------
    mysql_connection
        mysql connection instance

    Returns
    -------
    list of requests paramsters
    """
    requests = []
    try:
        assert isinstance(mysql_connection, Connection)
        with mysql_connection.cursor() as cursor:
            sql = "SELECT " \
                  " controller_id" \
                  ",register_number" \
                  ",exec_status " \
                  "FROM {} " \
                  "WHERE " \
                  "exec_status = 'read_alarm_setup' " \
                  " AND register_type = 31".format(config['requests_table'])
            cursor.execute(sql)
            records = cursor.fetchall()

            for record in records:

                request = {"route": prolon_server_routes["alarm"]["read"],
                           "params": {"id": record["controller_id"]
                                      }}
                if record["register_number"] != 0:
                    request["params"]["start"] = record["register_number"]
                    request["params"]["count"] = 1

                requests.append(request)
                logger.debug("Read alarm setup request received:" + str(request))

    except BaseException as ex:
        logger.error("Error at get read alarms setup info {}".format(ex))
    finally:
        return requests


def read_alarms_setup_from_server_and_update_db(mysql_connection, requests_to_controllers):
    """
    executes all requests to controllers and update database from response data
    Parameters
    ----------
    mysql_connection
        mysql connection instance
    requests_to_controllers
        list of requests

    Returns
    -------
    None

    """
    assert isinstance(mysql_connection, Connection)
    if len(requests_to_controllers) == 0:
        return

    db_update_sql = "INSERT INTO {}" \
                    " (controller_id,register_type,register_number,text_value,update_time,exec_status)" \
                    " VALUES (%s,%s,%s,%s,%s,%s) " \
                    "ON DUPLICATE KEY UPDATE text_value=VALUES(text_value)," \
                    " update_time = VALUES(update_time)," \
                    " exec_status=VALUES(exec_status)".format(config['requests_table'])

    db_update_error_sql = "INSERT INTO {}" \
                          " (controller_id,register_type,register_number,text_value,update_time,exec_status)" \
                          " VALUES (%s,%s,%s,%s,%s,%s) " \
                          "ON DUPLICATE KEY UPDATE  exec_status=VALUES(exec_status)".format(config['requests_table'])

    with mysql_connection.cursor() as cursor:

        for request in requests_to_controllers:
            try:
                logger.debug("Execute request {}".format(request))
                parameters = request["params"]
                controller_id = parameters["id"]
                register_number = parameters.get("start", 0)

                url = "{}/{}".format(prolon_server_address, request["route"])

                response_text = requests.request("GET", url
                                                 , params=parameters).text

                logger.debug("Data received:{}".format(response_text.encode("utf8", 'ignore')))
                response_json = json.loads(response_text)
                if "error" in response_json.keys():
                    cursor.execute(db_update_error_sql,
                                   (controller_id, 31, register_number, 0, datetime.now(), 'read_alarm_setup_error'))

                else:

                    readed_data = json.dumps(response_json["setup"])
                    logger.debug(readed_data)
                    update_time = datetime.fromtimestamp(int(response_json["timestamp"]))
                    cursor.execute(db_update_sql,
                                   (
                                       controller_id, 31, register_number, readed_data, update_time,
                                       'read_alarm_setup_ok'))

                    if register_number == 0:
                        for alert_controller_id, controller_alerts in response_json["setup"].items():
                            for alert_number, alert_setup in controller_alerts.items():
                                json_for_write_to_db = {alert_controller_id: {alert_number: alert_setup}}

                                logger.debug(
                                    "Update alert setup for controller {} alert number ={}".format(controller_id,
                                                                                                   alert_number))
                                cursor.execute(db_update_sql, (
                                    controller_id, 31, alert_number, json.dumps(json_for_write_to_db), update_time,
                                    'read_alarm_setup_ok'))

                mysql_connection.commit()
            except BaseException as ex:
                logger.error("Read alarm setup Request processing error:{}".format(ex))


def get_write_alarms_setup_requests_from_database(mysql_connection):
    """
    get all write alarm setup requests from database
    Parameters
    ----------
    mysql_connection
        mysql connection instance

    Returns
    -------
        list of requests parameters
    """
    requests = []
    try:
        assert isinstance(mysql_connection, Connection)
        with mysql_connection.cursor() as cursor:
            sql = "SELECT " \
                  " controller_id" \
                  ",register_number" \
                  ",exec_status " \
                  ",text_value" \
                  " FROM {} " \
                  " WHERE " \
                  " exec_status = 'write_alarm_setup' " \
                  " AND register_type = 31".format(config['requests_table'])
            cursor.execute(sql)
            records = cursor.fetchall()

            for record in records:
                request_json = json.loads(record["text_value"])
                logger.debug(request_json)

                alarm_number = str(record["register_number"])
                setup = json.dumps(request_json.values()[0][alarm_number])
                request = {"route": prolon_server_routes["alarm"]["write"],
                           "params": {"id": record["controller_id"],
                                      "number": record["register_number"]},
                           "setup": setup}
                requests.append(request)
                logger.debug("Write alarm setup request received:" + str(request))

    except BaseException as ex:
        logger.error("Error at get write alarms setup req info {}".format(ex))
    finally:
        return requests


def write_alarms_setup_to_sever_and_update_db(mysql_connection, requests_to_controllers):
    """
    executes all write alarms setup requests and update database from responses
    Parameters
    ----------
    mysql_connection
        mysql connection instance
    requests_to_controllers
        list of requests

    Returns
    -------
        None
    """
    assert isinstance(mysql_connection, Connection)
    if len(requests_to_controllers) == 0:
        return

    db_update_sql = "INSERT INTO {}" \
                    " (controller_id,register_type,register_number,string_value,update_time,exec_status)" \
                    " VALUES (%s,%s,%s,%s,%s,%s) " \
                    "ON DUPLICATE KEY UPDATE string_value=VALUES(string_value)," \
                    " update_time = VALUES(update_time)," \
                    " exec_status=VALUES(exec_status)".format(config['requests_table'])

    db_update_error_sql = "INSERT INTO {}" \
                          " (controller_id,register_type,register_number,string_value,update_time,exec_status)" \
                          " VALUES (%s,%s,%s,%s,%s,%s) " \
                          "ON DUPLICATE KEY UPDATE  exec_status=VALUES(exec_status)".format(config['requests_table'])

    with mysql_connection.cursor()as cursor:
        for request in requests_to_controllers:
            try:
                logger.debug("Execute write alarm setup request {}".format(request))
                parameters = request["params"]
                controller_id = str(parameters["id"])
                register_number = str(parameters["number"])
                setup = str(request["setup"])
                response_text = requests.request("POST", "{}/{}".format(prolon_server_address, request["route"])
                                                 , params=parameters, json=setup).text

                logger.debug("Data received:{}".format(response_text))
                response_json = json.loads(response_text)
                if "error" in response_json.keys():

                    logger.error("Error resp received:{}".format(response_json["error"]))

                    cursor.execute(db_update_error_sql,
                                   (controller_id, '31', register_number, '0', datetime.now(),
                                    'write_alarm_setup_error'))

                    mysql_connection.commit()

                else:

                    update_time = datetime.fromtimestamp(int(response_json["timestamp"]))
                    cursor.execute(db_update_sql,
                                   (controller_id, 31, register_number, json.dumps(response_json), update_time,
                                    'write_alarm_setup_ok'))

                mysql_connection.commit()
            except BaseException as ex:
                logger.error("Write alarm setup Request processing error:{}".format(ex))
            finally:
                cursor.close()


if __name__ == '__main__':
    init_logger()
    config = get_config()
    conn = pymysql.connect(host=config['db_host']
                           , database=config['db_name']
                           , user=config['user']
                           , password=config['password']
                           , cursorclass=pymysql.cursors.DictCursor)

    while True:

        try:
            conn.ping(reconnect=True)
            logger.debug("Connect ok")

            # read_registers
            read_requests_to_controller = get_read_http_requests_from_database(conn)
            read_data_from_server_and_update_db(conn, read_requests_to_controller)

            # write registers
            write_requests_to_controller = get_write_http_requests_from_database(conn)
            write_data_to_server_and_update_db(conn, write_requests_to_controller)
            #
            read_alarm_emails_requests = read_email_requests_from_database(conn)
            read_alarm_emails_from_server_and_update_db(conn, read_alarm_emails_requests)

            write_alarm_emails_requests = read_write_email_requests_from_database(conn)
            write_email_data_to_server_and_update_db(conn, write_alarm_emails_requests)

            read_alarms_setup_requests = get_read_alarms_setup_requests_from_database(conn)
            read_alarms_setup_from_server_and_update_db(conn, read_alarms_setup_requests)

            write_alarms_setup_requests = get_write_alarms_setup_requests_from_database(conn)
            write_alarms_setup_to_sever_and_update_db(conn, write_alarms_setup_requests)
        except BaseException as ex:
            logger.error("Read requests table error:{}".format(ex))
        else:
            logger.debug("conn={}".format(conn))
            if conn:
                logger.debug("connected={}".format(conn.open))
        finally:
            if conn:
                conn.close()
            time.sleep(3)
