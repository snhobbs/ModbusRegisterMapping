import configparser
from . import ModbusRegister

def parse_register_section(section):
    entries = []
    for line in section:
        if len(line.strip() > 0):
            cols = line.split(',')
            if len(cols) < 3:
                print("Error in line '%s'"%line)
                continue
            name = cols[0]
            dtype = cols[1]
            length = cols[2]
            entries.append([name, dtype, int(length)])
    return entries


class Schema:
    def __init__(self, r_holding, r_input, coils=None, d_input=None):
        self.r_holding = r_holding
        self.r_input = r_input
        self.coils = coils
        self.d_input = d_input

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

if __name__ == "__main__":
    with open("demo.schema", "r") as f:
        Schema.read(f.read())
