FROM mediamoose/nginx:1.8

ENV NGINX_MAIN_HOSTNAME=localhost \
    NGINX_CONF=/etc/nginx/conf.d/nginx.conf \
    NGINX_SERVER_CONF=production.conf

COPY nginx.conf /etc/nginx/conf.d/nginx.conf
COPY staging.conf /etc/nginx/conf.d/staging.conf
COPY production.conf /etc/nginx/conf.d/production.conf
