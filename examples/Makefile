all:
	python3 BasicRegisterMapping.py 
	make fbs

fbs:
	../../../flatbuffers/flatc --cpp --grpc --cpp-std=c++17 --cpp-ptr-type naked --gen-mutable --scoped-enums --gen-name-strings --cpp-static-reflection --gen-object-api *.fbs 

clean:
	rm HoldingRegisterMappedDataStore.fbs  PyModbusTestMaster.py HoldingRegisterMappedDataStore.h    WindLDRConfiguration.csv HoldingRegisterMappedDataStore.md   WindLDRTagEditor.csv InputRegisterMappedDataStore.h InputRegisterMappedDataStore.md LibModbusTestMaster.cpp HoldingRegisterMappedDataStore_generated.h

