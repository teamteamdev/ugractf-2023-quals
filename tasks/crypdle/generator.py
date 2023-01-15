import hashlib
import os
import subprocess

from kyzylborda_lib.generator import get_attachments_dir
from kyzylborda_lib.secrets import get_flag


WINDOW_SIZE = 8


def generate():
    attachments_dir = get_attachments_dir()
    crypdle_c = os.path.join(attachments_dir, "crypdle.c")
    crypdle_elf = os.path.join(attachments_dir, "crypdle")
    crypdle_exe = os.path.join(attachments_dir, "crypdle.exe")

    flag_enc = get_flag().encode()
    flag_md5 = hashlib.md5(flag_enc).digest()
    flag_window_md5 = [hashlib.md5((flag_enc * 2)[i:i + WINDOW_SIZE]).digest()[0] for i in range(len(flag_enc))]

    with open("crypdle.c") as f:
        source_code = f.read()
    source_code = (
        source_code
            .replace("[[FLAG_LENGTH]]", str(len(flag_enc)))
            .replace("[[WINDOW_SIZE]]", str(WINDOW_SIZE))
            .replace("[[FLAG_MD5]]", ", ".join(map(str, flag_md5)))
            .replace("[[FLAG_WINDOW_MD5]]", ", ".join(map(str, flag_window_md5)))
    )
    with open(crypdle_c, "w") as f:
        f.write(source_code)

    subprocess.run(["gcc", crypdle_c, "-o", crypdle_elf, "-O2", "-lcrypto", "-static"], check=True)
    subprocess.run(["x86_64-w64-mingw32-gcc", crypdle_c, "-o", crypdle_exe, "-O2"], check=True)
