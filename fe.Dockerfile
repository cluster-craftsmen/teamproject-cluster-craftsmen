FROM node:17.4-alpine3.14 AS builder

# Install pnpm globally
RUN npm install -g pnpm

WORKDIR /app
COPY ./frontend .
RUN rm -rf node_modules && pnpm install
RUN pnpm run build

FROM nginx:1.21.5-alpine
COPY --chown=nginx:nginx --from=builder /app/nginx-ui.conf /etc/nginx/conf.d/default.conf
COPY --chown=nginx:nginx --from=builder /app/dist/ /var/www/html/