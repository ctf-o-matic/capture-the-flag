#!/usr/bin/env bash
#

#ssh-add ~/.ssh/gcloud_id_rsa

set -euo pipefail

if ! [[ ${version+x} ]]; then
    echo "Run as: version=vNUM $0"
    exit 1
fi

image=gcr.io/$gcp_project_id/ss1
name=$image:$version

docker tag ss1 "$name"
docker push "$name"

terraform destroy -auto-approve  && terraform apply -auto-approve
