# modules/networking/outputs.tf
output "network_id" {
  description = "The ID of the VPC network"
  value       = google_compute_network.vpc_network.id
}

output "network_name" {
  description = "The name of the VPC network"
  value       = google_compute_network.vpc_network.name
}

output "network_self_link" {
  description = "The self link of the VPC network"
  value       = google_compute_network.vpc_network.self_link
}

output "subnet_id" {
  description = "The ID of the subnet"
  value       = google_compute_subnetwork.subnet.id
}

output "subnet_name" {
  description = "The name of the subnet"
  value       = google_compute_subnetwork.subnet.name
}

output "subnet_self_link" {
  description = "The self link of the subnet"
  value       = google_compute_subnetwork.subnet.self_link
}

output "subnet_cidr" {
  description = "The CIDR range of the subnet"
  value       = google_compute_subnetwork.subnet.ip_cidr_range
}

output "subnet_region" {
  description = "The region of the subnet"
  value       = google_compute_subnetwork.subnet.region
}

output "gke_pods_range_name" {
  description = "The name of the secondary range for GKE pods"
  value       = var.secondary_ranges[var.subnet_name][0].range_name
}

output "gke_services_range_name" {
  description = "The name of the secondary range for GKE services"
  value       = var.secondary_ranges[var.subnet_name][1].range_name
}