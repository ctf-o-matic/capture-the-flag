FROM i386/alpine:latest

RUN apk update && apk add \
    bash \
    python \
    curl \
    binutils \
    gdb \
    nano \
    openssh-server \
    openrc \
    make \
    gcc \
    libc-dev \
    sudo

EXPOSE 22
EXPOSE 8002
EXPOSE 8004

COPY static-files /
COPY generated-files /

WORKDIR /setup
COPY setup .
RUN ./install.sh
ENTRYPOINT ["./entrypoint.sh"]
