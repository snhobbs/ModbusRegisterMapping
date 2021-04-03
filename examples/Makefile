all:
	modbus_generator -f demo.schema -p -l -m --md -t -w --windldr-offset=10 --libmodbus-includes "array.cpp"

pymodbus:
	modbus_generator -f demo.schema -p -t -m
	mv PyModbusTestMaster.py flatbuffers.fbs pymodbus
	cd pymodbus
	flatc -p flatbuffers.fbs

libmodbus:
	modbus_generator -f demo.schema -l
	mv LibModbusTestMaster.cpp libmodbus

clean:
	rm pymodbus/flatbuffers.fbs pymodbus/PyModbusTestMaster.py pymodbus/InputRegisters.py pymodbus/HoldingRegisters.py
	
