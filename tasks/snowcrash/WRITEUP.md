# Snow Crash: Write-up

> Разбор написан при помощи участника команды **two_raccoons_enough** ([@diduk001](https://t.me/diduk001)).

В HTML-файле видим форму ввода флага и кнопку «Check». Давайте посмотрим, как флаг проверяется. Хорошие новости: код на JavaScript. Плохие новости: внутри лежит [WebAssembly](https://webassembly.org/).

Судя по коду, основная логика реализована именно в WASM, все остальное — графическая оболочка.

Для начала выдернем из HTML собственно код на WASM. Для этого достаточно записать массив чисел в файл как-нибудь так:

```python
code = [0, 97, ..., 46, 49]
open("code.wasm", "wb").write(bytes(code))
```

`file code.wasm` подтверждает, что это корректный бинарник. Для декомпиляции wasm есть несколько утилит. WABT, например, содержит декомпилятор [wasm-decompile](https://github.com/WebAssembly/wabt/blob/main/docs/decompiler.md). Ловким движением руки декомпилируем бинарник:

```shell
$ wasm-decompile code.wasm -o code.dcmp
```

И получаем следующее чудо:

```c
export memory memory(initial: 2, max: 0);

global stack_pointer:int = 66640;

table T_a:funcref(min: 1, max: 1);

data rodata(offset: 1024) =
  "\12x0\15-`>\054p\08x\06q\12\048lTO.)Dr|FN2t\1aEzCAd\1a~\0d)%j\10\02B/5"
  "T|\1dKGmR1K`\1dC\1f.]B\03\17h\02z9U";

function strlen(a:int):int {
  var d:int;
  var b:int = 0;
  loop L_a {
    var c:ubyte_ptr = a + b;
    d = b + 1;
    b = d;
    if (c[0]) continue L_a;
  }
  return d + -1;
}

function srand(a:int) {
  0[274]:int = a
}

function rand():int {
  var a:int;
  0[274]:int = (a = 0[274]:int * 214013 + 2531011);
  return a >> 16 & 32767;
}

export function check_flag(a:int):int {
  var b:ubyte_ptr = stack_pointer - 80;
  stack_pointer = b;
  var c:int = 0;
  if (strlen(a) != 69) goto B_a;
  c = 0;
  loop L_b {
    (b + c)[0]:byte = (a + c)[0]:ubyte;
    c = c + 1;
    if (c != 69) continue L_b;
  }
  srand(1);
  var d:int = 0;
  loop L_c {
    c = rand() % 69;
    if (c == (a = rand() % 69)) continue L_c;
    c = b + c;
    c[0]:byte = c[0]:ubyte ^ (b + a)[0]:ubyte;
    d = d + 1;
    if (d != 1000) continue L_c;
  }
  c = 0;
  if (b[0] != 18) goto B_a;
  a = 1;
  loop L_e {
    c = a;
    if (c == 69) goto B_d;
    a = c + 1;
    if ((b + c)[0]:ubyte == (c + 1024)[0]:ubyte) continue L_e;
  }
  label B_d:
  c = c + -1 > 67;
  label B_a:
  stack_pointer = b + 80;
  return c;
}
```

`rodata` содержит, на первый взгляд, какой-то мусор; пока проигнорируем его. `strlen`, как понятно из названия, считает длину строки, `srand` инициализирует генератор псевдослучайных чисел, а `rand` эти числа генерирует.

`check_flag` можно переписать на псевдокод следующим образом:

```python
def check_flag(flag: bytearray) -> bool:
    if len(flag) != 69:
        return False
    srand(1)
    d = 0
    while d != 1000:
        c = rand() % 69
        a = rand() % 69
        if a == c:
            continue
        flag[c] ^= flag[a]
        d += 1
    if flag[0] != 18:
        return False
    return flag[1:] == memory[1024 + 1:1024 + 69]
```

Давайте поймём, что эта функция делает:

1. Проверяет длину флага — мы знаем, что она равна 69.
2. Вызывает `srand(1)` — по всей видимости, это инициализация генератора псевдослучайных чисел.
3. 1000 раз генерирует два различных индекса: `c` и `a` по формуле `rand() % 69`, а затем выполняет [побитовое исключающее или (XOR)](https://ru.wikipedia.org/wiki/%D0%98%D1%81%D0%BA%D0%BB%D1%8E%D1%87%D0%B0%D1%8E%D1%89%D0%B5%D0%B5_%C2%AB%D0%B8%D0%BB%D0%B8%C2%BB) для символов флага с индексами `c` и `a`, записывая результат по индксу `c`.
4. И, наконец, ожидает, что результат совпадёт с `rodata` по индексу 1024.

Вот и она:

```c
data rodata(offset: 1024) =
  "\12x0\15-`>\054p\08x\06q\12\048lTO.)Dr|FN2t\1aEzCAd\1a~\0d)%j\10\02B/5"
  "T|\1dKGmR1K`\1dC\1f.]B\03\17h\02z9U";
```

Осталось понять, как его декодировать. Здесь, к сожалению, придется помудрить: символов в этой строке явно больше 69, а еще здесь много обратных слешей, поэтому явно используется эскейпинг, но нестандартный — обычно формат `\x<2 hex digits>` или `\<3 oct digits>`, а здесь что-то другое. Можно попробовать угадать формат, можно поискать документацию.

А можно поступить как программист — найти исходники декомпилятора в репозитории WABT и, поискав в них подстроку `\\`, найти [функцию BinaryToString](https://github.com/WebAssembly/wabt/blob/a4a77c18df16d6ee672f2a2564969bc9b2beef3a/src/decompiler.cc#L697):

```cpp
std::string BinaryToString(const std::vector<uint8_t>& in) {
  std::string s = "\"";
  size_t line_start = 0;
  static const char s_hexdigits[] = "0123456789abcdef";
  for (auto c : in) {
    if (c >= ' ' && c <= '~') {
      s += c;
    } else {
      s += '\\';
      s += s_hexdigits[c >> 4];
      s += s_hexdigits[c & 0xf];
    }
    if (s.size() - line_start > target_exp_width) {
      if (line_start == 0) {
        s = "  " + s;
      }
      s += "\"\n  ";
      line_start = s.size();
      s += "\"";
    }
  }
  s += '\"';
  return s;
}
```

Что ж, это было ожидаемо: после `\` сразу идет двузначное шестнадцатиричное число без привычного `x`. Можно накалякать парсер, можно перевести символы из hex руками, а можно редактором заменить `\` на `\x`, засунуть строку в Python и получить:

```python
rodata = bytearray([18, 120, 48, 21, 45, 96, 62, 5, 52, 112, 8, 120, 6, 113, 18, 4, 56, 108, 84, 79, 46, 41, 68, 114, 124, 70, 78, 50, 116, 26, 69, 122, 67, 65, 100, 26, 126, 13, 41, 37, 106, 16, 2, 66, 47, 53, 84, 124, 29, 75, 71, 109, 82, 49, 75, 96, 29, 67, 31, 46, 93, 66, 3, 23, 104, 2, 122, 57, 85])
```

Собственно, отсюда видно, что сравнение первого символа с числом 18 — просто оптимизация компилятора.

Осталась идейная часть: взяв эту строку за основу, применить к ней все операции в обратном порядке и получить флаг:

```python
def restore_flag(flag: bytearray) -> str:
    srand(1)
    operations = []
    d = 0
    while d != 1000:
        c = rand() % 69
        a = rand() % 69
        if a == c:
            continue
        operations.append((c, a))
        d += 1
    for c, a in operations[::-1]:
        flag[c] ^= flag[a]
    return flag.decode()
```

Естественно, придется дополнительно руками реализовать `rand` и `srand`, не забывая про переполнение:

```python
seed: int = 0

def srand(a: int):
    global seed
    seed = a

def rand() -> int:
    global seed
    seed = (seed * 214013 + 2531011) % (2 ** 32)
    return (seed >> 16) & 32767
```

Флаг: **ugra_dont_roll_your_own_cryptography_unless_you_are_nist_po9t49ix2c0b**

-------

Есть и другой путь решения — от команды **two_raccoons_enough**.

Давайте сначала восстановим все пары `c` и `a` — для этого нам достаточно разобраться только в функциях `rand` и `srand`. Реализацию можно посмотреть в [`get_idx_pairs.py`](writeup-alt/get_idx_pairs.py).

Теперь нам нужно восстановить флаг по парам индексов и результату операций `^=`. Давайте поймём, как работает XOR (его ещё обозначают символом ⊕). Начнём со сложения:

A | B | A + B
---|---|---
Чётное | Чётное | Чётное
Чётное | Нечётное | Нечётное
Нечётное | Чётное | Нечётное
Нечётное | Нечётное | Чётное

Заметим, что это очень похоже на таблицу истинности XOR для двух битов. Это неспроста — XOR это [сумма бит по модулю два](https://ru.wikipedia.org/wiki/%D0%A1%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5_%D0%BF%D0%BE_%D0%BC%D0%BE%D0%B4%D1%83%D0%BB%D1%8E) — иначе говоря, в [GF(2)](https://ru.wikipedia.org/wiki/%D0%9A%D0%BE%D0%BD%D0%B5%D1%87%D0%BD%D0%BE%D0%B5_%D0%BF%D0%BE%D0%BB%D0%B5), a ⊕ b = a + b.

Что нам это даёт? Давайте рассматривать наши символы флага не как цельное число, а бит за битом. Обозначим биты флага как `flag[i]`, а биты результата — как `result[i]`.

Тогда `result[i]` можно представить в виде суммы всех битов флага, умноженных на некоторые коэффициенты: `k[i][0] * flag[0] + k[i][1] * flag[1] + ... + k[i][n - 1] * flag[n - 1] = result[i]` в GF(2) для каких-то коэффициентов. Говоря очень умным языком, перед нами [система линейных алгебраических уравнений](https://ru.wikipedia.org/wiki/%D0%A1%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0_%D0%BB%D0%B8%D0%BD%D0%B5%D0%B9%D0%BD%D1%8B%D1%85_%D0%B0%D0%BB%D0%B3%D0%B5%D0%B1%D1%80%D0%B0%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D1%85_%D1%83%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B9) над полем GF(2). Кстати, поскольку ⊕ — побитовая операция, все биты считаются независимо. Такую систему можно взять и решить.

Нам осталось узнать, что же такое `k[i][j]`. Давайте изначально будем считать `k` [единичной матрицей](https://ru.wikipedia.org/wiki/%D0%95%D0%B4%D0%B8%D0%BD%D0%B8%D1%87%D0%BD%D0%B0%D1%8F_%D0%BC%D0%B0%D1%82%D1%80%D0%B8%D1%86%D0%B0) (`result[i] = flag[i]`, когда ни одной операции не сделали), а при XOR индексов `a` и `b` будем прибавлять `k[b][j]` к `k[a][j]` для всех `j`.

> На самом деле, поскольку мы живём в GF(2), в котором `a ^ a = 0`, мы можем исключать повторяющиеся строчки. В наших терминах, мы вместо наших коэффициентов можем использовать только остаток от деления на 2 — все `k[i][j]` будут либо нулём, либо единицей.

Что ж, осталось написать скрипт. Воспользуемся для этого библиотекой [sagemath](https://www.sagemath.org/) — она содержит довольно много математических и околокриптографических функций. Например, её можно использовать как библиотеку для Python.

Пример решения есть в [solve.py](writeup-alt/solve.py).

Флаг: **ugra_dont_roll_your_own_cryptography_unless_you_are_nist_po9t49ix2c0b**
