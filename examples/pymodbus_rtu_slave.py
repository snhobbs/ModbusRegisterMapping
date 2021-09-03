#!/usr/bin/env python
"""
Pymodbus Asynchronous Server Example
--------------------------------------------------------------------------

The asynchronous server is a high performance implementation using the
twisted library as its backend.  This allows it to scale to many thousands
of nodes which can be helpful for testing monitoring software.
"""
# --------------------------------------------------------------------------- #
# import the various server implementations
# --------------------------------------------------------------------------- #
from pymodbus.server.asynchronous import StartTcpServer
from pymodbus.server.asynchronous import StartUdpServer
from pymodbus.server.asynchronous import StartSerialServer

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSparseDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import (ModbusRtuFramer,
                                  ModbusAsciiFramer,
                                  ModbusBinaryFramer)
import sys
from modbus_server_objects import modbus_entries
# --------------------------------------------------------------------------- #
# configure the service logging
# --------------------------------------------------------------------------- #
import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

class StrictDataBlock(ModbusSparseDataBlock):
    def __init__(self, *args, **kwargs):
        self.entries = kwargs.pop("entries")
        d = {}
        for p in self.entries:
            for i in range(p.registers):
                d[p.address+i] = 0
        #d[max(d.keys())+1] = 0
        args = list(args)
        args.append(d)
        super().__init__(*args, **kwargs)
        self.address = 1

    def validate(self, address, count=1):
        print("Validate", address, count)
        return super().validate(address, count)
'''
        offset_address = address-1

        for e in self.entries:
            if offset_address == e.address:
                if count <= e.registers:
                    return True
                print("Invalid", count, "!=", e.registers)
                return False
        print("Invalid Address not found", offset_address)
        return False

    def getValues(self, address, count=1):
        offset_address = address-1
        assert self.validate(address, count)
        i=0
        #for e in self.entries:
        #    if e.address==offset_address:
        #        assert count == e.registers
        return [self.values[p+offset_address] for p in range(count)]
        #return super().getValues(address, count)
'''

def run_async_server(port, address, baud):
    # ----------------------------------------------------------------------- #
    # initialize your data store
    # ----------------------------------------------------------------------- #
    # The datastores only respond to the addresses that they are initialized to
    # Therefore, if you initialize a DataBlock to addresses from 0x00 to 0xFF,
    # a request to 0x100 will respond with an invalid address exception.
    # This is because many devices exhibit this kind of behavior (but not all)
    #
    #     block = ModbusSequentialDataBlock(0x00, [0]*0xff)
    #
    # Continuing, you can choose to use a sequential or a sparse DataBlock in
    # your data context.  The difference is that the sequential has no gaps in
    # the data while the sparse can. Once again, there are devices that exhibit
    # both forms of behavior::
    #
    #     block = ModbusSparseDataBlock({0x00: 0, 0x05: 1})
    #     block = ModbusSequentialDataBlock(0x00, [0]*5)
    #
    # Alternately, you can use the factory methods to initialize the DataBlocks
    # or simply do not pass them to have them initialized to 0x00 on the full
    # address range::
    #
    #     store = ModbusSlaveContext(di = ModbusSequentialDataBlock.create())
    #     store = ModbusSlaveContext()
    #
    # Finally, you are allowed to use the same DataBlock reference for every
    # table or you you may use a seperate DataBlock for each table.
    # This depends if you would like functions to be able to access and modify
    # the same data or not::
    #
    #     block = ModbusSequentialDataBlock(0x00, [0]*0xff)
    #     store = ModbusSlaveContext(di=block, co=block, hr=block, ir=block)
    #
    # The server then makes use of a server context that allows the server to
    # respond with different slave contexts for different unit ids. By default
    # it will return the same context for every unit id supplied (broadcast
    # mode).
    # However, this can be overloaded by setting the single flag to False
    # and then supplying a dictionary of unit id to context mapping::
    #
    #     slaves  = {
    #         0x01: ModbusSlaveContext(...),
    #         0x02: ModbusSlaveContext(...),
    #         0x03: ModbusSlaveContext(...),
    #     }
    #     context = ModbusServerContext(slaves=slaves, single=False)
    #
    # The slave context can also be initialized in zero_mode which means that a
    # request to address(0-7) will map to the address (0-7). The default is
    # False which is based on section 4.4 of the specification, so address(0-7)
    # will map to (1-8)::
    #
    #     store = ModbusSlaveContext(..., zero_mode=True)
    # ----------------------------------------------------------------------- #

    holding_registers = [r for r in modbus_entries if r.type=="holding register"]
    input_registers = [r for r in modbus_entries if r.type=="input register"]

    #hr_dict = [0]*1024
    #ir_dict = [0]*1024
    hr = StrictDataBlock(entries=holding_registers)
    ir = StrictDataBlock(entries=input_registers)

    for pt in holding_registers:
        assert hr.validate(pt.address, pt.registers)
        print(hr.getValues(pt.address, pt.registers))

    for pt in input_registers:
        assert ir.validate(pt.address, pt.registers)
        print(ir.getValues(pt.address, pt.registers))
    #ir=ModbusSequentialDataBlock(0, ir_dict)
    #hr=ModbusSequentialDataBlock(0, hr_dict)


    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [17]*1),
        co=ModbusSequentialDataBlock(0, [17]*1),
        hr=hr,
        ir=ir
    )
    context = ModbusServerContext(slaves={address: store}, single = False)

    # ----------------------------------------------------------------------- #
    # initialize the server information
    # ----------------------------------------------------------------------- #
    # If you don't set this or any fields, they are defaulted to empty strings.
    # ----------------------------------------------------------------------- #
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/bashwork/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = '2.3.0'

    # ----------------------------------------------------------------------- #
    # run the server you want
    # ----------------------------------------------------------------------- #

    # TCP Server

    #StartTcpServer(context, identity=identity, address=("localhost", 5020),
    #               custom_functions=[CustomModbusRequest])

    # TCP Server with deferred reactor run

    # from twisted.internet import reactor
    # StartTcpServer(context, identity=identity, address=("localhost", 5020),
    #                defer_reactor_run=True)
    # reactor.run()

    # Server with RTU framer
    # StartTcpServer(context, identity=identity, address=("localhost", 5020),
    #                framer=ModbusRtuFramer)

    # UDP Server
    # StartUdpServer(context, identity=identity, address=("127.0.0.1", 5020))

    # RTU Server
    StartSerialServer(context, identity=identity,
                       port=port, framer=ModbusRtuFramer, baud=baud)

    # ASCII Server
    # StartSerialServer(context, identity=identity,
    #                   port='/dev/ttyp0', framer=ModbusAsciiFramer)

    # Binary Server
    # StartSerialServer(context, identity=identity,
    #                   port='/dev/ttyp0', framer=ModbusBinaryFramer)


if __name__ == "__main__":
    run_async_server(sys.argv[1], 246, 9600)

