from jinja2 import Template, Environment, FileSystemLoader
from os import path

#def MakeLibModbusTest(template_directory, input_registers, holding_registers, includes):
def MakeLibModbusTest(input_registers, holding_registers, includes):
    template_directory = path.join(path.dirname(__file__), 'templates', "LibModbus")
    env = Environment(loader=FileSystemLoader(template_directory))
    register_map_template = "LibModbusTestMaster.cpp.j2"
    fname = register_map_template.strip(".j2")
    template = env.get_template(register_map_template)
    rendering = template.render(input_registers=input_registers, holding_registers=holding_registers, includes=includes)
    with open(fname, 'w') as f:
        f.write(rendering)

def generate_libmodbus_server(schema, includes=None):
    pass

def generate_libmodbus_master(schema, includes=None):
    pass
