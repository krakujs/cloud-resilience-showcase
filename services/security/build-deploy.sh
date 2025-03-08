#!/bin/bash
set -e

# Variables
PROJECT_ID="cloud-simulation-project"
IMAGE_NAME="security-scanner"
IMAGE_TAG="latest"
GCR_PATH="gcr.io/${PROJECT_ID}/${IMAGE_NAME}:${IMAGE_TAG}"

# Build the Docker image
echo "Building Docker image..."
docker build -t ${GCR_PATH} .

# Push to Google Container Registry
echo "Pushing to Google Container Registry..."
docker push ${GCR_PATH}

# Update the Kubernetes deployment
echo "Updating Kubernetes deployment..."
kubectl apply -f - <<YAML
apiVersion: apps/v1
kind: Deployment
metadata:
  name: security-scanner
  namespace: security
spec:
  replicas: 1
  selector:
    matchLabels:
      app: security-scanner
  template:
    metadata:
      labels:
        app: security-scanner
    spec:
      serviceAccountName: security-scanner-sa
      containers:
      - name: security-scanner
        image: ${GCR_PATH}
        imagePullPolicy: Always
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "1Mi"
            cpu: "1m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 60
          periodSeconds: 15
YAML

# Apply the service
kubectl apply -f - <<YAML
apiVersion: v1
kind: Service
metadata:
  name: security-scanner
  namespace: security
spec:
  selector:
    app: security-scanner
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP
YAML

# Apply the CronJob
kubectl apply -f - <<YAML
apiVersion: batch/v1
kind: CronJob
metadata:
  name: security-scan-trigger
  namespace: security
spec:
  schedule: "0 */6 * * *"  # Every 6 hours
  concurrencyPolicy: Forbid
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: curl
            image: curlimages/curl:7.87.0
            command: ["curl", "-X", "POST", "http://security-scanner/api/scan/start"]
          restartPolicy: OnFailure
YAML

# Make sure the ingress is properly configured
kubectl apply -f - <<YAML
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: security-ingress
  namespace: security
  annotations:
    kubernetes.io/ingress.class: "nginx"
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
spec:
  rules:
  - http:
      paths:
      - path: /security
        pathType: Prefix
        backend:
          service:
            name: security-scanner
            port:
              number: 80
YAML

echo "Deployment complete!"
