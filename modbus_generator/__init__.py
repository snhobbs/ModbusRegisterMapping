from jinja2 import Template, Environment, FileSystemLoader
from os import path

def get_template(language, name):
    template_directory = path.join(path.dirname(__file__), 'templates', language)
    env = Environment(loader=FileSystemLoader(template_directory))
    template = env.get_template(name)
    return template


from . schema import *
from . ModbusEntries import *
from . data_store import *
from . modbus_basic import *
from . WindLdr import *
from . libmodbus import *
from . pymodbus import *
from . documentation import *
