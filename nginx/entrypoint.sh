#!/bin/bash

if [ "$PRODUCTION" = "True" ]; then
    echo "Production mode: using only APP_DOMAIN"
    export SERVER_NAMES="${APP_DOMAIN}"

    (while :; do sleep 8h; nginx -s reload; done) &

else
    echo "Development mode: using localhost and APP_DOMAIN"
    export SERVER_NAMES="localhost ${APP_DOMAIN}"

    (while :; do sleep 4h; nginx -s reload; done) &
fi

envsubst '${BACKEND_PORT} ${FRONTEND_PORT} ${APP_DOMAIN} ${SERVER_NAMES}' < /etc/nginx/conf.d/template > /etc/nginx/conf.d/default.conf

exec nginx -g 'daemon off;'