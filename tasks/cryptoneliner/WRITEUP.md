# Криптобаш: Write-up

В первую очередь изучим файл `bash_history`. 
Среди достаточно рутинных действий среднестатистического пользователя Linux, можно увидеть такой интересный фрагмент:

```bash
openssl enc -aes-256-cbc -pbkdf2 -in secret.data -out secret.enc -k $my_key

echo -n $my_key | base64 | tr '[A-Za-z0-9]' '[N-ZA-Mn-za-m3-90-2]' | rev | xxd -p | xargs -I {} python3 -c "import sys;print(f'{int(sys.argv[1],16)^int((sys.argv[2]*(len(sys.argv[1])//len(sys.argv[2])+1))[:len(sys.argv[1])],16):x}')" {} deadbeef | awk '{print substr($0,length/2+1) substr($0,1,length/2)}'

unset $my_key
```

Разберём по частям всё выше написанное. 
В первой строчке используется команда `openssl`, с помощью которой производится шифрование файла по алгоритму AES. Флаг `-pbkdf2` говорит о том, что ключ шифрования формируется на основе пароля по стандарту [PBKDF2](https://ru.wikipedia.org/wiki/PBKDF2),  так что можем предположить, что ключ `$my_key`, который передаётся команде, представляет собой  печатный текст.

Ниже видим большую страшную строчку из множества команд, соединённых символами `|` — это пайпы, специальные элементы командной оболочки `bash`, с помомщью которых можно перенаправлять вывод из одной команды в другую. Видимо, таким образом сотрудник и пытался зашифровать ключ. 
Как именно он это сделал, мы разберём чуть ниже.

Ну и последней строчкой переменная `$my_key` очищается с помощью команды `unset`, в результате чего изначальный ключ и был утерян. 
Попробуем же его восстановить!

Для того, чтобы разобраться, что же происходит в этом огромном однострочнике, сперва развернём его:

```bash
echo -n $my_key | \ 
    base64 | \
    tr '[A-Za-z0-9]' '[N-ZA-Mn-za-m3-90-2]' | \
    rev | \
    xxd -p | \
    xargs -I {} python3 -c "import sys;print(f'{int(sys.argv[1],16)^int((sys.argv[2]*(len(sys.argv[1])//len(sys.argv[2])+1))[:len(sys.argv[1])],16):x}')" {} deadbeef | \
    awk '{print substr($0,length/2+1) substr($0,1,length/2)}'
```

Теперь мы можем последовательно разобрать, как преобразуется ключ на каждом этапе. Сперва он кодируется в base64 одноимённой командой, тут всё просто. Для обратного декодирования у этой команды есть флаг `-d`.

Далее мы видим команду `tr` с двумя аргументами, чем-то напоминающими регулярные выражения.
Обратившись к [системному руководству](https://www.opennet.ru/cgi-bin/opennet/man.cgi?topic=tr&category=1) команды, мы узнаем, что эту команду можно использовать для замены символов в строках или файлах.
Для этого команде можно передать диапазоны символов, согласно которым будет производиться замена. 
В данном случае мы видим, что, например, диапазону символов от A до Z будет соответствовать диапазон от N до Z, а потом от A до M:
```
ABCDEFGHIJKLMNOPQRSTUVWXYZ
↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
NOPQRSTUVWXYZABCDEFGHIJKLM
```
Визуализировав эту замену, понимаем, что это ничто иное, как шифр Цезаря, а точнее, его вариация — ROT13. В этой реализации заглавные и строчные буквы английского алфавита будут сдвинуты на 13 символов, как и цифры. Но так как для замены используются именно наборы символов, а не таблица ASCII, то 10 цифр рассматриваются как отдельный алфавит,в рамках которого производится сдвиг. Можно представить полную таблицу замены:

```
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789
↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm3456789012
```
Для обратного преобразования достаточно будет использовать ту же самую команду `tr`, только поменяв аргументы местами.

Следующим этапом является команда `rev`. По первому же запросу в Гугле можно узнать, что это команда просто переворачивает строку задом наперёд, а значит для обратного преобразования нужно лишь снова применить эту команду.

Далее мы видим команду `xxd` с флагом `-p`. 
Эта команда создаёт шестнадцатиричное представление файла или потока стандартного ввода, а флаг `-p` позволяет вывести лишь саму шестнадцатиричную запись, а не hexdump-таблицу, в которой также есть номера байтов и ASCII-представления печатных символов. 
Для обратного декодирования из шестнадцатиричного представления в ASCII-символы у команды есть флаг `-r`.

После этого вывод команды перенаправляется в Питон, но не просто так, а с дополнительной командой `xargs`. Она используется для формирования списка аргументов для последующей команды, в данном случае Питона. В самом Питоне же выполняется ещё один непонятный однострочник. Особо не вчитываясь в код, мы можем сделать следующие выводы:

1. Первым аргументом является шестнадцатеричное число, так как перед этим выполнялась команда `xxd`
2. Вторым аргументом является запись `deadbeef`, которая тоже может являться шестнадцатеричным числом
3. Вывод команды — опять шестнадцатеричное число, так как в форматной строке используется модификатор `:x`
4. В самом скрипте выполняется операция XOR

На основе всего вышеперечисленного можно сделать вывод, что команда выполняет XOR-шифрование с ключом `0xDEADBEEF`. И это действительно так! Помимо этого, перед непосредственно шифрованием ключ повторяется N раз до того момента, пока его длина не будет равна длине исходного текста. В результате, весь однострочник можно представить в следующем, более читабельном, виде:

```python
import sys

# аргументы команды
msg_str = sys.argv[1]
key_str = sys.argv[2]

# преобразование исходного сообщения из hex-строки в число
msg = int(msg, 16)

# дополнение ключа
key_pad = key_str * (len(msg_str) // len(key_str) + 1)[:len(msg_str)]
# преобразование ключа из hex-строки в число
key = int(key_pad, 16)

# вывод результата XOR в шестнадцатиричном формате
print(f'{msg ^ key:x}')
```

Немного почитав про свойства операции XOR и шифрование, на ней основанное, можно узнать, что зная один из операндов (ключ) и результат операции (шифротекст), можно легко восстановить исходное сообщение:

$$a \oplus b = c \rightarrow a = b \oplus c$$

Поэтому для обратного преобразования этой операции достаточно будет использовать тот же самый однострочник, только вместо исходного  передать XOR-ключ `0xDEADBEEF` и результат этого шифрования, который мы получим из последнего этапа преобразований.

А последним этапом является команда `awk`. awk — это Си-подобный язык, предназначенный для обработки строк по различным шаблонам (регулярным выражениям). В данном случае она применяется для того, чтобы поменять местами половины входной строки. Очевидно, что для обратного преобразования достаточно просто применить ту же команду.

Итак, разобравшись со всеми элементами этого однострочника, мы можем построить свой собственный, который будет «дешифровать» наш ключ:

```bash
decrypted_key=$(echo $encrytped_key | awk '{print substr($0,length/2+1) substr($0,1,length/2)}' | xargs -I {} python3 -c "import sys;print(f'{int(sys.argv[1],16)^int((sys.argv[2]*(len(sys.argv[1])//len(sys.argv[2])+1))[:len(sys.argv[1])],16):34x}')" {} deadbeef | xxd -r -p | rev | tr '[N-ZA-Mn-za-m3-90-2]' '[A-Za-z0-9]' | base64 -d)
```

Получив ключ, которым был зашифрован наш секретный файл, мы наконец можем его дешифровать:

```bash
openssl enc -d -aes-256-cbc -pbkdf2 -in secret.enc -out - -k $decrypted_key
```

Также все эти действия можно объединить в один скрипт, например, [такой](solve.sh).

В результате видим то самое секретное послание, а в его конце...

Флаг: **ugra_oneliners_rule_19f99780be9d**

## Постмортем

В ходе соревнований выяснилось, что при генерации файла `bash_history` существует 1.7%-я вероятность, что в нём не сформируются команды, непосредственно шифрующие ключ. Ошибка была сразу же исправлена.
