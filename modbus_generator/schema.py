import configparser
import numpy as np

def GetAddresses(entries, starting=0, alignment=4):
    addresses = []
    address = starting
    for entry in entries:
        if entry["data type"] not in ['uint16_t', 'int16_t']:
            current_address = int(address + address % (alignment//2))  # Only allow uint16s to be unaligned
        else:
            current_address = address
        addresses.append(int(address))
        address = current_address + entry["register count"]
    return np.array(addresses, dtype=int)


def get_dtype_size(dtype):
    if dtype in ["int8_t", "uint8_t", "string"]:
        return 1;
    if dtype in ["int16_t", "uint16_t"]:
        return 2;
    if dtype in ["int32_t", "uint32_t"]:
        return 4;
    if dtype in ["int64_t", "uint64_t"]:
        return 8;
    print(dtype)
    assert(0)


def make_variable_name(entry_name, registers, max_length=20):
    append = ""
    if registers > 1:
        append += "_%d"%(registers - 1)
    append += "_%d"%0xff

    name = entry_name
    if len(append) + len(entry_name) > max_length:
        split = entry_name.split("_")
        if len(split) > 2:
            name = "_".join(split[1:])

    return name[:max_length-len(append)]


def calculate_entry_registers(dtype, length):
    entry_size = get_dtype_size(dtype)*length
    return int(entry_size//2 + entry_size % 2)


class Entry:
    def __init__(self, name, dtype, length, function, address=0):
        self.name = name
        self.dtype = dtype
        self.length = int(length)
        self.type = function
        self.address = address

    @property
    def function_type(self):
        return self.type

    @property
    def registers(self):
        return calculate_entry_registers(self.dtype, self.length)

    @property
    def plc_variable_name(self):
        return make_variable_name(self.name, self.registers, 20)

def parse_register_section(section):
    entries = []
    for option, arg in section.items():
        try:
            dtype, length = arg.strip(',').split(',')
            entries.append(Register(option, dtype, length))
        except (TypeError, IndexError, ValueError):
            print("Error with option '%s' (%s)"%(option, arg))
    SetAddresses(entries)
    return entries


class Schema:
    def __init__(self, holding_registers, input_registers, coils=None, discrete_inputs=None):
        self.holding_registers = holding_registers
        self.input_registers = input_registers
        self.coils = coils
        self.discrete_inputs = discrete_inputs

    @classmethod
    def read(cls, string):
        config = configparser.ConfigParser()
        config.read_string(string)
        holding_registers = []
        if "holding registers" in config:
            holding_registers = parse_register_section(config["holding registers"])
        input_registers = []
        if "input registers" in config:
            input_registers = parse_register_section(config["input registers"])

        return Schema(holding_registers, input_registers,None,None)
