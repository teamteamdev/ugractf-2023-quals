#!/usr/bin/env bash
set -e

sed -i "s/{{FLAG}}/$KYZYLBORDA_SECRET_flag/" safestr.c
gcc safestr.c -o safestr

exec socat unix-listen:/tmp/app.sock,fork system:./safestr
