from jinja2 import Template, Environment, FileSystemLoader
from os import path
import datetime, os

def MakeFbs(entries, fname, name):
    template_directory = path.join(path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_directory))
    env.trim_blocks = True
    env.lstrip_blocks = True

    data_store_template = "flatbuffers.fbs.j2"
    template = env.get_template(data_store_template)
    rendering = template.render(entries=entries, name=name, fname=fname, timestamp=datetime.datetime.now())
    with open(fname, 'w') as f:
        f.write(rendering)

    os.system("clang-format %s -i --style=Google"%fname)

def generate_flatbuffers_schema(schema, namespace=None):
    if namespace is None:
        namespace = ""
    template_directory = path.join(path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_directory))
    env.trim_blocks = True
    env.lstrip_blocks = True

    data_store_template = "flatbuffers.fbs.j2"
    fname = data_store_template.strip(".j2")

    template = env.get_template(data_store_template)
    rendering = template.render(schema=schema, namespace=namespace, fname=fname, timestamp=datetime.datetime.now())
    with open(fname, 'w') as f:
        f.write(rendering)
