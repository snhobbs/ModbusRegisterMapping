//#include <Modbus/Utilities.h>
//#include <Modbus/MappedRegisterDataStore.h>
#include <Modbus/Modbus.h>
#include <Modbus/ModbusRtu/ModbusRtuSlave.h>
#include <Modbus/MappedRegisterDataStore.h>
#include <Modbus/DataStore.h>

#include <modbus.h>
#include <cassert>
#include <iostream>
#include <array>
#include <string>
#include <cstdio>
#include <cerrno>
#include <cstdint>
#include <unistd.h>
#include <cstring>
#include <string>
#include <vector>
#include <modbus_basic_server_holding_register.h>
#include <modbus_basic_server_input_register.h>

using namespace Modbus;

template<typename T>
void PrintArray(const T& t) {
  for (auto pt : t) {
    std::cout << static_cast<int>(pt) << ",";
  }
  std::cout << std::endl;
}

struct ModbusEntry {
  std::string name_;
  std::string dtype_;
  std::string type_;
  size_t length_;
  size_t address_;
  size_t registers_;

  ModbusEntry(std::string name, std::string dtype, std::string type, size_t length, size_t address, size_t registers):
  name_{name}, dtype_{dtype}, type_{type}, length_{length}, address_{address}, registers_{registers}
  {}
};


int ReadPrint(modbus_t* modbus_ctx, const int kAddressStart, int cnt) {
  std::vector<uint16_t> reg{cnt, 0};
  assert(cnt <= reg.size());
  int rc = modbus_read_registers(modbus_ctx, kAddressStart, reg.size(), reg.data());
  if(rc == -1) {
    fprintf(stderr, "Read Error %s\n", modbus_strerror(errno));
    return -1;
  }
  assert(rc == cnt);
  PrintArray(reg);
  return 0;
}

inline int ConnectRtu(modbus_t** modbus_ctx, const char* dev_name, const std::size_t baudrate = 9600) {
  *modbus_ctx = modbus_new_rtu(dev_name, baudrate, 'N', 8, 1);
  return 0;
}

using HoldingRegistersWrapper = ModbusBasic_holding_register::Wrapper; 
using InputRegistersWrapper = ModbusBasic_input_register::Wrapper; 

using HoldingRegisters = ModbusBasic_holding_register::holding_register; 
using InputRegisters = ModbusBasic_input_register::input_register; 

static modbus_t *ctx = nullptr;


void ReadWriteEntries(modbus_t* modbus_ctx, const ModbusEntry& entry) {
    std::cout << "Reading " << entry.name_ << std::endl;

#if 1
    //sleep(1);
    if (entry.type_ == "input register") {
      std::vector<uint16_t> buffer(entry.registers_, 0);
      assert(entry.registers_ <= buffer.size());
      modbus_read_input_registers(modbus_ctx, entry.address_, buffer.size(), buffer.data());  
      //inregs.SetFieldFromAddress(entry.address_, ArrayView<const uint8_t>(u8array.size(), u8array.data()));
      //const auto value = inregs_wrapper.get_{{ entry['name'] }}();
      //std::cout << value << std::endl;
    }
#else
    if (0){}
#endif
#if 1
    else if (entry.type_ == "holding register") {
      std::vector<uint16_t> buffer(entry.registers_, 0);
      size_t i = 0;
      for (auto& pt : buffer) {
        pt = 0xffff - i;
        i++;
      }
      modbus_write_registers(modbus_ctx, entry.address_, entry.registers_, buffer.data());
      ReadPrint(modbus_ctx, entry.address_, entry.registers_);
      //sleep(1);

      //Modbus::MakeRegistersToBytes(read_buffer, ArrayView<uint8_t>(u8array.size(), u8array.data()));
    }
#endif
}

int main(int argc, char** argv) {
  HoldingRegistersWrapper* holding_register_data_map_;
  Modbus::MappedRegisterDataStore<HoldingRegistersWrapper> holding_register_data_store_{holding_register_data_map_};
  HoldingRegisterController< Modbus::MappedRegisterDataStore<HoldingRegistersWrapper> > holding_registers_{&holding_register_data_store_};

  InputRegistersWrapper* input_register_data_map_;
  Modbus::MappedRegisterDataStore<InputRegistersWrapper> input_register_data_store_{input_register_data_map_};
  InputRegisterController< Modbus::MappedRegisterDataStore<InputRegistersWrapper> >input_registers_{&input_register_data_store_};

  const char* dev_name = nullptr;
  uint8_t slave_address = 246;
  if(argc > 1) {
    dev_name = argv[1];
    if(argc > 2) {
      slave_address = atoi(argv[2]);
    }
  }
  printf("Device: %s\n", dev_name);
  printf("Address: %u\n", slave_address);
  //  ConnectRtu(&ctx, DemoData::master_name);
  ConnectRtu(&ctx, dev_name);

  //Set the Modbus address of the remote slave
  modbus_set_slave(ctx, slave_address);//DemoData::slave_address);

  if (modbus_connect(ctx) == -1) {
    fprintf(stderr, "Connection failed: %s\n", modbus_strerror(errno));
    modbus_free(ctx);
    return -1;
  }
  modbus_set_debug(ctx, slave_address);


#ifdef MODBUS_TIMEVAL
  struct timeval response_timeout;
  modbus_get_response_timeout(ctx, &response_timeout);

  response_timeout.tv_sec = 1;
  response_timeout.tv_usec = 0;
  modbus_set_response_timeout(ctx, &response_timeout);
  modbus_set_byte_timeout(ctx, &response_timeout);
#else
  modbus_set_response_timeout(ctx, 1, 0);
  modbus_set_byte_timeout(ctx, 1, 0);
#endif
  
  printf("Connection Successful\n");
#if 0
  for (size_t i=0; i<holding_register_data_map_->names_.size(); i++) {
    const size_t registers = holding_register_data_map_->end_points_[i] - holding_register_data_map_->offsets_[i] + 1;
    ModbusEntry entry{holding_register_data_map_->names_[i], "int32_t", "holding register", 1, holding_register_data_map_->offsets_[i], registers};
    ReadWriteEntries(ctx, entry);
  };
#endif
  for (size_t i=0; i<input_register_data_map_->names_.size(); i++) {
    const size_t registers = input_register_data_map_->end_points_[i] - input_register_data_map_->offsets_[i] + 1;
    ModbusEntry entry{input_register_data_map_->names_[i], "int32_t", "input register", 1, input_register_data_map_->offsets_[i], registers};
    ReadWriteEntries(ctx, entry);
  };

 
  printf("Closing\n");
  modbus_close(ctx);
  printf("Freeing\n");
  modbus_free(ctx);
}
