#pragma once

#include <stdint.h>

void sha256_parallel4(uint8_t s[4][6], uint8_t result[4][32]);
