#!/usr/bin/env sh
set -e

mkdir -p -m 777 /tmp/uploads
mkdir -p /var/www/html/_/uploads
mount --bind /tmp/uploads /var/www/html/_/uploads

php-fpm8
