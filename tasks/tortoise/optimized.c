#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "sha256.h"

char ucDataBlock[60] = {
    // Offset 0x00000000 to 0x00000033
    '\x86', '\x77', '\x1E', '\x97', '\x0A', '\xF7', '\xFB', '\x30', '\xD9',
    '\x2B', '\xF0', '\x00', '\xD8', '\x41', '\xBB', '\x93', '\x65', '\x50',
    '\xCC', '\x8F', '\x4C', '\x85', '\x9F', '\x1D', '\xC3', '\x5E', '\x16',
    '\x3A', '\x28', '\xDB', '\xE7', '\x37', '\xF6', '\x1B', '\xC7', '\xD9',
    '\xF9', '\xC0', '\x48', '\xCE', '\x4C', '\x4C', '\xDA', '\xE1', '\xB2',
    '\x8C', '\x99', '\x3F', '\xB7', '\xD4', '\x08', '\x16', '\x00', '\x00',
    '\x00', '\x00', '\x00', '\x00', '\x00', '\x00'};
static char state[] = "\x6a\x09\xe6\xbb\x67\xae\x3c\x6e\xf3\xa5\x4f\xf5";
uint16_t blockmod4 = 0;

#include <openssl/sha.h>
void sha256(char *data, char *out) {
  unsigned char hash[SHA256_DIGEST_LENGTH];
  SHA256_CTX sha256;
  SHA256_Init(&sha256);
  SHA256_Update(&sha256, data, 6);
  SHA256_Final(hash, &sha256);
  for (int i = 0; i < 3; i++) {
    out[i] = (char)hash[i];
  }
}

void update(char *buf, int64_t count) {
  for (int64_t i = 0; i < count; i++) {
    uint8_t data[4][6];
    for (int j = 0; j < 4; j++) {
      data[j][0] = state[j * 3];
      data[j][1] = state[j * 3 + 1];
      data[j][2] = state[j * 3 + 2];
      data[j][3] = buf[j * 3];
      data[j][4] = buf[j * 3 + 1];
      data[j][5] = buf[j * 3 + 2];
    }
    uint8_t result[4][32];
    sha256_parallel4(data, result);
    for (int j = 0; j < 4; j++) {
      memcpy(state + j * 3, result[j], 3);
    }
  }
}

uint32_t swapByteOrder(uint32_t ui) {
  return (ui & 0x0000FF00) | ((ui >> 16) & 0x000000FF) |
         ((ui << 16) & 0x00FF0000);
}

void crypt(char *stream, char *password) {
  for (uint16_t i = 0; i < 52; i++) {
    update(password, pow(i, 6));
    char state_copy[13];
    state_copy[12] = '\0';
    strcpy(state_copy, state);
    char data[6];
    data[0] = state[0];
    data[1] = state[1];
    data[2] = state[2];
    data[3] = 0;
    data[4] = 0;
    data[5] = 0;
    sha256(data, state);

    uint32_t x1 = swapByteOrder(*(uint32_t *)state),
             x2 = swapByteOrder(*(uint32_t *)(state + 3)),
             x3 = swapByteOrder(*(uint32_t *)(state + 6)),
             x4 = swapByteOrder(*(uint32_t *)(state + 9));
    x2 ^= x1;
    x3 ^= x2;
    x4 ^= x3;
    // cout << hex << x1 << ' ' << x2 << ' ' << x3 << ' ' << x4 << ' ' << ((((x1
    // & 0x00ff0000) >> 16) + ((x1 & 0x0000ff00) >> 8) + (x1 & 0x000000ff)) +
    // (((x2 & 0x00ff0000) >> 16) + ((x2 & 0x0000ff00) >> 8) + (x2 &
    // 0x000000ff)) + (((x3 & 0x00ff0000) >> 16) + ((x3 & 0x0000ff00) >> 8) +
    // (x3 & 0x000000ff)) + (((x4 & 0x00ff0000) >> 16) + ((x4 & 0x0000ff00) >>
    // 8) + (x4 & 0x000000ff))) << endl; exit(0);
    uint32_t temp = ((((x1 & 0x00ff0000) >> 16) + ((x1 & 0x0000ff00) >> 8) +
                      (x1 & 0x000000ff)) +
                     (((x2 & 0x00ff0000) >> 16) + ((x2 & 0x0000ff00) >> 8) +
                      (x2 & 0x000000ff)) +
                     (((x3 & 0x00ff0000) >> 16) + ((x3 & 0x0000ff00) >> 8) +
                      (x3 & 0x000000ff)) +
                     (((x4 & 0x00ff0000) >> 16) + ((x4 & 0x0000ff00) >> 8) +
                      (x4 & 0x000000ff)));
    printf("%c\n", (char)(stream[i] ^ (char)(temp % 255)));
    strcpy(state, state_copy);
  }
}

int main() { crypt(ucDataBlock, "sEkVqGKOrBdl"); }
