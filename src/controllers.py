from prolon_modbus_registers import *
import sqlite3 as sqlite
from sqlite3 import Row
import time
import os
from datetime import timedelta

SCRIPT_WORK_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))

controllers_db = os.path.join(SCRIPT_WORK_DIR, "resources", "controllers_data.db")
store_values_table = "realtime_values"
controllers_table = "controllers"

import logging

logger = logging.getLogger("boilers")


def remove_old_records(store_deep, remove_logger=logger):
    now_timestamp = time.mktime(datetime.now().timetuple())
    oldest_record_timestamp = int(now_timestamp - store_deep)
    try:
        con = sqlite.connect(controllers_db)
        cursor = con.cursor()
        sql = "DELETE FROM {} WHERE timestamp < {}".format(
            store_values_table, oldest_record_timestamp
        )

        remove_logger.debug(
            "Remove local store records older when {}".format(
                datetime.fromtimestamp(oldest_record_timestamp)
            )
        )
        cursor.execute(sql)
        removed_rows_count = cursor.rowcount
        con.commit()
        remove_logger.debug("Removed {} rows".format(removed_rows_count))
    except BaseException as ex:
        remove_logger.error("Remove old records error {}".format(ex))
    finally:
        if con:
            con.close()


def store_controllers_memory(controllers_list):
    # (List[ProlonController]):->None
    try:
        con = sqlite.connect(controllers_db)
        cursor = con.cursor()
        sql = (
            "INSERT OR IGNORE INTO "
            + store_values_table
            + "(controller_id,register_address,timestamp,value,register_type) VALUES (?,?,?,?,?) "
        )

        for controller in controllers_list:
            assert isinstance(controller, ProlonController)
            for reg_type, registers in controller.operative_values_memory.items():
                for register_address, prolon_value in registers.items():
                    assert isinstance(prolon_value, ProlonValue)
                    cursor.execute(
                        sql,
                        (
                            controller.internal_id,
                            register_address,
                            time.mktime(prolon_value.timestamp.timetuple()),
                            prolon_value.value,
                            ProlonController.register_types[reg_type],
                        ),
                    )

        con.commit()
    finally:
        if con:
            con.close()


def get_controllers_in_system():
    #TODO: load controllers from database
    controllers = {
        1: ProlonController(
            name="Main Boiler",
            uid=2,
            modbus_map=get_m2000_boiler_modbus_map(),
            internal_id=1,
        ),
        1: ProlonController(
            name="Pair Boiler",
            uid=3,
            modbus_map=get_m2000_boiler_modbus_map(),
            internal_id=2,
        )
    }

    for controller in controllers.values():
            controller.add_read_input_regs_request(0, 21)

    return controllers


def get_data_stored_after(controllers_update_info, config, logger=logger):
    con = sqlite.connect(controllers_db)
    con.row_factory = Row
    cursor = con.cursor()

    result = {}
    for controller_id, timestamp in controllers_update_info.items():
        assert isinstance(timestamp, datetime)
        try:
            logger.debug(
                "Get data for controller {} after {}".format(controller_id, timestamp)
            )
            sql = (
                "SELECT * FROM "
                + store_values_table
                + " WHERE controller_id = "
                + str(controller_id)
                + " AND timestamp>"
                + str(time.mktime(timestamp.timetuple()))
                + " ORDER BY timestamp ASC LIMIT 10000"
            )
            cursor.execute(sql)
            records = cursor.fetchall()

            result[controller_id] = []
            for record in records:
                result[controller_id].append(
                    {
                        "timestamp": timestamp.fromtimestamp(record["timestamp"]),
                        "register_number": record["register_address"],
                        "register_type": record["register_type"],
                        "value": record["value"],
                    }
                )
        except BaseException as ex:
            logger.error(
                "Error at get data stored after {} for controller {}:{}".format(
                    timestamp, controller_id, ex
                )
            )
    cursor.close()
    con.close()
    return result


def create_data_forwarding_request(
    from_controller,
    from_register_type,
    from_register_number,
    to_controller,
    to_register_type,
    to_register_number,
):
    assert isinstance(from_controller, ProlonController)
    assert isinstance(to_controller, ProlonController)
    read_prolon_value = from_controller.operative_values_memory[from_register_type][
        from_register_number
    ]
    assert isinstance(read_prolon_value, ProlonValue)

    read_value = read_prolon_value.value

    write_prolon_register = to_controller.modbus_map[to_register_type][
        to_register_number
    ]
    assert isinstance(write_prolon_register, ProlonRegister)
    register_value = write_prolon_register.get_register_from_value(read_value).value

    request = ModbusRequest.create_write_register_req(
        to_register_number, register_value, to_controller.uid
    )
    return request


