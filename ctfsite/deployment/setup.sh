#!/usr/bin/env bash

set -euo pipefail

if [[ $# != 2 ]]; then
    echo "usage: $0 release-repo-path release-branch"
    echo "example: $0 ~/repos/git/releases/project.git prod"
    exit 1
fi

if [[ "$1" != *.git ]]; then
    echo "error: first parameter was expected to end with '.git', got: $1"
    exit 1
fi

repo_path=$1
branch=$2

if ! [[ -d "$repo_path" ]]; then
    git init --bare "$repo_path"
fi

script_dir_abspath=$(cd "$(dirname "$0")"; pwd)

ln -snf "$script_dir_abspath/post-receive" "$repo_path/hooks/"
ln -snf "$script_dir_abspath/upgrade.sh" "$repo_path/upgrade-$branch.sh"

remote_repo_path=$(cd "$repo_path"; pwd)
remote_repo_path=${remote_repo_path#$HOME/}

cat << EOF
Setup almost done, a few manual steps remain.

In $script_dir_abspath, add the following remote:

    git add remote releases $repo_path

Then checkout the deployment branch:

    git checkout "$branch"

On your work PC, add the following remote:

    git add remote releases "server:$remote_repo_path"

Then add the following Git alias in your ~/.gitconfig:

    deploy-$branch = push releases master:$branch

This will enable "git deploy-$branch" to trigger a push to the deployment repo,
which in turn will trigger calling $script_dir_abspath/upgrade.sh
EOF
