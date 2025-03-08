#!/bin/bash
# Auto-shutdown script for non-essential services during inactive hours

# Define namespaces for non-essential services
NAMESPACES=("visualizer" "chaos-engineering" "cost-optimization" "security" "performance")

# Scale down deployments
for ns in "${NAMESPACES[@]}"
do
  echo "Scaling down deployments in namespace: $ns"
  kubectl scale deployment --all --replicas=0 -n $ns
done

echo "Only essential services in shared namespace are kept running"
echo "To restart services, run the startup script"

# Log the shutdown
echo "Services scaled down at $(date)" >> /var/log/auto-shutdown.log
