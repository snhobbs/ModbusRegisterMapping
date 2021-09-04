import sys
from time import sleep
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

from modbus_server_objects import modbus_entries
from python_utilities import utilities
RegistersToBytes = utilities.RegistersToBytes
DecodeText = utilities.DecodeText
TransformBytesToDataType = utilities.TransformBytesToDataType

sleep_time = 0


class ModbusMaster:
    parity = 'N'
    bytesize = 8
    stopbits = 1
    method= "rtu"
    timeout_seconds = .1

    def __init__(self, port, baud = 9600):
        self.port = port
        self.baudrate = baud
        #method=self.method,
        self.client = ModbusClient(method=self.method, port=self.port, parity=self.parity,
            timeout=self.timeout_seconds, bytesize=self.bytesize,
            stopbits=self.stopbits, baudrate=self.baudrate)
        self.connect()

    def connect(self):
        self.client.connect()
        print("Connection Successful")

    def disconnect(self):
        self.client.close()
        print("Connection Closed Successfully")

def print_response(response, entry):
    data_bytes = RegistersToBytes(response.registers)
    value = TransformBytesToDataType(entry.dtype, data_bytes)
    print(entry.name, value)

def main(port, address=246, baud=9600):
    master = ModbusMaster(port, baud)
    for entry in modbus_entries:
        if entry.type == "input register":
            response = master.client.read_input_registers(entry.address, entry.registers, unit=address)
            print_response(response, entry)
        elif entry.type == "holding register":
            print(entry)
            response = master.client.read_holding_registers(entry.address, entry.registers, unit=address)
            print_response(response, entry)
            register_values = [0xff - p for p in range(entry.registers)]
            sleep(sleep_time)
            write_values = list(range(entry.registers))
            response = master.client.write_registers(entry.address, register_values, unit=address)
            print(f"{entry.name} Response:", response)
    master.disconnect()

if __name__ == "__main__":
    port = "/tmp/ptyp0"
    address = 1
    if len(sys.argv) > 1:
        port = sys.argv[1]
    if len(sys.argv) > 2:
        address = int(sys.argv[2])
    print("Device: %s"%port)
    print("Address: %d"%address)
    main(port, address, baud=9600)
