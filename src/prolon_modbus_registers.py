import datetime
import time
from datetime import datetime
from pymodbus.exceptions import ModbusIOException
from pymodbus.pdu import ExceptionResponse
from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder, Endian
from pymodbus.client.sync import ModbusSerialClient

ALARMS_EU = {
    1: 100.0,  # F
    2: 1.0,  # %
    3: 1.0,  # ON/OFF
    5: 1.0,  # Occupied/Unoccupied
    16: 1.0,  # Comunnictaion
    0: 1.0,  # None
    11: 10.0,  # Pa
    8: 1.0,  # ppm
    14: 1.0,  # MID/WINTER/SUMMER
    13: 1.0,  # NONE/NO DAMP PRF/LOW DISCHx3/INNVAL DISCH
    12: 10.0,  # V
}


class ModbusRequest:
    def __init__(self, fc, start=0, count=0, uid=0, value=0, registers=None):
        self.fc = fc
        self.start = start
        self.stop = count
        self.uid = uid
        self.value = value
        self.registers = registers

    @classmethod
    def create_read_hold_regs_req(cls, start, count, uid):
        """
        creates read holding registers request instance
        Parameters
        ----------
        start:int
            start register number
        count: int
            registers count
        uid: int
            controller modbus uid

        Returns
        ----------
        ModbusRequest instance

        """
        return ModbusRequest(3, start, count, uid)

    @classmethod
    def create_read_input_regs_req(cls, start, count, uid):
        """
        create read input registers request
        Parameters
        ----------
        start:int
            start register number
        count: int
            registers count
        uid: int
            controller modbus uid

        Returns
        -------
        ModbusRequest instance
        """
        return ModbusRequest(4, start, count, uid)

    @classmethod
    def create_write_register_req(cls, address, value, uid):
        """
        create write holding register request
        Parameters
        ----------
        address:int
            register address
        value: int
           register value
        uid: int
           controller modbus uid

        Returns
        -------
        ModbusRequest instance
        """
        return ModbusRequest(fc=6, start=address, value=value, uid=uid)

    @classmethod
    def create_write_registers_request(cls, start, registers, uid):
        """
        create write holding registers request
        Parameters
        ----------
        start: int
            start register address
        registers: [int]
            registers list
        uid
            controller modbus uid

        Returns
        -------
        ModbusRequest instance
        """
        return ModbusRequest(10, start, uid, registers=registers)

    def execute(self, client):
        """
        execute request on given client
        Parameters
        ----------
        client

        Returns
        -------
        response registers or 'write_ok' msg(for write requests)
        """

        assert isinstance(client, ModbusSerialClient)
        if self.fc == 3:
            response = client.read_holding_registers(
                self.start, self.stop, unit=self.uid
            )
        if self.fc == 4:
            response = client.read_input_registers(self.start, self.stop, unit=self.uid)
        if self.fc == 6:
            response = client.write_register(
                unit=self.uid, address=self.start, value=int(self.value)
            )
        if self.fc == 10:
            assert isinstance(client, ModbusSerialClient)
            response = client.write_registers(self.start, self.registers)

        if isinstance(response, ExceptionResponse) or isinstance(
                response, ModbusIOException
        ):
            raise BaseException(str(response))

        if self.fc == 6 or self.fc == 10:
            return "write_ok"

        return response.registers


class WriteAlarmEmailRequest(object, ModbusRequest):
    def __init__(self, uid, email_number, email):
        start = 4451 + (email_number - 1) * 48
        self.fc = 10
        self.start = start
        self.uid = uid
        self.email = email

    def execute(self, client):
        builder = BinaryPayloadBuilder()
        builder.add_string(self.email)
        email_registers = builder.to_registers()

        while len(email_registers) < 48:
            email_registers.append(0)

        self.registers = email_registers

        try:
            response = super(WriteAlarmEmailRequest, self).execute(client)
        except BaseException as ex:
            if "no response" in ex.message.lower():
                return "write_ok"
            else:
                raise ex
        return response


class ReadAlarmEmailRequest(object, ModbusRequest):
    def __init__(self, uid, email_number):
        start = 4451 + (email_number - 1) * 48
        self.fc = 3
        self.start = start
        self.stop = 48
        self.uid = uid

    def execute(self, client):
        response = super(ReadAlarmEmailRequest, self).execute(client)
        decoder = BinaryPayloadDecoder.fromRegisters(response)
        result = decoder.decode_string(48).decode()
        return result


class ReadAlarmSetup(object, ModbusRequest):
    def __init__(self, uid, number):
        start = 4643 + (number - 1) * 24
        self.fc = 3
        self.start = start
        self.stop = 24
        self.uid = uid

    def execute(self, client):
        response = super(ReadAlarmSetup, self).execute(client)
        decoder = BinaryPayloadDecoder.fromRegisters(response, byteorder=Endian.Big)

        result = {
            "device": decoder.decode_16bit_int(),
            "reg_address": decoder.decode_16bit_int(),
            "alert_type": decoder.decode_16bit_int(),
            "alert_value": (decoder.decode_16bit_int() / 100.0),
            "alert_unit": decoder.decode_16bit_int(),
            "alert_group": decoder.decode_16bit_int(),
            "debounce_time": decoder.decode_16bit_int(),
            "device_type": decoder.decode_16bit_int(),
            "alert_name": str(decoder.decode_string(16)).replace("\x00", ""),
            "dev_name": str(decoder.decode_string(16)).replace("\x00", ""),
        }

        return result