class ProlonController:
    register_types = {"HOLDING": 3, "INPUT": 4}

    def __init__(self, name, uid, modbus_map, internal_id=1):
        self.name = name  # type:str
        self.uid = uid  # type:int
        self.modbus_map = modbus_map
        self.operative_values_memory = {
            "HOLDING": {},
            "INPUT": {},
        }  # map of regular updated values
        self.last_update = datetime.now()
        self.last_update_status = "OK"
        self.operative_memory_requests = (
            []
        )  # list of requests for operative_values_memory
        self.internal_id = internal_id
        if len(self.modbus_map["INPUT"].keys()) > 0:
            self.max_input_register_number = max(self.modbus_map["INPUT"].keys())
        else:
            self.max_input_register_number = 0

        if len(self.modbus_map["HOLDING"].keys()) > 0:
            self.max_holding_register_number = max(self.modbus_map["HOLDING"].keys())
        else:
            self.max_holding_register_number = 0

    def decode_modbus_responce_to_json(self, request, responce_registers):
        type = "HOLDING"
        if request.fc == 4:
            type = "INPUT"

        result = {}
        register_number = request.start
        for register in responce_registers:
            if register_number in self.modbus_map[type]:
                result[register_number] = (
                    self.modbus_map[type][register_number]
                    .get_value_from_register(register)
                    .to_json()
                )
            register_number += 1

        return result

    def add_read_holding_regs_request(self, start_register, registers_count):
        # if stop_register - start_register > 125:
        # raise ValueError('Stop-start difference is to big!(>125)')
        # else:
        self.operative_memory_requests.append(
            ModbusRequest.create_read_hold_regs_req(
                start_register, registers_count, self.uid
            )
        )
        for register in range(start_register, start_register + registers_count - 1):
            if register in self.modbus_map["HOLDING"]:
                prolon_register = self.modbus_map["HOLDING"][
                    register
                ]  # type: ProlonRegister
                self.operative_values_memory["HOLDING"][
                    prolon_register.register_number
                ] = prolon_register.get_value_from_register(0)

    def add_read_input_regs_request(self, start_register, count):
        # if stop_register - start_register > 125:
        # raise ValueError('Stop-start difference is to big!(>125)')
        # else:
        self.operative_memory_requests.append(
            ModbusRequest.create_read_input_regs_req(start_register, count, self.uid)
        )
        for register in range(start_register, count):
            if register in self.modbus_map["INPUT"]:
                prolon_register = self.modbus_map["INPUT"][
                    register
                ]  # type: ProlonRegister
                default_value = prolon_register.get_value_from_register(0)
                default_value.timestamp = datetime.fromtimestamp(0)
                self.operative_values_memory["INPUT"][
                    prolon_register.register_number
                ] = default_value

    def update_memory_from_responce(
        self, responce_registers, start_register, responce_fnc
    ):
        register_address = start_register
        reg_types = "INPUT"
        if responce_fnc == 3:
            reg_types = "HOLDING"

        self.last_update = datetime.now()
        for responce_register in responce_registers:
            if register_address in self.modbus_map[reg_types].keys():
                prolon_register = self.modbus_map[reg_types][
                    register_address
                ]  # type: ProlonRegister
                value_from_controller = prolon_register.get_value_from_register(
                    responce_register
                )
                current_memory_value = self.operative_values_memory[reg_types][
                    prolon_register.register_number
                ]
                assert isinstance(current_memory_value, ProlonValue)
                if (
                    current_memory_value.value != value_from_controller.value
                    or value_from_controller.timestamp - current_memory_value.timestamp
                    >= timedelta(hours=1)
                ):
                    # logger.debug("Update value in {}({}):{}({}) from {}=>{}".format(
                    # self.name
                    # , self.uid
                    # , value_from_controller.name
                    # , register_address
                    #  , current_memory_value.value
                    #   , value_from_controller.value))

                    self.operative_values_memory[reg_types][
                        prolon_register.register_number
                    ] = value_from_controller
            register_address += 1

    def store_memory(self):

        print("=====HOLDING====")
        for value in self.operative_values_memory["HOLDING"].values():
            print(str(value))
        print("====INPUT===")
        for value in self.operative_values_memory["INPUT"].values():
            print(str(value))

        print(
            "total registers = "
            + str(
                len(self.operative_values_memory["HOLDING"])
                + len(self.operative_values_memory["INPUT"])
            )
        )
