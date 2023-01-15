#!/usr/bin/env sh
set -e
echo "127.0.0.1 $(hostname)" >>/etc/hosts
ln -s /var/www/html/_ "/var/www/html/$KYZYLBORDA_SECRET_token"
chown -R www-data:www-data /var/www/html/_/uploads
exec docker-php-entrypoint apache2-foreground "$@"
