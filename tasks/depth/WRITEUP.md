# Глубина: Write-up

Открываем сайт и наблюдаем кучу директорий. Будем надеяться, что флаг где-то в них. Открываем все четыре директории. В трех из них, по-видимому, лежит `index.html` с веселыми (или не очень) цитатками, а четвертая внутри себя содержит другие четыре директории, с которыми история повторяется.

По-видимому, флаг лежит в какой-то из очень глубоких директорий. Можно попробовать потыкать руками, но после пятидесяти директорий руки явно устанут. Придется автоматизировать этот процесс.

Для скрепинга сайта можно попробовать использовать `wget`, не забыв отключить ограничение уровня вложенности и, мысленно карая админов за кривую обработку слешей, нагуглить, что починить ошибку `pathconf: Not a directory` можно, включив `--adjust-extension`:

```shell
$ wget -r -l inf --adjust-extension https://depth.q.2023.ugractf.ru/lkv2x8ejmsuxumkb
```

Эта команда прекрасно работает до некоторого момента, а затем внезапно падает с ошибкой `File name too long`, потому что `wget` сохраняет найденные файлы в файловую систему, а на длины путей в Linux есть ограничение в 4096 байт (по крайней мере, в том контексте, в котором их использует `wget`), чего явно не хватает. С Windows ситуация еще хуже.

Дальше можно пытаться как-нибудь настраивать или патчить `wget`, чтобы он нормально обрабатывал длинные пути, но, скорее всего, проще будет просто написать логику обхода руками. Благо, даже парсить HTML не придется: каждая страница имеет очень простой вид:

```html
<H1>Index of /4b07d2e100356dab/</H1><A HREF=draconic_boa/>draconic_boa</A><BR><A HREF=field_violin/>field_violin</A><BR><A HREF=opal_tiger/>opal_tiger</A><BR><A HREF=yellow_pilot/>yellow_pilot</A><BR>
```

```python
import re
import requests

def visit(path):
    text = requests.get(path).text
    if "Index of" not in text:
        print(text)
        return

    for match in re.finditer(r"HREF=(\w+)/", text):
        word = match.group(1)
        visit(path + "/" + word)

visit("https://depth.q.2023.ugractf.ru/lkv2x8ejmsuxumkb")
```

Для ускорения этот процесс можно распараллелить: [solution_async.py](writeup/solution_async.py), но если время не поджимает, то это не обязательно.

Посреди всякого мусора в самом низу получим вывод с флагом:

> ...  
> The primary purpose of the DATA statement is to give names to constants; instead of referring to PI as 3.141592653589797, at every appearance, the variable PI can be given that value with a DATA statement, and used instead of the longer form of the constant. This also simplifies modifying the program, should the value of PI change. -- Xerox FORTRAN manual  
> The program is ill-formed. The behavior is undefined. No diagnostic is required.  
> How many Prolog programmers does it take to change a light bulb? Yes.  
> I think ... err ... I think ... I think I'll go home  
> It's never too late to give up.  
> Ninety-nine bugs in the code. Take one down, patch it around, Ninety-nine bugs in the code.  
> **ugra_i_have_always_imagined_that_paradise_will_be_a_kind_of_library_h98hv1e4twat**  
> Nature of a compromise is that it leaves everyone more or less equally unhappy.

Флаг: **ugra_i_have_always_imagined_that_paradise_will_be_a_kind_of_library_h98hv1e4twat**
