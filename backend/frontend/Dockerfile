FROM node:latest AS build

WORKDIR workspace
COPY . .
RUN npm run build

FROM  nginx:latest AS deployment

RUN mkdir -p /var/cache/nginx && \
  chown -R www-data:www-data /var/cache/nginx && \
  rm -rf /var/log/nginx/* && \
  chown -R www-data:www-data /var/log/nginx

COPY nginx/nginx.conf.template /etc/nginx/
COPY nginx/start.sh /app/start.sh
RUN  chown www-data:www-data /app/start.sh

COPY --from=build /workspace/build /app/public
RUN chown -R www-data:www-data /etc/nginx && \
  chown -R www-data:www-data /app && \
  chown -R www-data:www-data /run


USER www-data
RUN whoami

WORKDIR app

EXPOSE 8080
ENTRYPOINT ["/app/start.sh"]
