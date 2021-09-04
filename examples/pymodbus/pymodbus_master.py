import logging
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.exceptions import ModbusException
from python_utilities import utilities


def handle_response_error(response, request=None):
    if hasattr(response, "registers"):
        return
    error = f"Modbus Response {response}"
    if request:
        error += f". Request: {request}"
    logging.getLogger().warning(error)
    raise ModbusException(error)


def handle_response(response, request):
    logging.getLogger().info(request)
    if response.isError():
    #if not hasattr(response, "registers"):
        handle_response_error(response, request)
    else:
        logging.getLogger().info(f"{response} {response.registers}")
    data_bytes = utilities.RegistersToBytes(response.registers)
    value = utilities.TransformBytesToDataType(request.dtype, data_bytes)
    return value


def ReadHoldingRegisterEntry(entry, client, modbus_address):
    response = client.read_holding_registers(address=entry.address, count=entry.registers, unit=modbus_address)
    return handle_response(response, entry)


def ReadInputRegisterEntry(entry, client, modbus_address):
    response = client.read_input_registers(address=entry.address, count=entry.registers, unit=modbus_address)
    return handle_response(response, entry)

class ModbusMaster:
    parity = "N"
    bytesize = 8
    stopbits = 1
    method = "rtu"
    timeout_seconds = 0.5

    def __init__(self, port=None, baud=9600, socket=None):
        self.port = port
        self.baudrate = baud
        # method=self.method,
        if port is None and socket is None:
            raise ValueError("Either port or socket must be specified")
        self.client = ModbusClient(method=self.method, port=self.port,
                                   parity=self.parity, timeout=self.timeout_seconds,
                                   bytesize=self.bytesize, stopbits=self.stopbits,
                                   baudrate=self.baudrate)
        if socket:
            self.client.socket = socket

    def connect(self):
        self.client.connect()
        print("Connection Successful")

    def disconnect(self):
        self.client.close()
