FROM nginx:mainline-alpine
RUN apk add --no-cache -X http://dl-cdn.alpinelinux.org/alpine/edge/testing file php8-fpm && rm /var/log/nginx/*.log
COPY www /var/www/html
