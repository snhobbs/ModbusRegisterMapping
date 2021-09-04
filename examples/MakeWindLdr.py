import copy
from modbus_generator import MapEntry, DataType, FunctionType, SetAddresses, Slave, WindLDREntry, MakeWindLDRConfig, MapEntry, ModbusRegister
import modbus_generator
import sys
from modbus_server_objects import modbus_entries

def GetInputRegisterMapEntries():
    return [pt for pt in modbus_entries if pt.type == "input register"]

def GetHoldingRegisterMapEntries():
    return [pt for pt in modbus_entries if pt.type == "holding register"]

def MakeWindLdrMap():
    map_entries = list(GetHoldingRegisterMapEntries()) + list(GetInputRegisterMapEntries())
    map_entries.sort(key = lambda x : int(x.address) + 100000 * x.read_code)
    slaves = (Slave(1), Slave(2), Slave(3), Slave(4), Slave(5), Slave(6))
    plc_address = 5000
    config_entries = list()
    for entry in map_entries:
        for slave in slaves:
            config_entry = WindLDREntry(entry, slave)
            config_entry.plc_address = plc_address
            config_entries.append(config_entry)
            plc_address += entry.registers

    MakeWindLDRConfig(config_entries, 'WindLDRModbusMasterConfiguration.csv')

if __name__ == "__main__":
    MakeWindLdrMap()
