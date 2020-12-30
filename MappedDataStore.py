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

class MapEntry:
    def __init__(self, name, dtype, length, function_type):
        self.name = name
        self.dtype = dtype
        self.length = length + (GetDataTypeSize(dtype) * length) % GetDataTypeSize(DataType.uint16_t)
        registers = float(GetDataTypeSize(dtype) * length) / GetDataTypeSize(DataType.uint16_t)
        self.registers = int(math.ceil(registers))
        assert((self.length * GetDataTypeSize(dtype)) % GetDataTypeSize(DataType.uint16_t) == 0)
        self.address = 0
        self.function_type = function_type
        assert(self.registers > 0)
        assert(type(self.name) is str)
        assert(type(self.dtype) is DataType)
        assert(type(self.length) is int)
        assert(type(self.function_type) is FunctionType)
        assert(self.length >= 1)

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

class WindLDREntry():
    def __init__(self, map_entry, slave):
        self.map_entry = map_entry
        self.plc_address = 0
        self.slave = slave

    @property
    def functions(self):
        if self.function_type == FunctionType.kHolding:
            return [self.map_entry.read_code, self.map_entry.write_code]
        return [self.map_entry.read_code]

    @property
    def name(self):
        return self.map_entry.name

    @property
    def dtype(self):
        return self.map_entry.dtype

    @property
    def length(self):
        return self.map_entry.length

    @property
    def registers(self):
        return self.map_entry.registers

    @property
    def address(self):
        return self.map_entry.address

    @property
    def function_type(self):
        return self.map_entry.function_type

    @property
    def memory_code(self):
        return self.map_entry.memory_code

    @property
    def plc_variable_name(self):
        max_length = 20
        append = ""
        if self.registers > 1:
            append += "_%d"%(self.registers - 1)
        append += "_%d"%0xff
        name = self.name

        if len(append) + len(self.name) > max_length:
            split = self.name.split("_")
            if len(split) > 2:
                name = "_".join(split[1:])

        return name[:max_length-len(append)]

class Slave:
    def __init__(self, address):
        self.address = address

def MakeHeader(template_directory, entries, fname, namespace):
    env = Environment(loader=FileSystemLoader(template_directory))
    data_store_template = "MappedDataStore.h.j2"
    template = env.get_template(data_store_template)
    rendering = template.render(entries=entries, namespace=namespace, fname=fname, timestamp=datetime.datetime.now())
    with open(fname, 'w') as f:
        f.write(rendering)
    os.system("clang-format %s -i --style=Google"%fname)

def MakeMap(template_directory, entries, fname, title):
    env = Environment(loader=FileSystemLoader(template_directory))
    register_map_template = "RegisterMap.md.j2"
    template = env.get_template(register_map_template)
    rendering = template.render(entries=entries, title=title)
    with open(fname, 'w') as f:
        f.write(rendering)

def MakeWindLDRConfig(template_directory, entries, fname):
    master_address = 0
    env = Environment(loader=FileSystemLoader(template_directory))
    for register_map_template in ("WindLDRConfiguration.csv.j2", "WindLDRTagEditor.csv.j2"):
        template = env.get_template(register_map_template)
        rendering = template.render(entries=entries, master_address=master_address)
        with open(register_map_template.strip('.j2'), 'w') as f:
            f.write(rendering)

def MakePyModbusTest(template_directory, input_registers, holding_registers, includes):
    env = Environment(loader=FileSystemLoader(template_directory))
    register_map_template = "PyModbusTestMaster.py.j2"
    fname = register_map_template.strip(".j2")
    template = env.get_template(register_map_template)
    rendering = template.render(input_registers=input_registers, holding_registers=holding_registers, includes=includes)
    with open(fname, 'w') as f:
        f.write(rendering)


def MakeLibModbusTest(template_directory, input_registers, holding_registers, includes):
    env = Environment(loader=FileSystemLoader(template_directory))
    register_map_template = "LibModbusTestMaster.cpp.j2"
    fname = register_map_template.strip(".j2")
    template = env.get_template(register_map_template)
    rendering = template.render(input_registers=input_registers, holding_registers=holding_registers, includes=includes)
    with open(fname, 'w') as f:
        f.write(rendering)

def MakeModbusTest(template_directory, input_registers, holding_registers, includes):
    MakePyModbusTest(template_directory, input_registers, holding_registers, includes)
    MakeLibModbusTest(template_directory, input_registers, holding_registers, includes)

