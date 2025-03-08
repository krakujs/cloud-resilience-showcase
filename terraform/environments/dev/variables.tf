# environments/dev/variables.tf
variable "project_id" {
  description = "The GCP project ID"
  type        = string
  default     = "cloud-simulation-project"
}

variable "region" {
  description = "The GCP region to deploy resources"
  type        = string
  default     = "europe-west9"  # Paris region
}

variable "zone" {
  description = "The GCP zone to deploy resources"
  type        = string
  default     = "europe-west9-a"  # Paris zone a
}

variable "environment" {
  description = "Environment (dev, prod, etc.)"
  type        = string
  default     = "dev"
}

variable "credentials_file" {
  description = "Path to the service account key JSON file"
  type        = string
  default     = "../../terraform-sa-key.json"
}