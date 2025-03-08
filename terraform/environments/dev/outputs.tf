# environments/dev/outputs.tf
output "network_name" {
  description = "The name of the VPC network"
  value       = module.networking.network_name
}

output "subnet_name" {
  description = "The name of the subnet"
  value       = module.networking.subnet_name
}

output "subnet_cidr" {
  description = "The CIDR range of the subnet"
  value       = module.networking.subnet_cidr
}