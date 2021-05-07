from os import path
from . import get_template

def generate_markdown(schema, title):
    register_map_template = "RegisterMap.md.j2"
    template = get_template(register_map_template)
    fname = "RegisterMap.md"
    rendering = template.render(schema=schema)
    with open(fname, 'w') as f:
        f.write(rendering)


