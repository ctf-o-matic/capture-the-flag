#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

level=$(basename "$PWD")

password=$(cat "/home/$level/.password")

src_path=special/db.sqlite3
dst_path=/var/run/levels/$level/wwwdata/db.sqlite3
cp -v "$src_path" "$dst_path"
chown -v "$level:$level" "$dst_path"
chown -v 0600 "$dst_path"

cat << EOF | sqlite3 "$dst_path"
update safemedicalanalysis_medicalresult set description = replace(description, '__PASSWORD__', '$password');
EOF
