#!/usr/bin/env bash

#gcloud iam service-accounts create "${key_name}" --display-name "${key_display_name}"
#gcloud iam service-accounts list
gcloud iam service-accounts keys create --iam-account terraform@$gcp_project_id.iam.gserviceaccount.com terraform-gcp.json
