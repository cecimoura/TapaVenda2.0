FROM python:3.11-alpine AS build
WORKDIR /app
COPY index.html style.css ./
COPY scripts/build.py scripts/build.py
COPY variants/ variants/
COPY assets/ assets/
RUN python scripts/build.py

FROM nginx:stable-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist/ /usr/share/nginx/html/
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget -q -O /dev/null http://127.0.0.1/healthz || exit 1
