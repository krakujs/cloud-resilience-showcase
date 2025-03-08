# outputs.tf
output "project_id" {
  description = "The project ID"
  value       = var.project_id
}

output "region" {
  description = "The region used"
  value       = var.region
}

output "kubernetes_cluster_name" {
  description = "The name of the GKE cluster"
  value       = google_container_cluster.primary.name
}

output "kubernetes_cluster_endpoint" {
  description = "The endpoint of the GKE cluster"
  value       = google_container_cluster.primary.endpoint
  sensitive   = true
}

output "kubernetes_cluster_ca_certificate" {
  description = "The CA certificate of the GKE cluster"
  value       = base64decode(
    google_container_cluster.primary.master_auth.0.cluster_ca_certificate
  )
  sensitive   = true
}