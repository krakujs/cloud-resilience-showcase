#!/bin/bash
# Startup script to restore services

# Define namespaces
NAMESPACES=("visualizer" "chaos-engineering" "cost-optimization" "security" "performance")

# Scale up deployments
for ns in "${NAMESPACES[@]}"
do
  echo "Scaling up deployments in namespace: $ns"
  kubectl scale deployment --all --replicas=1 -n $ns
done

echo "All services have been started"

# Log the startup
echo "Services started at $(date)" >> /var/log/auto-startup.log

# Schedule shutdown after 8 hours
echo "Scheduling shutdown after 8 hours"
at now + 8 hours -f $(dirname "$0")/auto-shutdown.sh
