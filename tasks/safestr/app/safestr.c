#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

struct SafeString {
  char *ptr;
  size_t size;
};

void set(struct SafeString s, size_t pos, char c) {
  if (pos >= 0 && pos < s.size) {
    s.ptr[pos] = c;
  }
}

void safeGets(struct SafeString s, size_t size) {
  for (size_t readed = 0; readed < size; readed++) {
    char c = fgetc(stdin);
    if (c == '\n') {
      set(s, readed, '\0');
      return;
    } else {
      set(s, readed, c);
    }
  }
  set(s, size, '\0');
}

void writeKey(struct SafeString s);

int main() {
  char *buf = (char *)malloc(512);
  struct SafeString s = {buf, 256};
  struct SafeString flag = {buf + s.size, 512 - s.size};
  writeKey(flag);

  size_t size = 0;
  printf("Enter input size: ");
  fflush(stdout);
  scanf("%lu", &size);
  fgetc(stdin); // skip newline
  if (size > s.size) {
    puts("Size is too big");
    return 0;
  }

  printf("Enter string: ");
  fflush(stdout);
  safeGets(s, size);

  printf("You entered: %s\n", s.ptr);
}

// --internal--

#include <string.h>
void writeKey(struct SafeString s) {
  char *flag = "\nBitcoin key is {{FLAG}}";
  strcpy(s.ptr, flag);
}
