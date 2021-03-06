from . import get_template

def generate_pymodbus_server(schema):
    pass

def generate_pymodbus_master(schema, includes=None):
    template_name = "PyModbusTestMaster.py.j2"
    template = get_template(template_name)
    fname = template_name.strip(".j2")
    rendering = template.render(input_registers=schema.input_registers, holding_registers=schema.holding_registers, includes=includes)
    with open(fname, 'w') as f:
        f.write(rendering)
