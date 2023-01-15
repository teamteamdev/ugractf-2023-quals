# Состоняние генератора псевдослучайных чисел
randstate = 0


# Задать сид
def srand(a):
    global randstate
    randstate = a


# Вернуть случайное число
# Алгоритм взят из декомпилированного кода, единственное отличие -
# Берём всё по модулю pow(2, 32) (т.к. в коде используется 32-битный целочисленный тип данных int)
def rand():
    global randstate
    a = randstate * 214013 + 2531011
    randstate = a % pow(2, 32)
    return ((randstate >> 16) & 32767) % pow(2, 32)


# Основной код. Генерируем пары и записываем их в файл
def main():
    srand(1)
    pairs = list()  # Список пар индексов

    # В декомпилированном коде есть счётчик d, который считает пары
    # Когда d == 1000, цикл прерывается
    # Мы делаем то же самое, но без цикла
    while len(pairs) < 1000:
        # Генерируем два числа
        c = rand() % 69
        a = rand() % 69

        # Если совпали - не подходят
        if c == a:
            continue

        # Добавляем пару
        pairs.append((c, a))

    # Проходимся по всем парам и записываем в файл
    with open("pairs.txt", mode="w") as out_file:
        for pair in pairs:
            # Переводим пару в строку (числа через пробел)
            pair_as_str = " ".join(map(str, pair))
            out_file.write(pair_as_str + "\n")


if __name__ == "__main__":
    main()
