#!/bin/sh

cd "$(dirname "$0")"
. ./venv.sh

if test $# = 0; then
    python manage.py help
else
    python manage.py "$@"
fi
