from jinja2 import Template, Environment, FileSystemLoader
from os import path
#def MakeMap(template_directory, entries, fname, title):
def MakeMap(entries, fname, title):
    template_directory = path.join(path.dirname(__file__), 'templates', "Documentation")
    env = Environment(loader=FileSystemLoader(template_directory))
    register_map_template = "RegisterMap.md.j2"
    template = env.get_template(register_map_template)
    rendering = template.render(entries=entries, title=title)
    with open(fname, 'w') as f:
        f.write(rendering)


