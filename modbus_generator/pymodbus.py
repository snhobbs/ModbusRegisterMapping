from jinja2 import Template, Environment, FileSystemLoader
from os import path
from . import get_template

class ModbusEntry:
    def __init__(self, name, dtype, length, address, registers, modbus_type):
        self.name = name
        self.dtype = dtype
        self.length = length
        self.address = address
        self.registers = registers
        self.type = modbus_type


def MakePyModbusTest(input_registers, holding_registers, includes):
    register_map_template = "PyModbusTestMaster.py.j2"
    fname = register_map_template.strip(".j2")
    template = get_template("PyModbus", register_map_template)
    rendering = template.render(input_registers=input_registers, holding_registers=holding_registers, includes=includes)
    with open(fname, 'w') as f:
        f.write(rendering)

def generate_pymodbus_server(schema):
    template = get_template("", "ModbusEntryDict.py.j2")
    entries = []
    for _, line in schema.iterrows():
        entries.append(ModbusEntry(line["name"], line["data type"], line["length"],  line["address"], line["register count"], line["type"]))
    rendering = template.render(entries=entries)
    return rendering


def generate_pymodbus_master(schema, includes=None):
    register_map_template = "PyModbusTestMaster.py.j2"
    fname = register_map_template.strip(".j2")
    template = get_template("PyModbus", register_map_template)
    rendering = template.render(input_registers=schema.input_registers, holding_registers=schema.holding_registers, includes=includes)
    with open(fname, 'w') as f:
        f.write(rendering)
