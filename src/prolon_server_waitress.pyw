import threading
from configparser import RawConfigParser
from flask import Flask, request, jsonify, url_for, redirect, render_template, Response
from multiprocessing import Queue
from pymodbus.client.sync import (
    ModbusSerialClient as ModbusClient,
)  # initialize a serial RTU client instance
import time
import logging
from datetime import datetime, timedelta
from logging.handlers import TimedRotatingFileHandler
from concurrent.futures import ThreadPoolExecutor
from prolon_modbus_registers import (
    ModbusRequest,
    ReadAlarmEmailRequest,
    WriteAlarmEmailRequest,
    ReadAllAlarmSetup,
    WriteAlarmSetupRequest,
)
import json
import os
from waitress import serve
from controllers import (
    get_controllers_in_system,
    store_controllers_memory,
    create_data_forwarding_request,
)

SCRIPT_WORK_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["JSON_AS_ASCII"] = False

controllers = get_controllers_in_system()
web_requests = Queue()

requests_executor = ThreadPoolExecutor(max_workers=1)


# pushing_executor = ThreadPoolExecutor(max_workers=1)


class CyclicTasksPusher(threading.Thread):
    def __init__(self):
        self.is_running = True
        super(CyclicTasksPusher, self).__init__()

    def stop(self):
        self.is_running = False

    def run(self):
        server_logger.info("Requests pushing started")
        while self.is_running:
            try:
                execute_controllers_requesting()
            except BaseException as ex:
                server_logger.error("Execute requesting error {}".format(ex))
            finally:
                time.sleep(60)
        server_logger.info("Requests pushing ended")


requesting_tasks_pusher = CyclicTasksPusher()

server_logger = logging.getLogger("boilers")


def get_com_port_setup():
    config_file_path = os.path.join(SCRIPT_WORK_DIR, "resources", "sync_config.ini")
    with open(config_file_path) as config_file:
        config_parser = RawConfigParser()
        config_parser.read_file(config_file)
        return dict(config_parser["COM PORT"])


