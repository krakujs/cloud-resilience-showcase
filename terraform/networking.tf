# networking.tf - VPC and Subnet resources

# VPC Network
resource "google_compute_network" "vpc_network" {
  name                    = "crs-network-${var.environment}"
  auto_create_subnetworks = false
  project                 = var.project_id
}

# Subnet
resource "google_compute_subnetwork" "subnet" {
  name          = "crs-subnet-${var.environment}"
  ip_cidr_range = "10.0.0.0/20"
  region        = var.region
  network       = google_compute_network.vpc_network.self_link
  project       = var.project_id

  # Enable private Google access to allow services to connect without external IPs
  private_ip_google_access = true

  # Secondary IP ranges for GKE pods and services
  secondary_ip_range {
    range_name    = "pods"
    ip_cidr_range = "10.16.0.0/16"
  }

  secondary_ip_range {
    range_name    = "services"
    ip_cidr_range = "10.17.0.0/20"
  }
}

# Firewall rule to allow internal communication
resource "google_compute_firewall" "allow_internal" {
  name    = "allow-internal"
  project = var.project_id
  network = google_compute_network.vpc_network.self_link

  allow {
    protocol = "icmp"
  }

  allow {
    protocol = "tcp"
  }

  allow {
    protocol = "udp"
  }

  source_ranges = ["10.0.0.0/20"]
}

# Firewall rule to allow SSH access (for debugging purposes)
resource "google_compute_firewall" "allow_ssh" {
  name    = "allow-ssh"
  project = var.project_id
  network = google_compute_network.vpc_network.self_link

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["ssh"]
}

# Cloud NAT router for outbound internet access without external IPs
resource "google_compute_router" "router" {
  name    = "crs-router-${var.environment}"
  region  = var.region
  network = google_compute_network.vpc_network.self_link
  project = var.project_id
}

# # Cloud NAT configuration
# resource "google_compute_router_nat" "nat" {
#   name                               = "crs-nat-${var.environment}"
#   router                             = google_compute_router.router.name
#   region                             = var.region
#   nat_ip_allocate_option             = "AUTO_ONLY"
#   source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
#   project                            = var.project_id

#   log_config {
#     enable = true
#     filter = "ERRORS_ONLY"
#   }
# }