import os, sys, datetime, math
from jinja2 import Template, Environment, FileSystemLoader
from enum import Enum, IntEnum
from data_stores import DataType, GetDataTypeCType, GetDataTypeSize
import data_stores



class FunctionType(IntEnum):
    kInput = 3
    kHolding = 4


class ModbusRegister(data_stores.StructEntry):
    def __init__(self, name, dtype, length, function_type):
        super().__init__(name, dtype, length)
        self.storage_type = DataType.uint16_t
        self.function_type = function_type

        assert(self.registers > 0)
        assert(self.length >= 1)
        assert(type(self.function_type) is FunctionType)

    @property
    def registers(self):
        return self.storage_length



class MapEntry(ModbusRegister):
    def __init__(self, **kwargs):
        if "register" in kwargs:
            reg = kwargs["register"]
            super().__init__(reg.name, reg.dtype, reg.length, reg.function_type)
        else:
            super().__init__(kwargs["name"], kwargs["dtype"], kwargs["length"], kwargs["function_type"])
        self._address = None

    def __repr__(self):
        return f"{type(self)}({self.name}, {self.dtype}, {self.length}, {self.address}, {self.function_type})"

    def __str__(self):
        return repr(self)

    def set_address(self, address):
        self._address = address

    def address(self):
        return self.address

    @property
    def dtype_ctype(self):
        return GetDataTypeCType(self.dtype)

    @property
    def read_code(self):
        if self.function_type == FunctionType.kHolding:
            return 3
        return 4

    @property
    def write_code(self):
        if self.function_type == FunctionType.kHolding:
            return 16
        else:
            assert(0)

    @property
    def memory_code(self):
        return self.function_type.value


class Slave:
    def __init__(self, address):
        self.address = address
