#!/bin/bash


echo "Creating custom nginx config with GENESIS_BACKEND_URL: $BACKEND_URL"
envsubst '$BACKEND_URL' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

echo "Starting nginx"
exec /usr/sbin/nginx -g "daemon off;"
