# modules/networking/main.tf
resource "google_compute_network" "vpc_network" {
  name                    = var.network_name
  auto_create_subnetworks = false
  project                 = var.project_id
}

resource "google_compute_subnetwork" "subnet" {
  name          = var.subnet_name
  ip_cidr_range = var.subnet_cidr
  region        = var.region
  network       = google_compute_network.vpc_network.self_link
  project       = var.project_id

  # Enable private Google access to allow services to connect without external IPs
  private_ip_google_access = true

  # Secondary IP ranges for GKE pods and services
  dynamic "secondary_ip_range" {
    for_each = lookup(var.secondary_ranges, var.subnet_name, [])
    content {
      range_name    = secondary_ip_range.value.range_name
      ip_cidr_range = secondary_ip_range.value.ip_cidr_range
    }
  }

  # Add lifecycle rule to preserve secondary ranges
  lifecycle {
    ignore_changes = [secondary_ip_range]
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

  source_ranges = [var.subnet_cidr]
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
  name    = "${var.network_name}-router"
  region  = var.region
  network = google_compute_network.vpc_network.self_link
  project = var.project_id
}

# Cloud NAT configuration
resource "google_compute_router_nat" "nat" {
  name                               = "${var.network_name}-nat"
  router                             = google_compute_router.router.name
  region                             = var.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
  project                            = var.project_id

  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}