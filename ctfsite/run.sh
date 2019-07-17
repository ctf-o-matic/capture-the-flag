#!/bin/sh

cd "$(dirname "$0")"

./manage.sh runserver "$@" --settings ctfsite.local_settings
