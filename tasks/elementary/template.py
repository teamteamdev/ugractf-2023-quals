import base64
import hashlib
import sys


def abort():
    print("Wrong flag!")
    sys.exit(1)


flag = input()

if len(flag) != [[VALUE]]:
    abort()
if flag[17] != [[VALUE]]:
    abort()
if flag[:5] != [[VALUE]]:
    abort()
if flag[9:3:-2] != [[VALUE]]:
    abort()
if flag[-2:-15:-3].encode().hex() != [[VALUE]]:
    abort()
if int.from_bytes(flag[6:18:2].encode(), "little") != [[VALUE]]:
    abort()
if sum(ord(x) * 1000 ** i for i, x in enumerate(flag[19:-4])) != [[VALUE]]:
    abort()
if base64.b64encode(flag[-4:].encode()) != [[VALUE]]:
    abort()
if hashlib.sha256(flag.encode()).hexdigest() != [[VALUE]]:
    abort()

print("OK!")
