# environments/dev/backend.tf
terraform {
  backend "gcs" {
    bucket      = "cloud-simulation-project-tf-state"
    prefix      = "terraform/dev"
    credentials = "../../terraform-sa-key.json"
  }
}