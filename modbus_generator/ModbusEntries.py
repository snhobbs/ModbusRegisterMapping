import os, sys, datetime, math
from enum import Enum, IntEnum


def GetDataTypeCType(dtype : str) -> str:
    if dtype == "string":
        return "uint8_t"
    return dtype + "_t"

def GetDataTypeSize(dtype: str) -> int:
    if dtype in ["string", "uint8", "int8"]:
        return 1
    elif dtype in ["uint16", "int16"]:
        return 2
    elif dtype in ["uint32", "int32"]:
        return 4
    elif dtype in ["uint64", "int64"]:
        return 8
    raise ValueError("Unknown dtype %s"%dtype)

def SetAddresses(entries):
    address = 0
    for entry in entries:
        if entry.dtype not in ["uint16","int16"]:
            entry.address = address + address % 2
        else:
            entry.address = address
        address = entry.address + entry.registers


#class FunctionType(IntEnum):
#    kInput = 3
#    kHolding = 4


class MapEntry:
    storage_type = "uint16"

    def __init__(self, name, dtype, count, function_type):
        self.name = name
        self.dtype = dtype
        self.count = int(count)
        self.function_type = function_type

        assert(self.registers > 0)
        assert(self.count >= 1)
        assert(self.storage_length >= 1)
        assert(self.function_type in ["input", "holding"])

        self._address = None

    def set_address(self, address):
        self._address = address

    def address(self):
        return self.address

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
        if self.function_type == "input":
            return 3
        return 4

    ''' Rounded up length to be integer multiple of storage type '''
    @property
    def storage_length(self):
        return int(math.ceil(float(GetDataTypeSize(self.dtype) * self.count) / GetDataTypeSize(self.storage_type)))

    @property
    def length(self):
        return self.count

    @property
    def registers(self):
        return self.storage_length


class Slave:
    def __init__(self, address):
        self.address = address
