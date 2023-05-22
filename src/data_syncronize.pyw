import mysql.connector
from mysql.connector import MySQLConnection
from controllers import get_data_stored_after, remove_old_records
from datetime import datetime, timedelta
import time
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from configparser import RawConfigParser

SCRIPT_WORK_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))

logger = logging.getLogger("sync")


def is_time_for_removing_old_data(sync_interval_in_seconds):
    time_now = datetime.now()
    return (
            time_now.hour == 8
            and time_now.minute * 60 + time_now.second <= sync_interval_in_seconds
    )


def init_logger(logging_level=logging.DEBUG):
    log_dir = os.path.join(SCRIPT_WORK_DIR, "logs", "sync")
    file_handler = TimedRotatingFileHandler(
        filename=os.path.join(log_dir, "sync_runtime.log"),
        when="midnight",
        interval=1,
        backupCount=3,
        encoding="utf-8",
        delay=False,
    )

    console_logger = logging.StreamHandler()
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_logger.setFormatter(console_formatter)
    logging.basicConfig(
        filename=os.path.join(log_dir, datetime.today().strftime("%Y-%m-%d") + ".log"),
        format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging.getLogger("sync").addHandler(file_handler)
    logging.getLogger("sync").addHandler(console_logger)
    logging.getLogger("sync").setLevel(logging_level)


def get_controllers_last_update(mysql_connection, config):
    """
    return registered controllers update information
    Parameters
    ----------
    mysql_connection
        mysql connection instance
    config
        remote database configuration information

    Returns
    -------
    dict of controllers data update time
    """
    update_info = {}
    try:
        assert isinstance(mysql_connection, MySQLConnection)
        cursor = mysql_connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM {}".format(config["update_info_table"]))
        records = cursor.fetchall()

        for record in records:
            if record["last_update"] is not None:
                update_info[record["controller_id"]] = record["last_update"]
            else:
                update_info[record["controller_id"]] = datetime.now() - timedelta(
                    minutes=5
                )

    except BaseException as ex:
        logger.error("Error at get updates info {}".format(ex))
    finally:
        cursor.close()

    return update_info


def store_controller_data_in_remote_base(conn, controllers_data, config):
    """
    updates controllers data in remote database and updates last_updates_info table
    Parameters
    ----------
    conn - mysql connection
    controllers_data - list of local database measurements
    config - remote database connection config

    Returns
    -------

    """
    assert isinstance(conn, MySQLConnection)
    cursor = conn.cursor()
    values_update_sql = "INSERT INTO {}" \
                        " (register_type,controller_id,timestamp,value,register_number) VALUES (%s,%s,%s,%s,%s) " \
                        " ON DUPLICATE KEY UPDATE value=VALUES(value)".format(config["realtime_values_table"])

    info_update_sql = "UPDATE {}" \
                      " SET last_update=%s WHERE controller_id=%s".format(config["update_info_table"])

    last_values_update_sql = "INSERT INTO {}" \
                             " (register_type,controller_id,timestamp,value,register_number) VALUES (%s,%s,%s,%s,%s) " \
                             "ON DUPLICATE KEY UPDATE value = values(value)".format(config["last_values_table"])

    execute_tuples = []

    last_controllers_data = {}
    for controller_id, controller_value_records in controllers_data.items():
        if len(controller_value_records) == 0:
            logger.debug("Nothing found for controller {}".format(controller_id))
            continue

        try:
            last_time_stamp = 0
            length = len(controller_value_records)
            start_time = datetime.now()
            logger.debug(
                "Start inserting {} records for controller {}".format(
                    length, controller_id
                )
            )

            for value_record in controller_value_records:
                if last_time_stamp == 0:
                    last_time_stamp = value_record["timestamp"]
                else:
                    if last_time_stamp < value_record["timestamp"]:
                        last_time_stamp = value_record["timestamp"]

                execute_tuples.append(
                    (
                        value_record["register_type"],
                        controller_id,
                        value_record["timestamp"],
                        value_record["value"],
                        value_record["register_number"],
                    )
                )

            cursor.executemany(values_update_sql, execute_tuples)
            cursor.executemany(last_values_update_sql, execute_tuples)
            cursor.execute(info_update_sql, (last_time_stamp, controller_id))
            logger.debug(
                "Insert ended. Total time:{}".format(
                    (datetime.now() - start_time).total_seconds()
                )
            )
        except BaseException as ex:
            logger.error(
                "Insert data for controller {} failed {}".format(controller_id, ex)
            )
            conn.rollback()
    conn.commit()
    cursor.close


def get_config():
    config_file_path = os.path.join(SCRIPT_WORK_DIR, "resources", "sync_config.ini")
    with open(config_file_path) as config_file:
        config_parser = RawConfigParser()
        config_parser.read_file(config_file)
        return dict(config_parser["DATABASE"])


if __name__ == "__main__":
    init_logger()
    config = get_config()

    while True:
        try:
            logger.debug("Start sync data")
            conn = mysql.connector.connect(
                host=config["db_host"],
                database=config["db_name"],
                user=config["user"],
                password=config["password"],
                use_pure=True,
            )
            update_info = get_controllers_last_update(conn, config)
            values = get_data_stored_after(update_info, config=config, logger=logger)
            store_controller_data_in_remote_base(conn, values, config)
        except BaseException as ex:
            logger.error("Store data error: {}".format(ex))
        finally:
            if conn and conn.is_connected():
                conn.close()
        try:
            if is_time_for_removing_old_data(int(config["sync_interval_in_seconds"])):
                remove_old_records(60 * 60 * 24 * 10, logger)
        except BaseException as ex:
            logger.error("Removing old records error: {}", ex)

        time.sleep(int(config["sync_interval_in_seconds"]))
