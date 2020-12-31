import copy
from jinja2 import Template, Environment, FileSystemLoader
from modbus_generator import MapEntry, DataType, FunctionType, SetAddresses, Slave, WindLDREntry, MakeWindLDRConfig, ModbusRegister
import modbus_generator
import sys

input_registers = (
    ModbusRegister('version', DataType.kString, 64, FunctionType.kInput),
    ModbusRegister('firmware_version', DataType.kString, 64, FunctionType.kInput),
    ModbusRegister('compile_date', DataType.kString, 64, FunctionType.kInput),
    ModbusRegister('compile_time', DataType.kString, 64, FunctionType.kInput),
    ModbusRegister('serial_number', DataType.kString, 40, FunctionType.kInput),

    ModbusRegister('fault_status', DataType.uint16_t, 1, FunctionType.kInput),
    ModbusRegister('analog_0_algorithm', DataType.uint16_t, 1, FunctionType.kInput),
    ModbusRegister('analog_1_algorithm', DataType.uint16_t, 1, FunctionType.kInput),
    ModbusRegister('analog_0_software_trip', DataType.int32_t, 1, FunctionType.kInput),
    ModbusRegister('analog_1_software_trip', DataType.int32_t, 1, FunctionType.kInput),

    ModbusRegister('p5_micro_volts', DataType.int32_t, 1, FunctionType.kInput),
    ModbusRegister('p5_reading', DataType.uint32_t, 1, FunctionType.kInput),

    ModbusRegister('p23_micro_volts', DataType.int32_t, 1, FunctionType.kInput),
    ModbusRegister('p23_reading', DataType.uint32_t, 1, FunctionType.kInput),

    ModbusRegister('vlo_micro_volts', DataType.int32_t, 1, FunctionType.kInput),
    ModbusRegister('vlo_reading', DataType.uint32_t, 1, FunctionType.kInput),

    ModbusRegister('thermistor_temp_spi', DataType.int32_t, 1, FunctionType.kInput),
    ModbusRegister('thermistor_temp_mcu', DataType.int32_t, 1, FunctionType.kInput),

    ModbusRegister('mw', DataType.uint32_t, 1, FunctionType.kInput),
    ModbusRegister('mw_max', DataType.uint32_t, 1, FunctionType.kInput),
    ModbusRegister('mw_early_detect_max', DataType.int32_t, 1, FunctionType.kInput),
    ModbusRegister('mw_early_detect_averaged', DataType.int32_t, 1, FunctionType.kInput),

    ModbusRegister('sw', DataType.uint32_t, 1, FunctionType.kInput),
    ModbusRegister('sw_max', DataType.uint32_t, 1, FunctionType.kInput),
    ModbusRegister('sw_spark_detect_max', DataType.int32_t, 1, FunctionType.kInput),
    ModbusRegister('sw_spark_detect_averaged', DataType.int32_t, 1, FunctionType.kInput),

    ModbusRegister('vis', DataType.uint32_t, 1, FunctionType.kInput),
    ModbusRegister('vis_max', DataType.uint32_t, 1, FunctionType.kInput),
    ModbusRegister('vis_averaged', DataType.int32_t, 1, FunctionType.kInput),

    ModbusRegister('shtc3_temperature', DataType.int32_t, 1, FunctionType.kInput),
    ModbusRegister('shtc3_humidity', DataType.int32_t, 1, FunctionType.kInput),

    ModbusRegister('sw_reading_low', DataType.uint32_t, 1, FunctionType.kInput),
    ModbusRegister('sw_reading_high', DataType.uint32_t, 1, FunctionType.kInput),
    ModbusRegister('sw_translated_low', DataType.int32_t, 1, FunctionType.kInput),
    ModbusRegister('mw_reading_low', DataType.uint32_t, 1, FunctionType.kInput),
    ModbusRegister('mw_reading_high', DataType.uint32_t, 1, FunctionType.kInput),
    ModbusRegister('mw_translated_low', DataType.int32_t, 1, FunctionType.kInput),
    ModbusRegister('data_frequency', DataType.uint32_t, 1, FunctionType.kInput),

    ModbusRegister('vlo_spi_micro_volts', DataType.int32_t, 1, FunctionType.kInput),
    ModbusRegister('vlo_spi_reading', DataType.uint32_t, 1, FunctionType.kInput),

    ModbusRegister('p3_3_micro_volts', DataType.int32_t, 1, FunctionType.kInput),
    ModbusRegister('p3_3_reading', DataType.uint32_t, 1, FunctionType.kInput),
)

