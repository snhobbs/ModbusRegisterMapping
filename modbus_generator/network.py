import configparser
import csv

'''
A network description has a section for each configuration type with a value containing an array of the fields to use
the network section has the addresses and configuration names.

'''
def parse_csv(string):
    return [pt.strip() for pt in string.strip(",;{}()[]").strip().split(",") if len(pt.strip()) > 0]

class Configuration:
    def __init__(self, holding_registers_read=None, holding_registers_write=None, input_registers=None, coils=None, discrete_inputs=None):
        self.holding_registers_read=holding_registers_read
        self.holding_registers_write=holding_registers_write
        self.input_registers=input_registers
        self.coils=None
        self.discrete_inputs=None

    # sections is a dictionary with function name : {field0, field1...}
    @classmethod
    def load_from_section(cls, section):
        try:
            holding_registers_read = parse_csv(section["holding registers read"])
        except KeyError:
            holding_registers_read = []
        try:
            holding_registers_write = parse_csv(section["holding registers write"])
        except KeyError:
            holding_registers_write = []
        try:
            input_registers = parse_csv(section["input registers"])
        except KeyError:
            input_registers = []
        return Configuration(holding_registers_read=holding_registers_read, holding_registers_write=holding_registers_write, input_registers=input_registers)

class Network:
    def __init__(self, configurations, network):
        self.configurations = dict(configurations)
        self.network = network

    @classmethod
    def from_string(cls, string):
        config = configparser.ConfigParser()
        config.read_string(string)
        network = config["network"]

        # take unique values
        configurations = []
        for section in set(network.values()):
            configuration = Configuration.load_from_section(config[section])
            configurations.append((section, configuration))
            print(section)

        # load the configurations
        return Network(dict(configurations), network)

