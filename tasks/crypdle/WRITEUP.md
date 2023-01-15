# Crypdle: Write-up

Нам дана программа с исходными кодами, которая просит пользователя ввести флаг и отвечает, на сколько процентов он корректен.

Все бы хорошо, но флаг проверяется на корректность каким-то нетривиальным методом.

Сначала проверяется длина флага:

```c
if (strlen(flag) != FLAG_LENGTH) {
  printf("Wrong flag length\n");
  continue;
}
```

Затем рассматриваются блоки из `WINDOW_SIZE` подряд идущих символов, каждый блок хешируется через MD5, и первый байт результата сравнивается с известным значением:

```c
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
```

Наконец, хешируется и проверяется весь флаг целиком:

```c
char flag_hash[MD5_DIGEST_LENGTH];
MD5(flag, FLAG_LENGTH, flag_hash);
if (memcmp(flag_hash, FLAG_MD5, MD5_DIGEST_LENGTH) == 0) {
  count++;
}
```

На первый взгляд кажется, что задача нерешаема, ведь используется хеширование, причем хешируются достаточно длинные строки, да и хешей много, поэтому коллизию подобрать сложнее, чем если бы хеш был один. Однако в криптографии больше хешей — не значит лучше: взлом одного из хешей уже дает информацию, которую можно использовать при взломе остальных.

Так и здесь: поверим, что флаг начинается с `ugra_`, и переберем следующие 3 символа среди цифр, подчеркивания и букв. Большую часть из этих строк можно сразу отбросить, если хеш первых 8 символов не совпадает с требуемым. После этого для каждой из оставшихся строк переберем 9-й символ, и также отбросим те, у которых хеш символов с 2-го по 9-й не совпадает с нужным, и так далее. В самом конце, если осталось несколько вариантов, можно либо попробовать загрузить в систему их все, либо выбрать тот, у которого полный хеш совпадает с `FLAG_MD5`.

На Python реализация выглядит так:

```python
def crack(prefix):
    if len(prefix) == FLAG_LENGTH:
        if FLAG_MD5 == list(hashlib.md5(prefix).digest()):
            print(prefix.decode())
        return

    for c in ALPHABET:
        s = prefix + bytes([ord(c)])
        if len(s) >= WINDOW_SIZE:
            cur = hashlib.md5(s[-WINDOW_SIZE:]).digest()[0]
            if cur == FLAG_WINDOW_MD5[len(s) - WINDOW_SIZE]:
                crack(s)
        else:
            crack(s)


crack(b"ugra_")
```

Полный код можно посмотреть в файле [solution.py](solution.py).

Флаг: **ugra_no_you_cant_replace_backend_with_crypto_06118ff6d838**
