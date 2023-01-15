# Bege: Write-up

Из первой строки узнаем, что это код на Emacs Lisp.

Сначала отформатируем код, чтобы его было возможно читать:

```elisp
;;; cipher.el --- Simple string cipher for Emacs
;;; Code:

(defun fletcher (a b s)
  (if (string= "" s)
    (logior a (ash b 8))
    (let* ((a_ (mod (+ a (seq-first s)) 255))
           (b_ (mod (+ b a_) 255)))
      (fletcher a_ b_ (seq-rest s)))))

(defun some-number (ki)
  (let* ((ti (expt 2 32))
         (ab (mod ki ti))
         (ba (mod (logxor ab (ash ab 13)) ti))
         (aa (mod (logxor ba (ash ba -17)) ti))
         (bb (mod (logxor aa (ash aa 5)) ti)))
    bb))

(defun cipher-string (po)
  (car (seq-reduce
        (lambda (goo cu)
          (let* ((noko (fletcher 0 0 goo))
                 (ji (car goo))
                 (ki (cdr goo))
                 (ti (some-number ki)))
            (cons
              (concat ji (format "%02x" (mod (+ cu ki) 256)))
              ti)))
        po (cons "" (length po)))))

(defun cipher-buffer ()
  (interactive)
  (let ((ki (cipher-string (buffer-string))))
    (erase-buffer)
    (insert ki)
    (save-buffer)))

(provide 'cipher)
;;; cipher.el ends here
```

Видно, что интерфейсом шифровальщика становится функция `cipher-buffer`, которая
заменяет содержимое файла тем, что выдала функция `cipher-string`.

Начнем разбирать функцию `cipher-string`, заменяя имена переменных на адекватные и читая, что делает каждая функция.

```elisp
(defun cipher-string (s)
  (car (seq-reduce
        (lambda (p c)
          (let* ((noko (fletcher 0 0 goo))
                 (prev (car p))
                 (n0 (cdr p))
                 (n1 (some-number n0)))
            (cons
              (concat prev (format "%02x" (mod (+ c n0) 256)))
              n1)))
        po (cons "" (length s)))))
```

`noko` вообще не используется, как и `fletcher`. Можно не обращать на них внимания.

Функция выполняет редукцию строки по символам, используя в качестве промежуточного состояния пару `(готовая строка, число)`. Каждый символ складывает с числом `n`, добавляет в ответ и меняет число через функцию `some-number`. То есть это шифр Цезаря, но сдвиг меняется на каждом символе. Изначально `n` равно длине строки.

Осталось разобрать функцию `some-number`. Как мы уже поняли, она из одного числа делает какое-то другое число.

```elisp
(defun some-number (n)
  (let* ((m (expt 2 32))
         (n0 (mod n m))
         (n1 (mod (logxor n0 (ash n0 13)) m))
         (n2 (mod (logxor n1 (ash n1 -17)) m))
         (n3 (mod (logxor n2 (ash n2 5)) m)))
    n3))
```

Видно, что код производит серию битовых манипуляций над числом.
```python
def some_number(n):
    m = 2**32
    n0 = n % m
    n1 = n0 ^ (n0 << 13)
    n2 = n1 ^ (n1 >> 17)
    n3 = n2 ^ (n2 << 5)
    return n3
```

Теперь у нас есть формула преобразования числа и алгоритм шифрования, который несложно обратить:
```python
def decipher(data):
    n = len(data) // 2 # символы записываются в hex, поэтому длина увеличивается в два раза
    result = []
    for i in range(n):
        c = int(data[i*2:i*2+2], 16)
        result.append((c - n) % 256)
        n = some_number(n)
    return ''.join(chr(c) for c in result)
```

Запускаем это на файле, который нам дали:

```
1) N.N. Vavilov
2) Cells
3) Meyos
5) 700y after era
4) 47 chromosom
6) Mice mass
7) Chichen party
8) XO
9) Donald Knuth
10) sum(i ** 2 for i in range(10))
11) krasivoe
12) 13.25 * sqrt(-2i)
13) Mumu... I'm too sad... *crying*
14) Die
15) ugra_r0tate_brack3ts_5709bf352e3f
16) A visit to a fresh place will bring strange work.
17) You're ugly and your mother dresses you funny.
18) What I tell you three times is true.
		-- Lewis Carroll
19) You are going to have a new love affair.
20) Chicken Little only has to be right once.
21) A few hours grace before the madness begins again.
22) Afternoon very favorable for romance.  Try a single person for a change.
23) Your mode of life will be changed for the better because of good news soon.
24) You like to form new friendships and make new acquaintances.
25) You single-handedly fought your way into this hopeless mess.
26) You will live to see your grandchildren.
27) You will gain money by a speculation or lottery.
```

И на 15-м месте находим наш флаг: `ugra_r0tate_brack3ts_5709bf352e3f`.

Флаг: **ugra_r0tate_brack3ts_5709bf352e3f**
