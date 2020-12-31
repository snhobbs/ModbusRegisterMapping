from jinja2 import Template, Environment, FileSystemLoader

def MakeLibModbusTest(template_directory, input_registers, holding_registers, includes):
    env = Environment(loader=FileSystemLoader(template_directory))
    register_map_template = "LibModbusTestMaster.cpp.j2"
    fname = register_map_template.strip(".j2")
    template = env.get_template(register_map_template)
    rendering = template.render(input_registers=input_registers, holding_registers=holding_registers, includes=includes)
    with open(fname, 'w') as f:
        f.write(rendering)

