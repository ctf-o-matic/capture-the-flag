#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"/..

branchname=$1

unset GIT_DIR
git pull releases "$branchname"

./scripts/install-or-upgrade-requirements.sh
./manage.sh collectstatic --noinput

touch "$(dirname "$PWD")"/tmp/restart.txt
