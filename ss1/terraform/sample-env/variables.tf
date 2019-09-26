variable "docker_image_version" {
  description = "Version of the Docker image of the contest environment"
  default = "v6"
}

variable "docker_image_name" {
  description = "Version of the Docker image of the contest environment"
  default = "gcr.io/foo-bar-baz-123456/ss1"
}

variable "project_name" {
  description = "The ID of the Google Cloud project"
  default = "foo-bar-baz-123456"
}

variable "region" {
  default = "us-central1"
}

variable "region_zone" {
  default = "us-central1-f"
}

variable "credentials_file_path" {
  description = "Path to the JSON file used to describe your account credentials"
  default     = "~/.gcloud/foo-bar-baz-1234567890abcdef.json
}

variable "public_key_path" {
  description = "Path to file containing public key"
  default     = "~/.ssh/gcloud_id_rsa.pub"
}

variable "private_key_path" {
  description = "Path to file containing private key"
  default     = "~/.ssh/gcloud_id_rsa"
}
