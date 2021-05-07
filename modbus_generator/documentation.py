from os import path
from . import get_template

def generate_markdown(schema):
    register_map_template = "RegisterMap.md.j2"
    template = get_template(register_map_template)
    fname = "RegisterMap.md"
    rendering = template.render(schema=schema, title="title")
    with open(fname, 'w') as f:
        f.write(rendering)


