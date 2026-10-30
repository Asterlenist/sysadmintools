#include <cstdlib>
#include <iostream>
#include <random>
#include <string>
using namespace std;

std::string generate_password(int length, bool use_upper, bool use_lower,
                              bool use_digits, bool use_special) {
  const std::string uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  const std::string lowercase = "abcdefghijklmnopqrstuvwxyz";
  const std::string digits = "0123456789";
  const std::string special = "!@#$%^&*()_+-=[]{}|;:,.<>?";

  std::string charset = "";
  if (use_upper) charset += uppercase;
  if (use_lower) charset += lowercase;
  if (use_digits) charset += digits;
  if (use_special) charset += special;

  if (charset.empty()) {
    return "Error: No character set selected!";
  }

  std::random_device rd;
  std::mt19937 gen(rd());
  std::uniform_int_distribution<> dist(0, charset.length() - 1);

  std::string password = "";
  for (int i = 0; i < length; ++i) {
    password += charset[dist(gen)];
  }

  return password;
                              }

                              int main() {
                                int length = 16;
                                bool use_upper = true;
                                bool use_lower = true;
                                bool use_digits = true;
                                bool use_special = true;

                                std::cout << "Generated Password: " << generate_password(length, use_upper, use_lower, use_digits, use_special) << std::endl;

                                return 0;
                              }
