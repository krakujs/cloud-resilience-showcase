# gke.tf - GKE Cluster configuration

# GKE Cluster
resource "google_container_cluster" "primary" {
  name     = "crs-cluster-${var.environment}"
  location = var.zone
  project  = var.project_id

  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true
  initial_node_count       = 1

  # Specify network and subnetwork
  network    = google_compute_network.vpc_network.name
  subnetwork = google_compute_subnetwork.subnet.name

  # Use VPC-native cluster routing (using alias IPs)
  ip_allocation_policy {
    cluster_secondary_range_name  = "pods"
    services_secondary_range_name = "services"
  }

  # Enable network policy for the cluster
  network_policy {
    enabled  = true
    provider = "CALICO"
  }

  # Enable private cluster
  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false
    master_ipv4_cidr_block  = "172.16.0.0/28"
  }

  # Disable basic authentication and client certificate
  master_auth {
    client_certificate_config {
      issue_client_certificate = false
    }
  }

  # Configure master authorized networks (IPs that can access the API server)
  master_authorized_networks_config {
    cidr_blocks {
      cidr_block   = "0.0.0.0/0"
      display_name = "All"
    }
  }

  # Enable Workload Identity
  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  # Enable shielded nodes
  node_config {
    shielded_instance_config {
      enable_secure_boot = true
    }
  }
}

# GKE Node Pool
resource "google_container_node_pool" "primary_nodes" {
  name       = "crs-node-pool"
  location   = var.zone
  cluster    = google_container_cluster.primary.name
  project    = var.project_id
  node_count = 2

  # Enable autoscaling
  autoscaling {
    min_node_count = 2
    max_node_count = 5
  }

  # Configure node management
  management {
    auto_repair  = true
    auto_upgrade = true
  }

  # Node configuration
  node_config {
    preemptible  = true
    machine_type = "e2-small"
    disk_size_gb = 30

    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    service_account = google_service_account.gke_sa.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    # Apply labels to nodes
    labels = {
      environment = var.environment
    }

    # Apply tags to nodes
    tags = ["gke-node", "crs-${var.environment}"]

    # Enable workload identity on the node pool
    workload_metadata_config {
      mode = "GKE_METADATA"
    }

    # Enable shielded nodes
    shielded_instance_config {
      enable_secure_boot = true
    }
  }
}

# GKE Service Account
resource "google_service_account" "gke_sa" {
  account_id   = "gke-sa-${var.environment}"
  display_name = "GKE Service Account for ${var.environment}"
  project      = var.project_id
}

# Grant necessary roles to GKE Service Account
resource "google_project_iam_member" "gke_sa_roles" {
  for_each = toset([
    "roles/container.nodeServiceAccount",
    "roles/logging.logWriter",
    "roles/monitoring.metricWriter",
    "roles/monitoring.viewer",
    "roles/storage.objectViewer"
  ])

  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.gke_sa.email}"
}