#pragma once
#include <cstdint>
#include <algorithm>
#include <array>
#include <cstdint>
#include <string>

struct ModbusEntry {
  std::string name_;
  std::string dtype_;
  size_t address_;
  size_t length_;
  size_t registers_;
  std::string type_;
};
