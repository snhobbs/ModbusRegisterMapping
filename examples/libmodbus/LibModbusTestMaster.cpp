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
#include "./modbus_server_objects.h"
void print_response(const std::vector<uint16_t>& response, const std::string& dtype) {
  //std::cout << "print_response "<<dtype << std::endl;
  std::vector<uint8_t> bytes;
  for (auto& pt : response) {
    bytes.push_back(static_cast<uint8_t>(pt >> 8));
    bytes.push_back(static_cast<uint8_t>(pt&0xff));
  }
  if (dtype == "string") {
    std::cout << std::string(bytes.begin(), bytes.end()) << std::endl;
  } else if (dtype == "uint16_t") {
    std::cout << response[0] << std::endl;
  } else if (dtype == "int32_t" || dtype == "uint32_t") {

    uint32_t value = 0;
    for (auto& p: {0, 1, 2, 3}) {
      value <<= 8;
      value |= bytes[p];
    }
    if (dtype == "int32_t") {
      std::cout << static_cast<int32_t>(value) << std::endl;
    } else {
      std::cout << value << std::endl;
    }
  }
}


template<typename T>
void PrintArray(const T& t) {
  for (auto pt : t) {
    std::cout << static_cast<int>(pt) << ",";
  }
  std::cout << std::endl;
}

int ReadPrint(modbus_t* modbus_ctx, const int kAddressStart, int cnt, const ModbusEntry& entry) {
  std::vector<uint16_t> reg{cnt, 0};
  assert(cnt <= reg.size());
  int rc = modbus_read_registers(modbus_ctx, kAddressStart, reg.size(), reg.data());
  if(rc == -1) {
    fprintf(stderr, "Read Error %s\n", modbus_strerror(errno));
    return -1;
  }
  assert(rc == cnt);
  //PrintArray(reg);
  print_response(reg, entry.dtype_);
  return 0;
}

inline int ConnectRtu(modbus_t** modbus_ctx, const char* dev_name, const std::size_t baudrate = 9600) {
  *modbus_ctx = modbus_new_rtu(dev_name, baudrate, 'N', 8, 1);
  return 0;
}

static modbus_t *ctx = nullptr;


void ReadWriteEntries(modbus_t* modbus_ctx, const ModbusEntry& entry) {
    std::cout << "Reading " << entry.name_ << std::endl;

#if 1
    //sleep(1);
    if (entry.type_ == "input register") {
      std::vector<uint16_t> buffer(entry.registers_, 0);
      assert(entry.registers_ <= buffer.size());
      modbus_read_input_registers(modbus_ctx, entry.address_, buffer.size(), buffer.data());  
      print_response(buffer, entry.dtype_);
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
      //modbus_write_registers(modbus_ctx, entry.address_, entry.registers_, buffer.data());
      ReadPrint(modbus_ctx, entry.address_, entry.registers_, entry);
      //sleep(1);

    }
#endif
}

int main(int argc, char** argv) {
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
  //modbus_set_debug(ctx, slave_address);


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
  for (auto& pt : modbus_entries) {
    ReadWriteEntries(ctx, pt);
  }

  printf("Closing\n");
  modbus_close(ctx);
  printf("Freeing\n");
  modbus_free(ctx);
}
