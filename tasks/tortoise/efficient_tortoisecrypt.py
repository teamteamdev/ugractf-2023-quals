import hashlib
import base64
import time
import sys


STATES0 = [b"\x6a\x09\xe6", b"\xbb\x67\xae", b"\x3c\x6e\xf3", b"\xa5\x4f\xf5"]


def iterate(state, block):
    return hashlib.sha256(state + block).digest()[:3]


def stream_state(state, block):
    seen = {}
    prefix = []
    while state not in seen:
        seen[state] = len(prefix)
        prefix.append(state)
        state = iterate(state, block)
    loop_start = seen[state]
    loop_len = len(prefix) - loop_start

    def at(pos):
        if pos >= len(prefix):
            pos = (pos - loop_start) % loop_len + loop_start
        return prefix[pos]

    i = 0
    tot = 0
    while True:
        tot += i ** 6
        yield at(tot)
        i += 1


def unite(states):
    states = states[:]
    states[0] = iterate(states[0], b"\x00\x00\x00")
    for i in range(1, 4):
        states[i] = bytes([a ^ b for a, b in zip(states[i], states[i - 1])])
    return b"".join(states)


def crypt(stream, password):
    orig_len = len(stream)
    stream += b"\x00" * (-len(stream) % 12)

    state_streams = [stream_state(state, password[i * 3:(i + 1) * 3]) for i, state in enumerate(STATES0)]
    for i in range(orig_len):
        hsh = sum(unite([next(stream) for stream in state_streams])) % 255
        decch = stream[i] ^ hsh
        yield decch


if __name__ == "__main__":
    encrypting = input("Encrypting or decrypting? [e/d] ") == "e"

    if encrypting:
        sys.stderr.write("Text: ")
        data = input().encode()
    else:
        sys.stderr.write("Ciphertext (base64): ")
        data = base64.b64decode(input())

    sys.stderr.write("Password (12 characters): ")
    password = input().encode()

    stream = crypt(data, password)

    if encrypting:
        while True:
            chars = []
            try:
                chars.append(next(stream))
                chars.append(next(stream))
                chars.append(next(stream))
            except StopIteration:
                pass
            if not chars:
                break
            sys.stdout.buffer.write(base64.b64encode(bytes(chars)))
            sys.stdout.buffer.flush()
    else:
        for ch in stream:
            sys.stdout.buffer.write(bytes([ch]))
            sys.stdout.buffer.flush()

    sys.stdout.buffer.write(b"\n")
    sys.stdout.buffer.flush()
