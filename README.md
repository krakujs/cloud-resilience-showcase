# Cloud Resilience Simulator

![Cloud Resilience](https://img.shields.io/badge/GCP-Kubernetes-blue)
![Version](https://img.shields.io/badge/version-1.0.0-green)
![License](https://img.shields.io/badge/license-MIT-blue)

A comprehensive Kubernetes-based project deployed on Google Cloud Platform that demonstrates cloud infrastructure resilience, chaos engineering principles, cost optimization, security scanning, and performance monitoring in a microservices architecture.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Core Components](#core-components)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Implementation Phases](#implementation-phases)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
- [Cost Optimization](#cost-optimization)
- [Security Measures](#security-measures)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## 🔭 Project Overview

The Cloud Resilience Simulator is a demonstration project designed to showcase DevOps expertise while optimizing for the $300 GCP credit limit. The project implements a complete microservices architecture with a focus on resilience, security, and cost optimization.

The simulator is built on a foundation of Infrastructure as Code using Terraform, with all components containerized and orchestrated by Kubernetes. The architecture follows best practices for cloud-native applications, including namespace isolation, network policies, resource quotas, and automated cost management.

## 🏗️ Architecture

The Cloud Resilience Simulator employs a microservices architecture running on Google Kubernetes Engine (GKE). The architecture consists of:

- A single GKE cluster with preemptible e2-small nodes
- Multiple namespaces for service isolation
- Shared infrastructure components in a dedicated namespace
- Independent microservices communicating through defined network policies
- Ingress controller for external access

The project is structured with the following organization:

```
cloud-resilience-simulator/
├── terraform/                   # Infrastructure as Code
│   ├── modules/                 # Reusable Terraform modules
│   ├── environments/            # Environment-specific configurations
│   ├── providers.tf             # Provider configurations
│   └── variables.tf             # Input variables
├── kubernetes/                  # Kubernetes manifests
│   ├── namespaces/              # Namespace definitions
│   ├── infrastructure/          # Shared infrastructure resources
│   ├── visualizer/              # Infrastructure Visualizer manifests
│   ├── chaos-engineering/       # Chaos Engineering manifests
│   ├── cost-optimization/       # Cost Optimization manifests
│   ├── security/                # Security Scanner manifests
│   └── performance/             # Performance Metrics manifests
├── services/                    # Microservice source code
│   ├── visualizer/              # Infrastructure Visualizer code
│   ├── chaos-engineering/       # Chaos Engineering code
│   ├── cost-optimization/       # Cost Optimization code
│   ├── security/                # Security Scanner code
│   └── performance/             # Performance Metrics code
├── scripts/                     # Utility scripts
│   ├── setup.sh                 # Environment setup script
│   ├── cleanup.sh               # Resource cleanup script
│   └── demo.sh                  # Demo startup script
└── docs/                        # Project documentation
```

## 🧩 Core Components

The Cloud Resilience Simulator consists of five core microservices, each serving a specific purpose in the demonstration:

1. **Infrastructure Visualizer** (React, D3.js, Node.js)
   - Interactive visualization of GCP infrastructure
   - Resource dependency mapping
   - Configuration viewer

2. **Chaos Engineering Module** (Go, Kubernetes API)
   - Pod termination simulation
   - Network policy restrictions
   - Resource constraints testing

3. **Cost Optimization Analyzer** (Python, Flask)
   - Integration with GCP Billing API
   - Resource utilization visualization
   - Cost projection calculator

4. **Security Posture Scanner** (Python, Kubernetes API)
   - Container vulnerability scanning
   - Kubernetes security posture assessment
   - Compliance checks

5. **Performance Metrics Hub** (Node.js, Vue.js, Chart.js)
   - Real-time metrics visualization
   - Load test controller
   - Horizontal pod autoscaling demonstration

Additionally, shared infrastructure components include:

- **Database**: PostgreSQL deployed as a StatefulSet
- **Observability Stack**: Prometheus and Grafana for monitoring
- **Ingress Layer**: NGINX Ingress Controller
- **CI/CD**: Cloud Build and ArgoCD (in progress)

## ✨ Key Features

- **Infrastructure as Code**: All infrastructure provisioned via Terraform
- **Containerization**: Microservices packaged as Docker containers
- **Orchestration**: Kubernetes for container management
- **Namespace Isolation**: Separate namespaces for each component
- **Network Policies**: Default deny with explicit allow rules
- **Cost Management**: Preemptible instances, resource limits, auto-shutdown
- **Security**: Least privilege approach, regular scanning, network isolation
- **Monitoring**: Prometheus for metrics, Grafana for visualization
- **Resilience Testing**: Chaos engineering principles for reliability

## 💻 Technology Stack

### Infrastructure
- Google Kubernetes Engine (GKE)
- Terraform for Infrastructure as Code
- Virtual Private Cloud (VPC)
- Cloud NAT for outbound traffic
- Service accounts with least privilege

### Frontend Technologies
- React with Hooks
- Vue.js with Composition API
- D3.js for visualizations
- Chart.js for metrics
- Bootstrap for responsive design

### Backend Technologies
- Node.js with Express
- Python with Flask
- Go for performance-critical services
- PostgreSQL database
- RESTful APIs

### DevOps & Observability
- Kubernetes with namespaces
- NGINX Ingress Controller
- Prometheus for metrics
- Grafana for dashboards
- ArgoCD for GitOps deployments

## 🚀 Implementation Phases

The project was implemented in four phases:

### Phase 1: Infrastructure Foundation
- GCP project setup with required APIs
- Terraform foundation setup
- VPC network with subnets and firewall rules
- GKE cluster with preemptible e2-small nodes
- Budget alerts at key thresholds

### Phase 2: Core Infrastructure
- Kubernetes namespace structure with resource quotas
- PostgreSQL database as a StatefulSet
- NGINX Ingress Controller
- Network policies for security isolation

### Phase 3: Microservice Development
- Infrastructure Visualizer with React and Node.js
- Chaos Engineering Module with Go
- Cost Optimization Analyzer with Python Flask
- Security Posture Scanner with Python
- Performance Metrics Hub with Node.js and Vue.js

### Phase 4: Integration and Optimization
- Cross-service API integration
- Resource optimization
- Auto-shutdown mechanisms
- Security hardening
- Landing page development

## 🏁 Getting Started

### Prerequisites

To work with the Cloud Resilience Simulator, you'll need the following tools:

- Google Cloud Platform account with billing enabled
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- [Terraform](https://www.terraform.io/downloads.html) v1.7.5+
- [kubectl](https://kubernetes.io/docs/tasks/tools/) v1.29.2+
- [Helm](https://helm.sh/docs/intro/install/) v3.14.2+ (optional)
- [Docker](https://docs.docker.com/get-docker/)
- [Node.js](https://nodejs.org/) v20.11.x+
- [Python](https://www.python.org/downloads/) v3.10.x+
- [Go](https://golang.org/doc/install) v1.22.1+

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cloud-resilience-simulator.git
   cd cloud-resilience-simulator
   ```

2. Create a GCP project and enable the required APIs:
   ```bash
   # Create a new project
   gcloud projects create PROJECT_ID
   
   # Set the project as the current project
   gcloud config set project PROJECT_ID
   
   # Enable required APIs
   gcloud services enable compute.googleapis.com \
                           container.googleapis.com \
                           containerregistry.googleapis.com \
                           cloudbuild.googleapis.com \
                           monitoring.googleapis.com \
                           logging.googleapis.com \
                           cloudbilling.googleapis.com \
                           secretmanager.googleapis.com \
                           iam.googleapis.com
   ```

3. Create a service account for Terraform:
   ```bash
   # Create a service account
   gcloud iam service-accounts create terraform-sa --display-name="Terraform Service Account"
   
   # Grant the necessary roles
   gcloud projects add-iam-policy-binding PROJECT_ID \
     --member="serviceAccount:terraform-sa@PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/owner"
   
   # Create and download a key
   gcloud iam service-accounts keys create terraform-sa-key.json \
     --iam-account=terraform-sa@PROJECT_ID.iam.gserviceaccount.com
   ```

4. Initialize Terraform:
   ```bash
   cd terraform
   
   # Create a GCS bucket for Terraform state
   gsutil mb -p PROJECT_ID gs://cloud-simulation-project-tf-state
   
   # Initialize Terraform
   terraform init
   ```

5. Deploy the infrastructure:
   ```bash
   terraform apply
   ```

6. Configure kubectl to connect to the cluster:
   ```bash
   gcloud container clusters get-credentials crs-cluster-dev --zone europe-west9-a --project PROJECT_ID
   ```

7. Deploy the Kubernetes components:
   ```bash
   # Create namespaces
   kubectl apply -f kubernetes/namespaces/

   # Deploy shared infrastructure
   kubectl apply -f kubernetes/infrastructure/

   # Deploy microservices
   kubectl apply -f kubernetes/visualizer/
   kubectl apply -f kubernetes/chaos-engineering/
   kubectl apply -f kubernetes/cost-optimization/
   kubectl apply -f kubernetes/security/
   kubectl apply -f kubernetes/performance/

   # Deploy network policies
   kubectl apply -f kubernetes/network-policies/
   ```

### Configuration

1. Update the `variables.tf` file with your specific configuration:
   ```hcl
   variable "project_id" {
     description = "The GCP project ID"
     type        = string
     default     = "your-project-id"
   }
   
   variable "region" {
     description = "The GCP region to deploy resources"
     type        = string
     default     = "europe-west9"  # Paris region
   }
   ```

2. Configure the database secrets:
   ```bash
   kubectl create secret generic postgres-secret \
     --from-literal=username=crs_user \
     --from-literal=password=your-secure-password \
     --from-literal=database=crs_db \
     --from-literal=host=postgres.shared.svc.cluster.local \
     --from-literal=port=5432 \
     -n shared
   ```

3. Set up the landing page:
   ```bash
   kubectl apply -f kubernetes/landing-page.yaml
   ```

## 🖥️ Usage

Once deployed, you can access the different components of the Cloud Resilience Simulator through the ingress endpoint:

1. **Landing Page**: http://your-external-ip/home
2. **Infrastructure Visualizer**: http://your-external-ip/
3. **Chaos Engineering Module**: http://your-external-ip:8080/chaos
4. **Cost Optimization Analyzer**: http://your-external-ip:30081/
5. **Security Posture Scanner**: http://your-external-ip:30082/
6. **Performance Metrics Hub**: http://your-external-ip/performance

You can find the external IP using:
```bash
kubectl get service -n ingress-nginx
```

Each component has its own interface and functionality:

- **Infrastructure Visualizer**: Explore your GCP resources visually.
- **Chaos Engineering Module**: Run controlled chaos experiments to test resilience.
- **Cost Optimization Analyzer**: Monitor and optimize your cloud spending.
- **Security Posture Scanner**: Identify security vulnerabilities in your infrastructure.
- **Performance Metrics Hub**: Monitor and test system performance.

## 💰 Cost Optimization

The Cloud Resilience Simulator is designed to operate within the $300 GCP credit limit through several optimizations:

### Compute Optimization
- Using preemptible e2-small instances for nodes
- Strict resource limits on all deployments
- Auto-scaling with tight constraints
- Daily shutdown of non-essential services

### Storage Optimization
- Minimal persistent volumes (1Gi for database)
- Short retention period for logs and metrics
- Efficient container images
- Regular cleanup of unused resources

### Network Optimization
- Single region deployment
- Shared ingress controller
- Minimized external traffic
- Efficient internal communication

### Cost Breakdown
- GKE Cluster (3 e2-small preemptible nodes): ~$60/month
- Persistent Storage (10GB): ~$2/month
- Load Balancer: ~$18/month
- Network Traffic: ~$10/month
- Other Services: ~$10/month
- Total Estimated Monthly Cost: ~$100/month

## 🔒 Security Measures

Security is implemented through multiple layers:

### Network Security
- Default deny-all network policies
- Namespace isolation
- Strict ingress rules
- Private GKE cluster configuration

### Authentication & Authorization
- Service accounts with least privilege
- RBAC for Kubernetes resources
- Secure management of secrets
- Regular credential rotation

### Container Security
- Regular vulnerability scanning
- Minimal base images
- No privileged containers
- Read-only file systems where possible

## 🤝 Contributing

Contributions to the Cloud Resilience Simulator are welcome! To contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please make sure to update tests and documentation as appropriate.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📬 Contact

Ujjwal Solanki - [ujjwalsolanki2001@gmail.com](mailto:ujjwalsolanki2001@gmail.com)

Project Link: [https://github.com/krakujs/cloud-resilience-showcase](https://github.com/krakujs/cloud-resilience-showcase)
