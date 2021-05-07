import os, sys, datetime, math
from jinja2 import Template, Environment, FileSystemLoader
from enum import Enum, IntEnum
import data_stores

def GetDataTypeCType(dtype):
    if dtype == "string":
        return "uint8_t"
    else:
        return dtype + "_t"


def GetDataTypeSize(dtype):
    if dtype in ["uint8", "int8", "string"]:
        return 1
    elif dtype in ["uint16", "int16"]:
        return 2
    elif dtype in ["uint32", "int32"]:
        return 4
    if dtype in ["uint64", "int64"]:
        return 8


def SetAddresses(entries):
    address = 0
    for entry in entries:
        if entry.dtype not in ["uint16", "int16"]:
            entry.address = address + address % 2
        else:
            entry.address = address
        address = entry.address + entry.registers


class FunctionType(IntEnum):
    kInput = 3
    kHolding = 4


class Entry:
    storage_type="uint16"
    def __init__(self, name, dtype, length, function_type, address=None):
        self.name = name
        self.dtype = dtype
        self.length = length
        self.function_type = function_type
        self._address = address

        assert(type(self.name) is str)
        assert(type(self.dtype) is str)
        assert(self.length >= 1)

        assert(self.registers > 0)
        assert(type(self.function_type) is str)

    ''' Rounded up length to be integer multiple of storage type '''
    @property
    def required_size(self):
        return self.length + (GetDataTypeSize(self.dtype) * self.length) % GetDataTypeSize(self.storage_type)

    @property
    def storage_length(self):
        return int(math.ceil(float(GetDataTypeSize(self.dtype) * self.required_size) / GetDataTypeSize(self.storage_type)))

    @property
    def dtype_ctype(self):
        return GetDataTypeCType(self.dtype)


    def set_address(self, address):
        self._address = address

    def address(self):
        return self.address

    @property
    def registers(self):
        assert(self.storage_type =="uint16")
        return self.storage_length

    @property
    def dtype_ctype(self):
        return GetDataTypeCType(self.dtype)

    @property
    def read_code(self):
        if self.function_type == "holding":
            return 3
        return 4

    @property
    def write_code(self):
        if self.function_type == "holding":
            return 16
        else:
            assert(0)

    @property
    def memory_code(self):
        if self.function_type == "holding":
            return 4
        return 3

class Slave:
    def __init__(self, address):
        self.address = address
