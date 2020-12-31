
# Input Register Map

| Entry |  Name  |  Data Type  |  Address | Register Count |
|-------|:------:|:-----------:|:--------:|:--------------:|
| 1.    | version | kString [64]   | 0x300000 | 32 |
| 2.    | firmware_version | kString [64]   | 0x300020 | 32 |
| 3.    | compile_date | kString [64]   | 0x300040 | 32 |
| 4.    | compile_time | kString [64]   | 0x300060 | 32 |
| 5.    | serial_number | kString [40]   | 0x300080 | 20 |
| 6.    | fault_status | uint16_t  | 0x300094 | 1 |
| 7.    | p5_micro_volts | int32_t  | 0x300096 | 2 |
| 8.    | p5_reading | uint32_t  | 0x300098 | 2 |
| 9.    | p23_micro_volts | int32_t  | 0x30009a | 2 |
| 10.    | p23_reading | uint32_t  | 0x30009c | 2 |
| 11.    | vlo_micro_volts | int32_t  | 0x30009e | 2 |
| 12.    | vlo_reading | uint32_t  | 0x3000a0 | 2 |
| 13.    | thermistor_temp_spi | int32_t  | 0x3000a2 | 2 |
| 14.    | thermistor_temp_mcu | int32_t  | 0x3000a4 | 2 |
| 15.    | data_frequency | uint32_t  | 0x3000a6 | 2 |
| 16.    | p3_3_micro_volts | int32_t  | 0x3000a8 | 2 |
| 17.    | p3_3_reading | uint32_t  | 0x3000aa | 2 |