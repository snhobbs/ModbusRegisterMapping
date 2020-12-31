from jinja2 import Template, Environment, FileSystemLoader
from os import path

def MakeHeader(entries, fname, namespace):
    template_directory = path.join(path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_directory))
    data_store_template = "MappedDataStore.h.j2"
    template = env.get_template(data_store_template)
    rendering = template.render(entries=entries, namespace=namespace, fname=fname, timestamp=datetime.datetime.now())
    with open(fname, 'w') as f:
        f.write(rendering)
    os.system("clang-format %s -i --style=Google"%fname)


