import os, sys, datetime, math
from jinja2 import Template, Environment, FileSystemLoader
from enum import Enum, IntEnum
class DataType(Enum):
    uint8_t = 0
    int8_t = 1
    uint16_t = 2
    int16_t = 3
    uint32_t = 4
    int32_t = 5
    uint64_t = 6
    int64_t = 7
    kString = 8

def GetDataTypeCType(dtype):
    if dtype == DataType.kString:
        return DataType.uint8_t.name
    else:
        return dtype.name

def GetDataTypeSize(dtype):
    if dtype in [DataType.uint8_t, DataType.int8_t, DataType.kString]:
        return 1
    elif dtype in [DataType.uint16_t, DataType.int16_t]:
        return 2
    elif dtype in [DataType.uint32_t, DataType.int32_t]:
        return 4
    if dtype in [DataType.uint64_t, DataType.int64_t]:
        return 8

def SetAddresses(entries):
    address = 0
    for entry in entries:
        if entry.dtype not in [DataType.uint16_t, DataType.int16_t]:
            entry.address = address + address%2
        else:
            entry.address = address
        address = entry.address + entry.registers

class FunctionType(IntEnum):
    kInput = 3
    kHolding = 4

class ModbusRegister:
    def __init__(self, name, dtype, length, function_type):
        self.name = name
        self.dtype = dtype
        self.length = length + (GetDataTypeSize(dtype) * length) % GetDataTypeSize(DataType.uint16_t)
        registers = float(GetDataTypeSize(dtype) * length) / GetDataTypeSize(DataType.uint16_t)
        self.registers = int(math.ceil(registers))
        assert((self.length * GetDataTypeSize(dtype)) % GetDataTypeSize(DataType.uint16_t) == 0)
        self.function_type = function_type
        assert(self.registers > 0)
        assert(type(self.name) is str)
        assert(type(self.dtype) is DataType)
        assert(type(self.length) is int)
        assert(type(self.function_type) is FunctionType)
        assert(self.length >= 1)

class MapEntry:
    def __init__(self, register, address=0):
        self.register_ = register
        self.address = address
    @property
    def registers(self):
        return self.register_.registers

    @property
    def dtype(self):
        return self.register_.dtype

    @property
    def dtype_ctype(self):
        return GetDataTypeCType(self.register_.dtype)

    @property
    def read_code(self):
        if self.register_.function_type == FunctionType.kHolding:
            return 3
        return 4

    @property
    def write_code(self):
        if self.register_.function_type == FunctionType.kHolding:
            return 16
        else:
            assert(0)

    @property
    def memory_code(self):
        return self.register_.function_type.value

class Slave:
    def __init__(self, address):
        self.address = address

def MakeModbusTest(template_directory, input_registers, holding_registers, includes):
    MakePyModbusTest(template_directory, input_registers, holding_registers, includes)
    MakeLibModbusTest(template_directory, input_registers, holding_registers, includes)

