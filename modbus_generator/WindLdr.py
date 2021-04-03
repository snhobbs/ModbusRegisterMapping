from . ModbusEntries import FunctionType
from . import get_template
from os import path

def make_variable_name(entry):
    max_length = 20
    append = ""
    if entries.registers > 1:
        append += "_%d"%(self.registers - 1)
    append += "_%d"%0xff

    name = entry.name
    if len(append) + len(entry.name) > max_length:
        split = entry.name.split("_")
        if len(split) > 2:
            name = "_".join(split[1:])

    return name[:max_length-len(append)]


class WindLDREntry():
    def __init__(self, map_entry, slave):
        self.map_entry = map_entry
        self.plc_address = 0
        self.slave = slave

    @property
    def functions(self):
        if self.function_type == FunctionType.kHolding:
            return [self.map_entry.read_code, self.map_entry.write_code]
        return [self.map_entry.read_code]

    @property
    def name(self):
        return self.map_entry.name

    @property
    def dtype(self):
        return self.map_entry.dtype

    @property
    def length(self):
        return self.map_entry.length

    @property
    def registers(self):
        return self.map_entry.registers

    @property
    def address(self):
        return self.map_entry.address

    @property
    def function_type(self):
        return self.map_entry.function_type

    @property
    def plc_variable_name(self):
        return make_variable_name(self.entry)

def generate_windldr_config(schema, offset):
    master_address = 0

    register_map_template = "WindLDRConfiguration.csv.j2"
    template = get_template(register_map_template)
    rendering = template.render(schema=schema)
    with open(register_map_template.strip('.j2'), 'w') as f:
        f.write(rendering)

    tag_template = "WindLDRTagEditor.csv.j2"
    template = get_template(tag_template)
    rendering = template.render(schema=schema)
    with open(tag_template.strip('.j2'), 'w') as f:
        f.write(rendering)