def init_logger(logging_level=logging.DEBUG):
    logs_location = os.path.join(SCRIPT_WORK_DIR, "logs", "server")
    file_handler = TimedRotatingFileHandler(
        filename=os.path.join(logs_location, "s_runtime.log"),
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
        filename=os.path.join(
            logs_location, datetime.today().strftime("%Y-%m-%d") + ".log"
        ),
        format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging.getLogger("boilers").addHandler(file_handler)
    logging.getLogger("boilers").addHandler(console_logger)
    logging.getLogger("boilers").setLevel(logging_level)


def execute_data_forwarding():
    try:

        request = create_data_forwarding_request(
            controllers[3], "INPUT", 0, controllers[4], "HOLDING", 141
        )
        # srequest.execute(client)
    except BaseException as ex:
        server_logger.error(
            "Data forwarding error from {}:{}:{} to {}:{}:{}".format(
                controllers[3].name, "INPUT", 0, controllers[4].name, "HOLDING", 141
            )
        )


def execute_controllers_requesting():
    start_time = datetime.now()
    # print("Start:" + str(datetime.now()))
    for controller in controllers.values():
        for request in controller.operative_memory_requests:
            try:
                request_result = requests_executor.submit(
                    request.execute, client=client
                )
                result_registers = request_result.result()
                controller.update_memory_from_responce(
                    result_registers, request.start, request.fc
                )
                controller.last_update_status = "OK"
                # print(controller.name + ":OK")
            except BaseException as ex:
                server_logger.error(controller.name + " request exception " + str(ex))
                controller.last_update_status = str(ex)

    try:
        store_controllers_memory(controllers.values())
    except BaseException as ex:
        server_logger.error("Store db error: " + str(ex))

    server_logger.debug(
        " Requesting time:" + str((datetime.now() - start_time).total_seconds())
    )


@app.route("/")
def main_page():
    controllers_info = {
        internal_id: {
            "name": controller.name,
            "uid": controller.uid,
            "last_update": controller.last_update.strftime("%m/%d/%Y %H:%M:%S"),
            "last_update_status": controller.last_update_status,
        }
        for (internal_id, controller) in controllers.items()
    }
    return render_template(
        "index.html",
        controllers=controllers_info,
        com_is_open=client.is_socket_open(),
        poll_is_started=requesting_tasks_pusher.is_running,
    )


@app.route("/get_server_status")
def get_server_status():
    controllers_info = {
        internal_id: {"name": controller.name}
        for (internal_id, controller) in controllers.items()
    }
    result = {"controllers_info": controllers_info}
    result["com_status"] = client.is_socket_open()
    result["poll_status"] = requesting_tasks_pusher.is_running
    return jsonify(result)


@app.route("/get_input_registers")
def get_input_registers():
    start = int(request.args.get("start"))
    count = int(request.args.get("count"))
    controller_id = int(request.args.get("id"))
    uid = controllers[int(controller_id)].uid
    request_to_controller = ModbusRequest(4, start, count, uid)

    try:
        result_future = requests_executor.submit(
            request_to_controller.execute, client=client
        )
        responce = result_future.result()
        responce_values = controllers[
            int(controller_id)
        ].decode_modbus_responce_to_json(request_to_controller, responce)
        return jsonify(responce_values)
    except BaseException as ex:
        return jsonify({"error": str(ex)})


@app.route("/stop_requesting")
def stop_requesting():
    global client, requesting_tasks_pusher

    server_logger.info("Stop polling")
    requesting_tasks_pusher.stop()

    server_logger.info("Stop serial client")
    client.close()

    server_logger.info("Requesting stop performed!")

    return redirect(url_for("get_server_status"))


@app.route("/start_requesting")
def start_requesting():
    global client, requesting_tasks_pusher, connection
    if not connection:
        server_logger.info("Connect serial client")
        connection = client.connect()

    if not requesting_tasks_pusher.is_running:
        server_logger.info("Start polling")
        requesting_tasks_pusher = CyclicTasksPusher()
        requesting_tasks_pusher.start()
    server_logger.info("Requesting start performed!")
    return redirect(url_for("get_server_status"))


@app.route("/get_raw_holding_registers")
def get_raw_holding_registers():
    start = int(request.args.get("start"))
    count = int(request.args.get("count"))
    controller_id = int(request.args.get("id"))
    uid = controllers[controller_id].uid
    request_to_controller = ModbusRequest(3, start, count, uid)
    try:
        result_future = requests_executor.submit(
            request_to_controller.execute, client=client
        )
        responce = result_future.result()
        responce_map = {}
        reg_start = 0
        for register in responce:
            responce_map[start + reg_start] = register
            reg_start += 1
        return jsonify(responce_map)
    except BaseException as ex:
        return jsonify({"error": str(ex)})


@app.route("/get_holding_registers")
def get_holding_registers():
    start = int(request.args.get("start"))
    count = int(request.args.get("count"))
    controller_id = int(request.args.get("id"))
    uid = controllers[controller_id].uid
    request_to_controller = ModbusRequest(3, start, count, uid)
    try:
        result_future = requests_executor.submit(
            request_to_controller.execute, client=client
        )
        responce = result_future.result()
        responce_values = controllers[controller_id].decode_modbus_responce_to_json(
            request_to_controller, responce
        )
        return jsonify(responce_values)
    except BaseException as ex:
        return jsonify({"error": str(ex)})


@app.route("/write_holding_register")
def write_holding_register():
    start = int(request.args.get("start"))
    value = float(request.args.get("value"))
    controller_id = int(request.args.get("id"))
    uid = controllers[controller_id].uid

    try:
        prolon_var = (
            controllers[controller_id]
            .modbus_map["HOLDING"][start]
            .get_register_from_value(value)
        )
        request_to_controller = ModbusRequest(
            6, uid=uid, start=start, value=prolon_var.value
        )
        result_future = requests_executor.submit(
            request_to_controller.execute, client=client
        )
        response = result_future.result()
        return redirect(
            url_for("get_holding_registers", id=controller_id, start=start, count=1)
        )
    except BaseException as ex:
        server_logger.error(
            "Write holding register error id={} start={} value={} : {}".format(
                controller_id, start, value, ex
            )
        )
        return jsonify({"error": str(ex)})


@app.route("/write_alarm_email")
def write_alarm_email():
    controller_id = int(request.args.get("id"))
    email_number = int(request.args.get("number"))
    email = str(request.args.get("email"))
    try:
        uid = controllers[controller_id].uid
        modbus_request = WriteAlarmEmailRequest(uid, email_number, email)
        result_future = requests_executor.submit(modbus_request.execute, client=client)
        response = result_future.result()
        return redirect(
            url_for("get_alarm_email", id=controller_id, number=email_number)
        )
    except BaseException as ex:
        return jsonify({"error": str(ex)})


@app.route("/get_alarm_email")
def get_alarm_email():
    controller_id = int(request.args.get("id"))
    email_number = int(request.args.get("number"))
    try:
        uid = controllers[controller_id].uid
        modbus_request = ReadAlarmEmailRequest(uid, email_number)
        result_future = requests_executor.submit(modbus_request.execute, client=client)

        result_dict = {
            "email": str(result_future.result()),
            "email_number": email_number,
            "timestamp": time.mktime(datetime.now().timetuple()),
        }

        result_json = json.dumps(result_dict).replace("\u0000", "")

        return Response(result_json, mimetype="application/json")
    except BaseException as ex:
        return jsonify({"error": str(ex)})


@app.route("/get_alarm_setup")
def get_alarm_setup():
    controller_id = int(request.args.get("id"))
    start = int(request.args.get("start", 1))
    count = int(request.args.get("count", 50))
    if count > 5:
        step = 5
    else:
        step = count

    try:
        uid = controllers[controller_id].uid
        result = {}
        start_alarm = start
        end_alarm = start + count - 1
        while start_alarm <= end_alarm and ("end_is_reached" not in result.keys()):
            modbus_request = ReadAllAlarmSetup(
                uid, start_alarm=start_alarm, read_alarms_number=step, input_dict=result
            )
            result_future = requests_executor.submit(
                modbus_request.execute, client=client
            )
            result = result_future.result()
            start_alarm += step

        uid_dict = {
            controller.uid: internal_id
            for internal_id, controller in controllers.items()
        }

        # server_logger.debug(str(uid_dict))
        # server_logger.debug(str(result))
        replaced_uids_dict = {
            uid_dict[uid]: alarms
            for uid, alarms in result.items()
            if uid != "end_is_reached"
        }

        result_dict = {
            "setup": replaced_uids_dict,
            "timestamp": time.mktime(datetime.now().timetuple()),
        }

        # result_json= json.dumps(result_dict)

        # return Response(result_json,
        # mimetype='application/json')
        return jsonify(
            result_dict,
        )

    except BaseException as ex:
        return jsonify({"error": str(ex)})


@app.route("/write_alarm_setup", methods=["POST"])
def write_alarm_setup():
    controller_id = int(request.args.get("id", 7))
    alarm_setup_number = int(request.args.get("number", 1))
    request_json = request.json

    try:
        uid = controllers[controller_id].uid
        modbus_request = WriteAlarmSetupRequest(
            uid, alarm_setup_number, json.loads(request.json)
        )
        result_future = requests_executor.submit(modbus_request.execute, client=client)
        response = result_future.result()
        return redirect(
            url_for(
                "get_alarm_setup", id=controller_id, start=alarm_setup_number, count=1
            )
        )
    except BaseException as ex:
        return jsonify({"error": str(ex)})


if __name__ == "__main__":
    config = get_com_port_setup()
    client = ModbusClient(
        method=config["method"],
        port=config["port"],
        stopbits=int(config["stopbits"]),
        bytesize=int(config["bytesize"]),
        parity=config["parity"],
        baudrate=int(config["baudrate"]),
    )
    connection = client.connect()

    init_logger()
    server_logger.info("Start server")

    requesting_tasks_pusher.start()

    serve(app, host="127.0.0.1", port=5000, threads=1)
    # app.run()
