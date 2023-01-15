#include <stdio.h>
#include <string.h>

#ifdef _WIN32
#include <windows.h>
#include <wincrypt.h>

#define MD5_DIGEST_LENGTH 16

void MD5(const char *data, int length, char *out) {
  static HCRYPTPROV hProv = 0;
  if (hProv == 0) {
    CryptAcquireContext(&hProv, NULL, NULL, PROV_RSA_FULL, CRYPT_VERIFYCONTEXT);
  }
  HCRYPTHASH hHash = 0;
  CryptCreateHash(hProv, CALG_MD5, 0, 0, &hHash);
  CryptHashData(hHash, data, length, 0);
  DWORD cbHash = MD5_DIGEST_LENGTH;
  CryptGetHashParam(hHash, HP_HASHVAL, out, &cbHash, 0);
  CryptDestroyHash(hHash);
}
#else
#include <openssl/md5.h>
#endif

const int MAX_FLAG_LENGTH = 128;

const int FLAG_LENGTH = [[FLAG_LENGTH]];
const int WINDOW_SIZE = [[WINDOW_SIZE]];
const char FLAG_MD5[] = {[[FLAG_MD5]]};
const char FLAG_WINDOW_MD5[] = {[[FLAG_WINDOW_MD5]]};

int main() {
  printf("Crypdle\n\n");

  for (;;) {
    char flag[MAX_FLAG_LENGTH];
    printf("Enter flag: ");
    fflush(stdout);
    fgets(flag, sizeof(flag), stdin);

    char* p = flag + strlen(flag);
    if(p != flag && *(p - 1) == '\n') {
      *(p - 1) = '\0';
    }

    if (strlen(flag) != FLAG_LENGTH) {
      printf("Wrong flag length\n");
      continue;
    }

    int count = 0;
    for (int i = 0; i < FLAG_LENGTH; i++) {
      char block[WINDOW_SIZE];
      for (int j = 0; j < WINDOW_SIZE; j++) {
        block[j] = flag[(i + j) % FLAG_LENGTH];
      }
      char block_hash[MD5_DIGEST_LENGTH];
      MD5(block, WINDOW_SIZE, block_hash);
      if (block_hash[0] == FLAG_WINDOW_MD5[i]) {
        count++;
      }
    }

    char flag_hash[MD5_DIGEST_LENGTH];
    MD5(flag, FLAG_LENGTH, flag_hash);
    if (memcmp(flag_hash, FLAG_MD5, MD5_DIGEST_LENGTH) == 0) {
      count++;
    }

    if (count == FLAG_LENGTH + 1) {
      printf("Nice flag!\n");
      return 0;
    } else {
      double percentage = 100 * count / (FLAG_LENGTH + 1);
      printf("This is not the right flag: you are %f%% correct\n", percentage);
    }
  }

  return 0;
}
