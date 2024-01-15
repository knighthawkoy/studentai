FROM alpine:latest
LABEL "maintainer"="AIbot <jasai@jas-ai.org>"

ARG POCKETBASE_VERSION=0.20.6

RUN apk add --no-cache \
    ca-certificates \
    unzip \
    wget \
    zip \
    zlib-dev

ADD https://github.com/pocketbase/pocketbase/releases/download/v${POCKETBASE_VERSION}/pocketbase_${POCKETBASE_VERSION}_linux_amd64.zip /app/pocketbase/pocketbase.zip

RUN unzip /app/pocketbase/pocketbase.zip -d /app/pocketbase && \
    chmod +x /app/pocketbase/pocketbase && \
    rm /app/pocketbase/pocketbase.zip

env PB_ADMIN_EMAIL admin@jasai.org
env PB_ADMIN_PASSWORD 2024Jasmine

COPY ./pb_migrations /app/data/pb_migrations

WORKDIR /app/data/
EXPOSE 8090

CMD [ "/app/pocketbase/pocketbase", "serve", "--http=0.0.0.0:8090", "--dir=/app/data/pb_data", "--migrationsDir=/app/data/pb_migrations", "--publicDir=/app/data/pb_public" ]
