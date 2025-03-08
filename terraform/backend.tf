# backend.tf
terraform {
  backend "gcs" {
    bucket      = "cloud-simulation-project-tf-state"
    prefix      = "terraform/state"
    credentials = "terraform-sa-key.json"
  }
}