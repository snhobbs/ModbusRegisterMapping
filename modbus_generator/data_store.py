from jinja2 import Template, Environment, FileSystemLoader
from os import path
import datetime, os

class StructEntry:
    def __init__(self, name, dtype, length, padding=0):
        self.name = name
        self.dtype = dtype
        self.length = length
        self.padding = padding

        assert(type(self.name) is str)
        assert(type(self.dtype) is str)
        assert(self.length >= 1)

    @property
    def dtype_ctype(self):
        return GetDataTypeCType(self.dtype)

def MakeHeader(entries, fname, name):
    template_directory = path.join(path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_directory))
    register_map_template = "MappedDataStore.h.j2"
    template = env.get_template(register_map_template)
    rendering = template.render(name=name, entries=entries, timestamp=datetime.datetime.now())
    with open(register_map_template.strip('.j2'), 'w') as f:
        f.write(rendering)

    os.system("clang-format %s -i --style=Google"%fname)
