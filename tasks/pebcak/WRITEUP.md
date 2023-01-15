# PEBCAK: Write-up

Программы на эзотерических языках &mdash; всегда весело, особенно если язык как эзотерический не задумывался.

В этом задании есть два основных пути решения.


## Способ 1, интеллектуальный

Читаем код:

```vbscript
code = "ANEcwu4fYegObF1i2VXyvJHxKd0qBkMl36ILRaUjPG8rToSZzpCDt7n9mWsh5Q"
Function Encode(n)
    If n = 0 Then
        Encode = ""
    Else
        Encode = Mid(code, n Mod Len(code) + 1, 1) & Encode(n \ Len(code))
    End If
End Function

Wscript.Echo "Enter flag:"
flag = WScript.StdIn.ReadLine

Dim numbers()
ReDim numbers(Len(flag) - 1)
s = ""
For i = 0 to Len(flag) - 1
    numbers(i) = asc(Mid(flag, i + 1, 1))
    If i > 2 Then
        numbers(i) = (numbers(i) + numbers(i-1) + numbers(i-2)) mod 179179
    End If
    If i > 0 Then
        s = s & "_"
    End If
    s = s & Encode(numbers(i))
Next

WScript.Echo s
```

Переводим на нормальный язык, помня, что строки в VBS индексируются с единицы, а массивы — с нуля:

```python
code = "ANEcwu4fYegObF1i2VXyvJHxKd0qBkMl36ILRaUjPG8rToSZzpCDt7n9mWsh5Q"
def encode(n):
    if n == 0:
        return ""
    else:
        return code[n % len(code)] + encode(n // len(code))

print("Enter flag:")
flag = input()

numbers = [0] * len(flag)
s = ""
for i in range(len(flag)):
    numbers[i] = ord(flag[i])
    if i > 2:
        numbers[i] = (numbers[i] + numbers[i-1] + numbers[i-2]) % 179179
    if i > 0:
        s += "_"
    s += encode(numbers[i])

print(s)
```

Понимаем, что происходит следующее. ASCII-коды флага как массив чисел шифруется слева направо, и очередное число зависит от предыдущего по принципу

```python
numbers[i] = (numbers[i] + numbers[i-1] + numbers[i-2]) % 179179
```

...а затем числа получившегося массива кодируются в base62 с нестандартным алфавитом и соединяются символом `_`.

Для расшифровки нужно применить те же действия в обратном порядке. Во-первых, распарсить строку в массив чисел:

```python
encrypted_flag = "9N_GN_tN_wu_qY_xi_Md_08_zfN_ctN_HQE_O7w_vnf_xZb_1Gv_VB6_y6f_lNG_H5N_0Nr_xNo_dBG_09j_rZI_QwB_122_CHT_tE1_qDO_emd_0Za_xuV_I2Y_Bxd_WG6_Okb_sgS_7cb_GPO_cSx_y0L_OLb_4dN_fA1_s0i_DBk_8mT_xzq_z40_oXf_Jq6_ZZP"
code = "ANEcwu4fYegObF1i2VXyvJHxKd0qBkMl36ILRaUjPG8rToSZzpCDt7n9mWsh5Q"

def decode(s):
    n = 0
    for c in s[::-1]:
        n *= len(code)
        n += code.find(c)
    return n

numbers = [decode(s) for s in encrypted_flag.split("_")]
```

Дальше действия нужно развернуть порядок цикла и каждую операцию внутри него: если раньше к `numbers[i]` прибавлялись предыдущие два числа по модулю, то теперь их нужно вычесть:

```python
for i in range(len(numbers) - 1, 2, -1):
    numbers[i] = (numbers[i] - numbers[i-1] - numbers[i-2]) % 179179
```

Наконец, получившиеся числа &mdash; это ASCII-коды, из которых можно получить флаг:

```python
print(bytes(numbers).decode())
```


## Способ 2, автоматизированный

Можно заметить, что шифровальщик в некотором смысле монотонен. А именно, если ему подать строку `ugra_`, то получится `9N_GN_LN_wu_qY`. А данная в условии строка как раз начинается с такого префикса.

Таким образом, вырисовывается план: перебираем следующий символ после `ugra_` среди всех допустимых символов (`[A-Za-z0-9_]`), шифруем строку `ugra_<очередной символ>` и выбираем из них такую, чтобы данная в условии строка имела такой префикс. Таким образом мы узнаем, что флаг начинается с `ugra_t`. Продолжаем так, пока не получим строку, которая при шифровании полностью совпадет с зашифрованной строкой из условия.

Сделать это программно можно, например, так:

```python
import string
import subprocess

encrypted_flag = "9N_GN_tN_wu_qY_xi_Md_08_zfN_ctN_HQE_O7w_vnf_xZb_1Gv_VB6_y6f_lNG_H5N_0Nr_xNo_dBG_09j_rZI_QwB_122_CHT_tE1_qDO_emd_0Za_xuV_I2Y_Bxd_WG6_Okb_sgS_7cb_GPO_cSx_y0L_OLb_4dN_fA1_s0i_DBk_8mT_xzq_z40_oXf_Jq6_ZZP"

def encrypt(s):
    proc = subprocess.run(["cscript", "encrypt.vbs"], input=s.encode() + b"\r\n", capture_output=True)
    return proc.stdout.decode().partition(":")[2].strip()

flag = "ugra_"
while encrypt(flag) != encrypted_flag:
    for c in string.ascii_letters + string.digits + "_":
        if encrypted_flag.startswith(encrypt(flag + c)):
            flag += c
            break
    else:
        assert False

print(flag)
```

Флаг: **ugra_thats_not_how_access_control_works_c2crkn95jari**
