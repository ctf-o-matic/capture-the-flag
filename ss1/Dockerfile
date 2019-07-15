FROM i386/alpine:latest

RUN apk update && apk add \
    bash \
    python \
    curl \
    binutils \
    gdb \
    nano \
    openssh-server \
    openssh \
    openrc \
    make \
    gcc \
    libc-dev \
    sudo

EXPOSE 22
EXPOSE 8001
EXPOSE 8002
EXPOSE 8003
EXPOSE 8004
EXPOSE 8005
EXPOSE 8006
EXPOSE 8007
EXPOSE 8008

COPY setup/generated/root /root
COPY system /

WORKDIR /setup
COPY setup .
RUN ./install.sh
ENTRYPOINT ["./entrypoint.sh"]
