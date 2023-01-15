code = "ANEcwu4fYegObF1i2VXyvJHxKd0qBkMl36ILRaUjPG8rToSZzpCDt7n9mWsh5Q"


def encode(n):
	if n == 0:
		return ""
	else:
		return code[n % len(code)] + encode(n // len(code))


def encrypt_flag(flag):
	numbers = []
	s = ""
	for i in range(len(flag)):
		numbers.append(ord(flag[i]))
		if i > 2:
			numbers[i] = (numbers[i] + numbers[i-1] + numbers[i-2]) % 179179
		if i > 0:
			s += "_"
		s += encode(numbers[i])
	return s