holding_registers = (
    ModbusRegister('alarm_threshold', DataType.uint32_t, 1, FunctionType.kHolding),
    ModbusRegister('analog_output0', DataType.uint32_t, 1, FunctionType.kHolding),
    ModbusRegister('analog_output1', DataType.uint32_t, 1, FunctionType.kHolding),
    ModbusRegister('isp_mode', DataType.uint32_t, 1, FunctionType.kHolding),
    ModbusRegister('slave_address_unlock', DataType.uint32_t, 1, FunctionType.kHolding),
    ModbusRegister('slave_address', DataType.uint16_t, 1, FunctionType.kHolding),
    ModbusRegister('clear_faults', DataType.uint32_t, 1, FunctionType.kHolding),
    ModbusRegister('start_data_read', DataType.uint32_t, 1, FunctionType.kHolding),
)

def GetInputRegisterMapEntries():
    InputRegisterMapEntries = [MapEntry(pt) for pt in input_registers]
    SetAddresses(InputRegisterMapEntries)
    return InputRegisterMapEntries

def GetHoldingRegisterMapEntries():
    HoldingRegisterMapEntries = [MapEntry(pt) for pt in holding_registers]
    SetAddresses(HoldingRegisterMapEntries)
    return HoldingRegisterMapEntries

def Make(entries, template_dir, name, namespace, title):
    MakeHeader(template_dir, entries, name + ".h", namespace)
    MakeMap(template_dir, entries, name + ".md", title)

def MakeWindLdrMap(template_dir):
    MapEntries = list(GetHoldingRegisterMapEntries()) + list(GetInputRegisterMapEntries())

    essential_entries = list(pt for pt in MapEntries if pt.name in (
        'version',
        'firmware_version',
        'fault_status',
        'isp_mode',
        'slave_address_unlock',
        'slave_address'))
    assert(len(essential_entries) == 6)

    operating_entries = list(pt for pt in MapEntries if pt.name in (
        'thermistor_temp_spi',
        'mw',
        'mw_early_detect_averaged',
        'sw',
        'sw_spark_detect_averaged',
        'vis',
        'shtc3_temperature',
        'shtc3_humidity'))
    assert(len(operating_entries) == 8)

    def EntryInEntries(entry, entries):
        for pt in entries:
            if pt.name == entry.name:
                return True
        return False

    operating_entries.extend(GetHoldingRegisterMapEntries())
    operating_entries = list(filter(lambda x : not EntryInEntries(x, essential_entries), operating_entries))

    operating_entries.sort(key = lambda x : int(x.address) + 100000 * x.read_code)
    essential_entries.sort(key = lambda x : int(x.address) + 100000 * x.read_code)
    slaves = (Slave(246), Slave(1), Slave(2), Slave(3), Slave(4), Slave(5), Slave(6))
    plc_address = 5000
    config_entries = list()

    for entry in essential_entries:
        print(entry.address)
        for slave in slaves:
            config_entry = WindLDREntry(entry, slave)
            config_entry.plc_address = plc_address
            config_entries.append(config_entry)
            plc_address += entry.registers

    for entry in operating_entries:  # skip the default detector
        print(entry.address)
        for slave in slaves[1:]:
            config_entry = WindLDREntry(entry, slave)
            config_entry.plc_address = plc_address
            config_entries.append(config_entry)
            plc_address += entry.registers

    MakeWindLDRConfig(template_dir, config_entries, 'WindLDRModbusMasterConfiguration.csv')

def ModbusDict(template_directory):
    env = Environment(loader=FileSystemLoader(template_directory))
    register_map_template = "ModbusEntryDict.py.j2"
    template = env.get_template(register_map_template)
    rendering = template.render(holding_registers=list(GetHoldingRegisterMapEntries()), input_registers=list(GetInputRegisterMapEntries()))
    with open(register_map_template.strip(".j2"), 'w') as f:
        f.write(rendering)

if __name__ == "__main__":
    template_dir = "templates"

    mode = ""
    if(len(sys.argv) > 1):
        mode = sys.argv[1]
    mode = mode.upper()

    print("Modbus Generation Mode %s"%mode)
    if mode == "DOCUMENTS" or mode == "ALL":
        modbus_generator.MakeMap(GetHoldingRegisterMapEntries(), "HoldingRegisterMappedDataStore.md", title="Holding Register Map")
        modbus_generator.MakeMap(GetInputRegisterMapEntries(), "InputRegisterMappedDataStore.md", title="Input Register Map")
        modbus_generator.MakeModbusTest(input_registers=GetInputRegisterMapEntries(), holding_registers=GetHoldingRegisterMapEntries(), includes=["HoldingRegisterMappedDataStore.h", "InputRegisterMappedDataStore.h"])
        #MakeWindLdrMap()
        #ModbusDict()

    elif mode == "SOURCE" or mode == "ALL":
        modbus_generator.MakeHeader(GetHoldingRegisterMapEntries(), "HoldingRegisterMappedDataStore.h", namespace="HoldingRegisters")
        modbus_generator.MakeHeader(GetInputRegisterMapEntries(), "InputRegisterMappedDataStore.h", namespace="InputRegisters")

    else:
        raise UserWarning("Unknown Mode %s"%mode)


