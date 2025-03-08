# environments/dev/main.tf
module "networking" {
  source      = "../../modules/networking"
  project_id  = var.project_id
  region      = var.region
  environment = var.environment

  network_name = "crs-network-${var.environment}"
  subnet_name  = "crs-subnet-${var.environment}"
  subnet_cidr  = "10.0.0.0/20"
  
  secondary_ranges = {
    "crs-subnet-${var.environment}" = [
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