import copy
from jinja2 import Template, Environment, FileSystemLoader
from modbus_generator import MapEntry, DataType, FunctionType, SetAddresses, Slave, WindLDREntry, MakeWindLDRConfig, MapEntry, ModbusRegister
import modbus_generator
import sys

input_registers = (
    ModbusRegister('version', DataType.kString, 64, FunctionType.kInput),
    ModbusRegister('firmware_version', DataType.kString, 64, FunctionType.kInput),
    ModbusRegister('compile_date', DataType.kString, 64, FunctionType.kInput),
    ModbusRegister('compile_time', DataType.kString, 64, FunctionType.kInput),
    ModbusRegister('serial_number', DataType.kString, 40, FunctionType.kInput),

    ModbusRegister('fault_status', DataType.uint16_t, 1, FunctionType.kInput),

    ModbusRegister('p5_micro_volts', DataType.int32_t, 1, FunctionType.kInput),
    ModbusRegister('p5_reading', DataType.uint32_t, 1, FunctionType.kInput),

    ModbusRegister('p23_micro_volts', DataType.int32_t, 1, FunctionType.kInput),
    ModbusRegister('p23_reading', DataType.uint32_t, 1, FunctionType.kInput),

    ModbusRegister('vlo_micro_volts', DataType.int32_t, 1, FunctionType.kInput),
    ModbusRegister('vlo_reading', DataType.uint32_t, 1, FunctionType.kInput),

    ModbusRegister('thermistor_temp_spi', DataType.int32_t, 1, FunctionType.kInput),
    ModbusRegister('thermistor_temp_mcu', DataType.int32_t, 1, FunctionType.kInput),

    ModbusRegister('data_frequency', DataType.uint32_t, 1, FunctionType.kInput),

    ModbusRegister('p3_3_micro_volts', DataType.int32_t, 1, FunctionType.kInput),
    ModbusRegister('p3_3_reading', DataType.uint32_t, 1, FunctionType.kInput),
)

holding_registers = (
    ModbusRegister('analog_output0', DataType.uint32_t, 1, FunctionType.kHolding),
    ModbusRegister('analog_output1', DataType.uint32_t, 1, FunctionType.kHolding),
    ModbusRegister('isp_mode', DataType.uint32_t, 1, FunctionType.kHolding),
    ModbusRegister('slave_address_unlock', DataType.uint32_t, 1, FunctionType.kHolding),
    ModbusRegister('slave_address', DataType.uint16_t, 1, FunctionType.kHolding),
    ModbusRegister('clear_faults', DataType.uint32_t, 1, FunctionType.kHolding),
    ModbusRegister('start_data_read', DataType.uint32_t, 1, FunctionType.kHolding),
)

def GetInputRegisterMapEntries():
    InputRegisterMapEntries = [MapEntry(register=pt) for pt in input_registers]
    SetAddresses(InputRegisterMapEntries)
    return InputRegisterMapEntries

def GetHoldingRegisterMapEntries():
    HoldingRegisterMapEntries = [MapEntry(register=pt) for pt in holding_registers]
    SetAddresses(HoldingRegisterMapEntries)
    return HoldingRegisterMapEntries

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
    modbus_generator.MakeMap(GetHoldingRegisterMapEntries(), "HoldingRegisterMappedDataStore.md", title="Holding Register Map")
    modbus_generator.MakeMap(GetInputRegisterMapEntries(), "InputRegisterMappedDataStore.md", title="Input Register Map")

    modbus_generator.MakeHeader(GetHoldingRegisterMapEntries(), "HoldingRegisterMappedDataStore.h", name="HoldingRegisters")
    modbus_generator.MakeHeader(GetInputRegisterMapEntries(), "InputRegisterMappedDataStore.h", name="InputRegisters")

    modbus_generator.MakeLibModbusTest(
        input_registers=GetInputRegisterMapEntries(),
        holding_registers=GetHoldingRegisterMapEntries(),
        includes=["HoldingRegisterMappedDataStore.h", "InputRegisterMappedDataStore.h"])

    modbus_generator.MakePyModbusTest(
        input_registers=GetInputRegisterMapEntries(),
        holding_registers=GetHoldingRegisterMapEntries(),
        includes=["HoldingRegisterMappedDataStore.h", "InputRegisterMappedDataStore.h"])

    MakeWindLdrMap()
    modbus_generator.MakeFbs(GetHoldingRegisterMapEntries(), "HoldingRegisterMappedDataStore.fbs", name="HoldingRegisters")
