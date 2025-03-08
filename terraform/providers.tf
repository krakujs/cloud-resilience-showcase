# providers.tf
provider "google" {
  credentials = file("terraform-sa-key.json")
  project     = var.project_id
  region      = var.region
}

provider "google-beta" {
  credentials = file("terraform-sa-key.json")
  project     = var.project_id
  region      = var.region
}