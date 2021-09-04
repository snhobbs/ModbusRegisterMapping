import configparser

def SetAddresses(entries):
    address = 0
    for entry in entries:
        if entry.dtype not in ['uint16', 'int16']:
            entry.address = address + address % 2
        else:
            entry.address = address
        address = entry.address + entry.registers

def get_dtype_size(dtype):
    if dtype in ["int8", "uint8", "string"]:
        return 1;
    if dtype in ["int16", "uint16"]:
        return 2;
    if dtype in ["int32", "uint32"]:
        return 4;
    if dtype in ["int64", "uint64"]:
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

class Entry:
    def __init__(self, name, dtype, length, function, address=0):
        self.name = name
        self.dtype = dtype
        self.length = int(length)
        self.function = function
        self.address = address

    @property
    def function_type(self):
        return self.function

    @property
    def registers(self):
        entry_size = get_dtype_size(self.dtype)*self.length
        return entry_size//2 + entry_size%2

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
