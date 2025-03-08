# modules/networking/variables.tf
variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region to deploy resources"
  type        = string
}

variable "network_name" {
  description = "The name of the VPC network"
  type        = string
  default     = "crs-network"
}

variable "subnet_name" {
  description = "The name of the subnet"
  type        = string
  default     = "crs-subnet"
}

variable "subnet_cidr" {
  description = "The CIDR range for the subnet"
  type        = string
  default     = "10.0.0.0/20"
}

variable "secondary_ranges" {
  description = "Secondary ranges for the subnet (for GKE pods and services)"
  type = map(list(object({
    range_name    = string
    ip_cidr_range = string
  })))
  default = {
    "crs-subnet" = [
      {
        range_name    = "pods"
        ip_cidr_range = "10.16.0.0/16"
      },
      {
        range_name    = "services"
        ip_cidr_range = "10.17.0.0/20"
      }
    ]
  }
}

variable "environment" {
  description = "Environment (dev, prod, etc.)"
  type        = string
}