from . import get_template

def generate_libmodbus_server(schema, includes=None):
    pass

def generate_libmodbus_master(schema, includes=None):
    if includes is None:
        includes = []

    template_name = "LibModbusTestMaster.cpp.j2"
    template = get_template(template_name)
    fname = template_name.strip(".j2")
    rendering = template.render(input_registers=schema.input_registers, holding_registers=schema.holding_registers, includes=includes)
    with open(fname, 'w') as f:
        f.write(rendering)
