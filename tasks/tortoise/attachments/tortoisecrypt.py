import hashlib
import base64
import time
import sys


class Hash:
    def __init__(self, initial=b""):
        # sqrt(2 + i) fractional parts
        self.state = [b"\x6a\x09\xe6", b"\xbb\x67\xae", b"\x3c\x6e\xf3", b"\xa5\x4f\xf5"]
        self.pending = b""
        self.done = False
        self.blockmod4 = 0
        self.update(initial)


    def _update_block(self, block):
        old = self.state[self.blockmod4]
        self.state[self.blockmod4] = hashlib.sha256(old + block).digest()[:3]
        self.blockmod4 = (self.blockmod4 + 1) % 4


    def update(self, buf):
        if self.done:
            raise Error("Hash.digest was already called")
        self.pending += buf
        for i in range(0, len(self.pending) - 2, 3):
            self._update_block(self.pending[i:i + 3])
        self.pending = self.pending[len(self.pending) // 3 * 3:]


    def _inplace_digest(self):
        if self.done:
            raise Error("Hash.digest was already called")

        if self.pending:
            len_mod3 = len(self.pending)
            self.update(bytes([0] * (2 - len_mod3) + [len_mod3]))
        else:
            self.update(bytes([0, 0, 0]))
        assert not self.pending

        for i in range(1, 4):
            self.state[i] = bytes([a ^ b for a, b in zip(self.state[i], self.state[i - 1])])

        return b"".join(self.state)


    def copy(self):
        h = Hash()
        h.state = self.state[:]
        h.pending = self.pending
        h.done = self.done
        h.blockmod4 = self.blockmod4
        return h


    def digest(self):
        return self.copy()._inplace_digest()


def crypt(stream, password):
    orig_len = len(stream)
    stream += b"\x00" * (-len(stream) % 12)

    hsh = Hash()
    for i, ch in zip(range(orig_len), stream):
        hsh.update(password * i ** 6)
        decch = ch ^ sum(hsh.digest()) % 255
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
