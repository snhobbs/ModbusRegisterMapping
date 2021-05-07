class Schema:
    def __init__(self, holding_registers, input_registers, coils=None, discrete_inputs=None):
        self.holding_registers = holding_registers
        self.input_registers = input_registers
        self.coils = coils
        self.discrete_inputs = discrete_inputs
