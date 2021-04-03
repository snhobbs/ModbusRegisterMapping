from jinja2 import Template, Environment, FileSystemLoader
from . ModbusEntries import FunctionType
from os import path

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
    def memory_code(self):
        return self.map_entry.memory_code

    @property
    def plc_variable_name(self):
        max_length = 20
        append = ""
        if self.registers > 1:
            append += "_%d"%(self.registers - 1)
        append += "_%d"%0xff
        name = self.name

        if len(append) + len(self.name) > max_length:
            split = self.name.split("_")
            if len(split) > 2:
                name = "_".join(split[1:])

        return name[:max_length-len(append)]

def MakeWindLDRConfig(entries, fname):
    template_directory = path.join(path.dirname(__file__), 'templates', "WindLDR")
    master_address = 0
    env = Environment(loader=FileSystemLoader(template_directory))
    for register_map_template in ("WindLDRConfiguration.csv.j2", "WindLDRTagEditor.csv.j2"):
        template = env.get_template(register_map_template)
        rendering = template.render(entries=entries, master_address=master_address)
        with open(register_map_template.strip('.j2'), 'w') as f:
            f.write(rendering)

def generate_windldr_config(schema, offset):
    pass

