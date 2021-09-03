# Modbus Register Mapping
This is a collection of jinja2 templates for auto generating all the code and documentation that a system needs.
When a change is made to to the interface all the documentation and interface code can be regenerated automatically.

Generates pymodbus, ModbusBasic, Libmodbus, and WindLDR modbus configuration data all from the same list of python objects.

- A modbus object needs:
  - Modbus Specific Data:
    - Starting address
    - Length
    - Type: input, coil, input register, holding register
  - Data Retrieval:
    - Data type

Using these objects requires attention to allignment, etc.
We would like to be able to work directly with the objects by name and/or enums

General Features:
  - Fields accessible as strings, enums, or offsets
  - Reads and writes cannot start or end in the middle of an entry
  - Use controllers for the registers and bit control
  - Passing the address and count to the corresponding controller responds with a true/false for validity
  - We can write and read the data through the proper data type

Entry
  - Use a CSV with the name, address, entry length, modbus type, data type, number of elements
  - If the address is and/or the entry length is blank then these will be autocalculated. Fixed values are to reproduce existing systems.

Python
  - Class with all the CSV data.
  - Lookups are done by iterating over a list of these objects
  - Each are in a different module

C++
  - Use a namespace with namespaces.
  - Generate enums for each entry
  - Generate list of offsets indexed by enum value, iterate over these for the start and end
  - Generate list of names indexed by enum
  - Offset to enum switch statement
  - Data is stored in namespace
  - Switch statement for read and write data to byte arrays
