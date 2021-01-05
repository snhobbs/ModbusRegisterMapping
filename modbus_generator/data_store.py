from jinja2 import Template, Environment, FileSystemLoader
from os import path
import datetime, os
from data_stores import make, Struct, DataType


def MakeHeader(entries, fname, name):
    make(Struct(name, entries, DataType.uint16_t), fname)
    os.system("clang-format %s -i --style=Google"%fname)
