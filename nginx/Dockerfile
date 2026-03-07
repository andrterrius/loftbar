FROM nginx:alpine

RUN apk add --no-cache openssl curl

RUN mkdir -p /var/www/certbot /etc/nginx/ssl

RUN openssl req -x509 -nodes -newkey rsa:2048 -days 365 \
    -keyout /etc/nginx/ssl/dummy.key \
    -out /etc/nginx/ssl/dummy.crt \
    -subj "/CN=localhost"

COPY proxy-common.conf /etc/nginx/proxy-common.conf
COPY entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh

EXPOSE 80 443

CMD ["sh", "entrypoint.sh"]