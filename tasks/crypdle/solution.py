import hashlib


ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789_"


with open("crypdle.c") as f:
    source_code = f.read()

FLAG_LENGTH = int(source_code.partition(" FLAG_LENGTH = ")[2].partition(";")[0])
WINDOW_SIZE = int(source_code.partition(" WINDOW_SIZE = ")[2].partition(";")[0])
FLAG_MD5 = list(map(int, source_code.partition(" FLAG_MD5[] = {")[2].partition("};")[0].split(", ")))
FLAG_WINDOW_MD5 = list(map(int, source_code.partition(" FLAG_WINDOW_MD5[] = {")[2].partition("};")[0].split(", ")))


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
