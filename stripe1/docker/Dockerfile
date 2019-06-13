FROM i386/alpine:latest

RUN apk update
RUN apk add bash
RUN apk add python
RUN apk add curl
RUN apk add binutils
RUN apk add gdb
RUN apk add nano
RUN apk add openssh-server
RUN apk add openrc
RUN apk add make
RUN apk add gcc
RUN apk add libc-dev
RUN apk add sudo

EXPOSE 22
EXPOSE 8002
EXPOSE 8004

COPY static-files /
COPY generated-files /

WORKDIR /setup
COPY setup .
RUN ./install.sh
CMD ./start.sh
