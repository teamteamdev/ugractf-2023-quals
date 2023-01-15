#include <arpa/inet.h>
#include <assert.h>
#include <immintrin.h>
#include <stdint.h>
#include <string.h>

#pragma GCC diagnostic ignored "-Wincompatible-pointer-types"

#define AVXROR(x, y)                                                           \
  _mm_or_si128(_mm_srli_epi32((x), (y)), _mm_slli_epi32((x), 32 - (y)))

static uint32_t digest[8] = {0x6A09E667U, 0xBB67AE85U, 0x3C6EF372U,
                             0xA54FF53AU, 0x510E527FU, 0x9B05688CU,
                             0x1F83D9ABU, 0x5BE0CD19U};
static uint32_t constants[64] = {
    0x428a2f98U, 0x71374491U, 0xb5c0fbcfU, 0xe9b5dba5U, 0x3956c25bU,
    0x59f111f1U, 0x923f82a4U, 0xab1c5ed5U, 0xd807aa98U, 0x12835b01U,
    0x243185beU, 0x550c7dc3U, 0x72be5d74U, 0x80deb1feU, 0x9bdc06a7U,
    0xc19bf174U, 0xe49b69c1U, 0xefbe4786U, 0x0fc19dc6U, 0x240ca1ccU,
    0x2de92c6fU, 0x4a7484aaU, 0x5cb0a9dcU, 0x76f988daU, 0x983e5152U,
    0xa831c66dU, 0xb00327c8U, 0xbf597fc7U, 0xc6e00bf3U, 0xd5a79147U,
    0x06ca6351U, 0x14292967U, 0x27b70a85U, 0x2e1b2138U, 0x4d2c6dfcU,
    0x53380d13U, 0x650a7354U, 0x766a0abbU, 0x81c2c92eU, 0x92722c85U,
    0xa2bfe8a1U, 0xa81a664bU, 0xc24b8b70U, 0xc76c51a3U, 0xd192e819U,
    0xd6990624U, 0xf40e3585U, 0x106aa070U, 0x19a4c116U, 0x1e376c08U,
    0x2748774cU, 0x34b0bcb5U, 0x391c0cb3U, 0x4ed8aa4aU, 0x5b9cca4fU,
    0x682e6ff3U, 0x748f82eeU, 0x78a5636fU, 0x84c87814U, 0x8cc70208U,
    0x90befffaU, 0xa4506cebU, 0xbef9a3f7U, 0xc67178f2U};

#define RND(a, b, c, d, e, f, g, h, wki)                                       \
  {                                                                            \
    __m128i t0_128 = _mm_add_epi32(                                            \
        _mm_add_epi32(                                                         \
            _mm_xor_si128(_mm_xor_si128(AVXROR(e, 6), AVXROR(e, 11)),          \
                          AVXROR(e, 25)),                                      \
            h),                                                                \
        _mm_add_epi32(_mm_xor_si128(g, _mm_and_si128(e, _mm_xor_si128(f, g))), \
                      wki));                                                   \
    d = _mm_add_epi32(d, t0_128);                                              \
    h = _mm_add_epi32(                                                         \
        _mm_add_epi32(                                                         \
            _mm_xor_si128(_mm_xor_si128(AVXROR(a, 2), AVXROR(a, 13)),          \
                          AVXROR(a, 22)),                                      \
            t0_128),                                                           \
        _mm_or_si128(_mm_and_si128(_mm_or_si128(a, b), c),                     \
                     _mm_and_si128(a, b)));                                    \
  }

void sha256_parallel4(uint8_t s[4][6], uint8_t result[4][32]) {
  uint8_t d[4][64];
  memset(d, 0, sizeof(d));
  for (int i = 0; i < 4; i++) {
    memcpy(d[i], s[i], 6);
    d[i][6] = '\x80';
    ((uint32_t *)d[i])[15] = htonl(6 << 3);
  }

  __m128i w[64];
  for (int j = 0; j < 16; j++) {
    w[j] = _mm_i32gather_epi32(
        (uint32_t *)d + j, _mm_set_epi32(3 * 64, 2 * 64, 1 * 64, 0 * 64), 1);
  }
  for (int i = 0; i < 128; i++) {
    ((uint32_t *)w)[i] = ntohl(((uint32_t *)w)[i]);
  }

  for (int j = 16; j < 64; j++) {
    __m128i x15 = w[j - 15];
    __m128i x2 = w[j - 2];
    w[j] = _mm_add_epi32(
        _mm_add_epi32(
            _mm_xor_si128(_mm_xor_si128(AVXROR(x15, 7), AVXROR(x15, 18)),
                          _mm_srli_epi32(x15, 3)),
            w[j - 16]),
        _mm_add_epi32(
            _mm_xor_si128(_mm_xor_si128(AVXROR(x2, 17), AVXROR(x2, 19)),
                          _mm_srli_epi32(x2, 10)),
            w[j - 7]));
  }

  for (int j = 0; j < 64; j++) {
    _mm_storeu_si128(&w[j], _mm_add_epi32(_mm_load_si128(&w[j]),
                                          _mm_set1_epi32(constants[j])));
  }

  __m128i ss[8];
  for (int j = 0; j < 8; j++) {
    ss[j] = _mm_set1_epi32(digest[j]);
  }

  for (int i = 0; i < 8; i++) {
    RND(ss[0], ss[1], ss[2], ss[3], ss[4], ss[5], ss[6], ss[7], w[8 * i + 0]);
    RND(ss[7], ss[0], ss[1], ss[2], ss[3], ss[4], ss[5], ss[6], w[8 * i + 1]);
    RND(ss[6], ss[7], ss[0], ss[1], ss[2], ss[3], ss[4], ss[5], w[8 * i + 2]);
    RND(ss[5], ss[6], ss[7], ss[0], ss[1], ss[2], ss[3], ss[4], w[8 * i + 3]);
    RND(ss[4], ss[5], ss[6], ss[7], ss[0], ss[1], ss[2], ss[3], w[8 * i + 4]);
    RND(ss[3], ss[4], ss[5], ss[6], ss[7], ss[0], ss[1], ss[2], w[8 * i + 5]);
    RND(ss[2], ss[3], ss[4], ss[5], ss[6], ss[7], ss[0], ss[1], w[8 * i + 6]);
    RND(ss[1], ss[2], ss[3], ss[4], ss[5], ss[6], ss[7], ss[0], w[8 * i + 7]);
  }

  for (int j = 0; j < 8; j++) {
    uint32_t ss_raw[4];
    _mm_storeu_si128(ss_raw, ss[j]);
    for (int i = 0; i < 4; i++) {
      ((uint32_t *)result[i])[j] = htonl(digest[j] + ss_raw[i]);
    }
  }
}