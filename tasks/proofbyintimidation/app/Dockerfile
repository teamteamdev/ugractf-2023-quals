FROM php:7.4-apache
RUN \
	apt-get update && \
	apt-get install -y libzip-dev zlib1g-dev && \
	docker-php-ext-install zip
RUN rm /var/log/apache2/*.log
COPY docker-php.conf /etc/apache2/conf-available/docker-php.conf
COPY start.sh /app/
COPY --chown=www-data:www-data www /var/www/html
ENTRYPOINT ["/app/start.sh"]