class ReadAllAlarmSetup(object, ModbusRequest):
    def __init__(self, uid, start_alarm=1, read_alarms_number=5, input_dict={}):
        start = 4643
        self.fc = 3
        self.start_alarm_number = start_alarm
        self.start = start + (start_alarm - 1) * 24
        self.read_alarms_number = read_alarms_number
        self.stop = 24 * self.read_alarms_number
        self.uid = uid
        self.input_dict = input_dict

    def execute(self, client):
        response = super(ReadAllAlarmSetup, self).execute(client)
        decoder = BinaryPayloadDecoder.fromRegisters(response, byteorder=Endian.Big)
        # "[Reg 1: Device Address -->Bit9=ThisAlertHasNotChanged]
        # [Reg 2: Modbus Register to be polled]
        # [Reg 3: Alert Type (<,>,=,Periodic)]
        # [Reg 4: Alert Value]
        # [Reg 5: Alert Unit]
        # [Reg 6: Alert Group]
        # [Reg 7: Debounce Time -> MSB=SendNow]
        # [Reg 8: Device Type]
        # [Reg 9-16: Alert Name]
        # [Reg 17-24: Dev Name]"

        readed_alert_number = 0

        while readed_alert_number < self.read_alarms_number:
            device = decoder.decode_16bit_int()
            if device != 0:
                if device not in self.input_dict.keys():
                    self.input_dict[device] = {}

                alert_setup = {
                    "device_id": device,
                    "reg_address": decoder.decode_16bit_int(),
                    "alert_type": decoder.decode_16bit_int(),
                    "alert_raw_value": (decoder.decode_16bit_int()),
                    "alert_unit": decoder.decode_16bit_int(),
                    "alert_group": decoder.decode_16bit_int(),
                    "debounce_time": decoder.decode_16bit_int(),
                    "device_type": decoder.decode_16bit_int(),
                    "alert_name": str(decoder.decode_string(16))
                        .replace("\x00", "")
                        .replace("\x82", "_2"),
                    "dev_name": str(decoder.decode_string(16)).replace("\x00", ""),
                }

                alert_value_mult = ALARMS_EU.get(int(alert_setup["alert_unit"]), 1.0)
                alert_setup["alert_value"] = (
                        alert_setup["alert_raw_value"] / alert_value_mult
                )

                self.input_dict[device][
                    self.start_alarm_number + readed_alert_number
                    ] = alert_setup
                readed_alert_number += 1
            else:
                self.input_dict["end_is_reached"] = True
                break
        return self.input_dict


class WriteAlarmSetupRequest(object, ModbusRequest):
    def __init__(self, uid, alarm_setup_number, setup_json):
        start = 4643 + (alarm_setup_number - 1) * 24
        self.fc = 10
        self.start = start
        self.uid = uid
        self.setup_json = setup_json

    def setup_json_to_registers(self):

        alert_unit_mult = ALARMS_EU.get(int(self.setup_json["alert_unit"]), 1.0)
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        builder.add_16bit_int(int(self.setup_json["device_id"]))
        builder.add_16bit_int(int(self.setup_json["reg_address"]))
        builder.add_16bit_int(int(self.setup_json["alert_type"]))
        builder.add_16bit_int(
            int(float(self.setup_json["alert_value"]) * alert_unit_mult)
        )
        builder.add_16bit_int(int(self.setup_json["alert_unit"]))
        builder.add_16bit_int(int(self.setup_json["alert_group"]))
        builder.add_16bit_int(int(self.setup_json["debounce_time"]))
        builder.add_16bit_int(int(self.setup_json["device_type"]))

        alert_name = str(self.setup_json["alert_name"])
        builder.add_string(alert_name)

        str_len = len(alert_name)
        while str_len < 16:
            builder.add_8bit_int(0)
            str_len += 1

        dev_name = str(self.setup_json["dev_name"])

        builder.add_string(dev_name)

        str_len = len(dev_name)
        while str_len < 16:
            builder.add_8bit_int(0)
            str_len += 1

        registers = builder.to_registers()
        return registers

    def execute(self, client):

        self.registers = self.setup_json_to_registers()

        try:
            response = super(WriteAlarmSetupRequest, self).execute(client)
        except BaseException as ex:
            if "no response" in ex.message.lower():
                return "write_ok"
            else:
                raise ex
        return response


class ProlonValue:
    def __init__(self, name, value, timestamp):
        self.value = value  # type:float

        self.timestamp = timestamp  # type:datetime

        self.name = name  # type:str

    def __str__(self):
        return self.name + "=" + str(self.value)

    def to_json(self):
        values_dict = {
            "name": self.name,
            "value": self.value,
            "timestamp": time.mktime(self.timestamp.timetuple()),
        }
        return values_dict


class ProlonRegister:
    def __init__(self, name, register_number, mult=1):
        self.name = name
        self.register_number = register_number
        self.mult = mult

    def get_value_from_register(self, register_value):
        decoder = BinaryPayloadDecoder.fromRegisters(
            [register_value], byteorder=Endian.Big
        )
        decoded_value = decoder.decode_16bit_int()
        return ProlonValue(
            self.name, float(decoded_value) / float(self.mult), datetime.now()
        )

    def get_register_from_value(self, value):
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        int_value = int(value * self.mult)
        builder.add_16bit_int(int_value)
        register_value = builder.to_registers()[0]
        return ProlonValue(self.name, register_value, datetime.now())

    def write_to_database(self):
        print("write " + self.name + "=" + self.value)
