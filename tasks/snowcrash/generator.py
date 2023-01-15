import subprocess

from kyzylborda_lib.generator import get_attachments_dir
from kyzylborda_lib.secrets import get_flag


STEPS = 1000


class PRNG:
    def __init__(self, seed: int):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 214013 + 2531011) & ((1 << 32) - 1)
        return (self.seed >> 16) & 0x7fff


def generate():
    flag = get_flag()

    prng = PRNG(1)
    data = list(flag.encode())
    for _ in range(STEPS):
        pos1 = 0
        pos2 = 0
        while pos1 == pos2:
            pos1 = prng.next() % len(flag)
            pos2 = prng.next() % len(flag)
        data[pos1] ^= data[pos2]

    with open("program.c") as f:
        program_source_code = f.read()
    program_source_code = program_source_code.replace("[[STEPS]]", f"{STEPS}")
    program_source_code = program_source_code.replace("[[DATA]]", ", ".join(map(str, data)))

    with open("/tmp/program.c", "w") as f:
        f.write(program_source_code)

    subprocess.run(["clang", "--sysroot=/usr/share/wasi-sysroot", "--target=wasm32-wasi", "/tmp/program.c", "-o", "/tmp/program.wasm", "-O1", "-Wl,--no-entry", "-nostdlib", "-ffreestanding"], check=True)

    with open("/tmp/program.wasm", "rb") as f:
        compiled_program = f.read()

    with open("program.html") as f:
        html_code = f.read()
    html_code = html_code.replace("[[WASM]]", ", ".join(map(str, compiled_program)))

    with open(get_attachments_dir() + "/program.html", "w") as f:
        f.write(html_code)
