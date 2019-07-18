#!/bin/sh

cd "$(dirname "$0")"

./manage.sh runserver 0.0.0.0:8000 "$@" --settings ctfsite.local_settings
