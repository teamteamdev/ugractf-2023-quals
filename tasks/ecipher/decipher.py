import sys

def some_number(n):
    m = 2**32
    n0 = n % m
    n1 = (n0 ^ (n0 << 13)) % m
    n2 = (n1 ^ (n1 >> 17)) % m
    n3 = (n2 ^ (n2 << 5)) % m
    return n3

def decipher(data):
    n = len(data) // 2
    result = []
    for i in range(n):
        c = int(data[i*2:i*2+2], 16)
        result.append((c - n) % 256)
        n = some_number(n)
    return ''.join(chr(c) for c in result)

if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'rb') as f:
        data = f.read()
    print(decipher(data))
