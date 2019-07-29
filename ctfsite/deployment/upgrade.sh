#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"/..

branchname=$1

# defined during the execution of a hook, need to unset this
unset GIT_DIR
git reset --hard
git pull releases "$branchname"

./scripts/install-or-upgrade-requirements.sh
./manage.sh migrate
./manage.sh collectstatic --noinput

touch "$(dirname "$PWD")"/tmp/restart.txt
