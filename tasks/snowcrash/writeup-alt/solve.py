# Нам понадобятся только то, что отвечает за конечное поле, за матрицы (конкректно - за единичную матрицу) и за вектор
from sage.all import GF, identity_matrix, vector

F = GF(2)  # Все вычисления для битов будут происходить в конечно поле GF(2)

# Массив result можно выдернуть из декомпилированной программы (но конкретно такой вид я нашёл, используя wasm2c)
result = [0x44, 0x60, 0x69, 0x41, 0x7e, 0x6c, 0x74, 0x5d, 0x76, 0x30, 0x0a, 0x6f,
          0x53, 0x20, 0x51, 0x03, 0x68, 0x6d, 0x5c, 0x5c, 0x71, 0x3f, 0x4b, 0x2e,
          0x36, 0x1c, 0x4c, 0x37, 0x24, 0x0b, 0x18, 0x3e, 0x49, 0x1f, 0x6a, 0x1c,
          0x35, 0x06, 0x2c, 0x20, 0x38, 0x51, 0x0d, 0x1b, 0x3c, 0x70, 0x0a, 0x6c,
          0x56, 0x11, 0x1a, 0x28, 0x17, 0x22, 0x07, 0x39, 0x09, 0x16, 0x10, 0x28,
          0x0b, 0x43, 0x1c, 0x46, 0x30, 0x10, 0x24, 0x74, 0x52]

N = len(result)  # Длина флага


# Достаём все пары индексов из файла pairs.txt
def get_pairs():
    result = list()
    with open("pairs.txt") as rfile:
        for line in rfile.readlines():
            first, second = map(int, line.split())
            result.append((first, second))
    return result


# По парам строим матрицу коэффициентов
def get_coefficients(pairs):
    # coefficients - это матрица коэффициентов
    # coefficients[i][j] - это коэффициент перед j-й перменной в i-м уравнении
    # Изначально матрица коэффициентов - единичная матрица размера N*N
    coefficients = identity_matrix(F, N)
    for a, b in pairs:
        # Достаём из списка пару и прибавляем b-ю строку к a-й
        coefficients[a] += coefficients[b]

    return coefficients


# Получить список, в котором на i-й позиции будет бит result[i] под номером bit_idx
def get_result_ith_bit(bit_idx):
    # Вектор - это крутое математическое название для списка
    result_bits = vector(F, N)

    # Проходимся по списку result, зная для каждого байта его индекс
    for byte_idx, byte in enumerate(result):
        # Переводим байт в строку вида "01100001"
        byte_to_bin = bin(byte)[2:].zfill(8)
        # Достаём бит бод номером bit_idx и превращаем его в int
        bit = int(byte_to_bin[bit_idx])
        result_bits[byte_idx] = bit  # Присваиваем результат

    return result_bits


def main():
    pairs = get_pairs()  # Достаём пары
    coefficients = get_coefficients(pairs)  # Считаем коэффициенты

    flag = [0 for i in range(N)]  # Сюда мы будем писать флаг (как байты-числа)
    for bit_idx in range(8):  # Проходим по каждому номеру бита
        result_bit_idx_bits = get_result_ith_bit(
            bit_idx
        )  # Достаём список с битами результата

        # Решаем уравнение для коэффициентов и битов результата
        # Решение - биты флага
        solutions = coefficients.solve_right(result_bit_idx_bits)

        # Проходимся по каждому байту флага и приписываем бит
        for byte_idx, bit in enumerate(solutions):
            flag[byte_idx] *= 2
            flag[byte_idx] += int(bit)

    s_flag = bytes(flag).decode()
    print(s_flag)


if __name__ == "__main__":
    main()
