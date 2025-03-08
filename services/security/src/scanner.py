import os
import time
import yaml
import json
import datetime
import logging
import kubernetes
from flask import Flask, jsonify, render_template, request
import threading
import schedule

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('security-scanner')

# Initialize Flask app with absolute template paths
app = Flask(__name__, 
            template_folder='/app/templates',
            static_folder='/app/static')

# Global variables
vulnerabilities = []
scan_in_progress = False
last_scan_time = None

# Security rules
SECURITY_RULES = [
    {
        "id": "SEC-K8S-001",
        "name": "Privileged Containers",
        "description": "Containers should not run in privileged mode",
        "severity": "HIGH",
        "category": "Pod Security",
        "check": lambda pod: any(
            container.get('securityContext', {}).get('privileged', False) 
            for container in pod.spec.containers
        )
    },
    {
        "id": "SEC-K8S-002",
        "name": "Root User",
        "description": "Containers should not run as root user",
        "severity": "MEDIUM",
        "category": "Pod Security",
        "check": lambda pod: any(
            not container.get('securityContext', {}).get('runAsNonRoot', False)
            for container in pod.spec.containers
        )
    },
    {
        "id": "SEC-K8S-003",
        "name": "Read-only Root Filesystem",
        "description": "Containers should use read-only root filesystem",
        "severity": "MEDIUM",
        "category": "Pod Security",
        "check": lambda pod: any(
            not container.get('securityContext', {}).get('readOnlyRootFilesystem', False)
            for container in pod.spec.containers
        )
    },
    {
        "id": "SEC-K8S-004",
        "name": "Resource Limits",
        "description": "Containers should have CPU and memory limits",
        "severity": "MEDIUM",
        "category": "Resource Management",
        "check": lambda pod: any(
            not container.get('resources', {}).get('limits') or
            'cpu' not in container.get('resources', {}).get('limits', {}) or
            'memory' not in container.get('resources', {}).get('limits', {})
            for container in pod.spec.containers
        )
    },
    {
        "id": "SEC-K8S-005",
        "name": "Default Namespace",
        "description": "Pods should not be deployed in the default namespace",
        "severity": "LOW",
        "category": "Namespace Management",
        "check": lambda pod: pod.metadata.namespace == 'default'
    },
    {
        "id": "SEC-K8S-006",
        "name": "Latest Tag",
        "description": "Container images should not use the 'latest' tag",
        "severity": "MEDIUM",
        "category": "Image Management",
        "check": lambda pod: any(
            container.image.endswith(':latest') or ':' not in container.image
            for container in pod.spec.containers
        )
    }
]

def connect_to_kubernetes():
    """Connect to Kubernetes API server"""
    try:
        # Try in-cluster config first
        kubernetes.config.load_incluster_config()
        logger.info("Using in-cluster Kubernetes configuration")
    except kubernetes.config.config_exception.ConfigException:
        # Fall back to kubeconfig file
        kubernetes.config.load_kube_config()
        logger.info("Using kubeconfig file for Kubernetes configuration")
    
    return kubernetes.client.CoreV1Api(), kubernetes.client.AppsV1Api()

def scan_pod(core_v1, pod, namespace):
    """Scan a pod for security vulnerabilities"""
    results = []
    
    for rule in SECURITY_RULES:
        try:
            if rule["check"](pod):
                results.append({
                    "rule_id": rule["id"],
                    "rule_name": rule["name"],
                    "description": rule["description"],
                    "severity": rule["severity"],
                    "category": rule["category"],
                    "resource_type": "Pod",
                    "resource_name": pod.metadata.name,
                    "namespace": namespace
                })
        except Exception as e:
            logger.error(f"Error checking rule {rule['id']} on pod {pod.metadata.name}: {e}")
    
    return results

def scan_deployment(apps_v1, deployment, namespace):
    """Scan a deployment for security vulnerabilities"""
    results = []
    
    # For simplicity, we'll just check the pod template
    pod_template = kubernetes.client.V1Pod(
        metadata=deployment.spec.template.metadata,
        spec=deployment.spec.template.spec
    )
    
    for rule in SECURITY_RULES:
        try:
            if rule["check"](pod_template):
                results.append({
                    "rule_id": rule["id"],
                    "rule_name": rule["name"],
                    "description": rule["description"],
                    "severity": rule["severity"],
                    "category": rule["category"],
                    "resource_type": "Deployment",
                    "resource_name": deployment.metadata.name,
                    "namespace": namespace
                })
        except Exception as e:
            logger.error(f"Error checking rule {rule['id']} on deployment {deployment.metadata.name}: {e}")
    
    return results

def run_security_scan():
    """Run a full security scan on the cluster"""
    global vulnerabilities, scan_in_progress, last_scan_time
    
    if scan_in_progress:
        logger.info("Scan already in progress, skipping")
        return
    
    scan_in_progress = True
    scan_start_time = datetime.datetime.now()
    logger.info(f"Starting security scan at {scan_start_time}")
    
    try:
        core_v1, apps_v1 = connect_to_kubernetes()
        results = []
        
        # Scan all namespaces
        namespaces = core_v1.list_namespace()
        
        for ns in namespaces.items:
            namespace = ns.metadata.name
            logger.info(f"Scanning namespace: {namespace}")
            
            # Scan pods
            pods = core_v1.list_namespaced_pod(namespace)
            for pod in pods.items:
                pod_results = scan_pod(core_v1, pod, namespace)
                results.extend(pod_results)
            
            # Scan deployments
            deployments = apps_v1.list_namespaced_deployment(namespace)
            for deployment in deployments.items:
                deployment_results = scan_deployment(apps_v1, deployment, namespace)
                results.extend(deployment_results)
        
        # Update vulnerabilities
        vulnerabilities = results
        last_scan_time = scan_start_time
        
        # Save report
        report = {
            "scan_time": scan_start_time.isoformat(),
            "vulnerabilities": results,
            "summary": {
                "total": len(results),
                "by_severity": {
                    "HIGH": len([r for r in results if r["severity"] == "HIGH"]),
                    "MEDIUM": len([r for r in results if r["severity"] == "MEDIUM"]),
                    "LOW": len([r for r in results if r["severity"] == "LOW"])
                },
                "by_category": {}
            }
        }
        
        # Calculate category summary
        categories = set(r["category"] for r in results)
        for category in categories:
            report["summary"]["by_category"][category] = len([r for r in results if r["category"] == category])
        
        # Save to file
        os.makedirs("reports", exist_ok=True)
        with open(f"reports/scan_{scan_start_time.strftime('%Y%m%d%H%M%S')}.json", "w") as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Security scan completed. Found {len(results)} vulnerabilities.")
    
    except Exception as e:
        logger.error(f"Error during security scan: {e}")
    
    finally:
        scan_in_progress = False

def start_scheduler():
    """Start the scheduler for periodic scans"""
    schedule.every(6).hours.do(run_security_scan)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

# Mock data for initial testing
def generate_mock_data():
    global vulnerabilities, last_scan_time
    
    last_scan_time = datetime.datetime.now()
    vulnerabilities = [
        {
            "rule_id": "SEC-K8S-001",
            "rule_name": "Privileged Containers",
            "description": "Containers should not run in privileged mode",
            "severity": "HIGH",
            "category": "Pod Security",
            "resource_type": "Pod",
            "resource_name": "nginx-pod",
            "namespace": "default"
        },
        {
            "rule_id": "SEC-K8S-004",
            "rule_name": "Resource Limits",
            "description": "Containers should have CPU and memory limits",
            "severity": "MEDIUM",
            "category": "Resource Management",
            "resource_type": "Deployment",
            "resource_name": "frontend",
            "namespace": "visualizer"
        },
        {
            "rule_id": "SEC-K8S-006",
            "rule_name": "Latest Tag",
            "description": "Container images should not use the 'latest' tag",
            "severity": "MEDIUM",
            "category": "Image Management",
            "resource_type": "Deployment",
            "resource_name": "backend",
            "namespace": "visualizer"
        }
    ]

# API routes
@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"})

@app.route('/api/scan')
def get_scan_results():
    """Get the results of the latest scan"""
    return jsonify({
        "last_scan_time": last_scan_time.isoformat() if last_scan_time else None,
        "vulnerabilities": vulnerabilities,
        "summary": {
            "total": len(vulnerabilities),
            "by_severity": {
                "HIGH": len([v for v in vulnerabilities if v["severity"] == "HIGH"]),
                "MEDIUM": len([v for v in vulnerabilities if v["severity"] == "MEDIUM"]),
                "LOW": len([v for v in vulnerabilities if v["severity"] == "LOW"])
            }
        }
    })

@app.route('/api/scan/start', methods=['POST'])
def start_scan():
    """Start a new security scan"""
    global scan_in_progress
    
    if scan_in_progress:
        return jsonify({"status": "error", "message": "Scan already in progress"}), 409
    
    # Start scan in a separate thread
    threading.Thread(target=run_security_scan).start()
    
    return jsonify({
        "status": "started",
        "message": "Security scan started"
    })

@app.route('/')
@app.route('/')
def index():
    """Main page"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering template: {e}")
        return """
        <!DOCTYPE html>
        <html>
        <head>
          <title>Security Posture Scanner</title>
          <style>
            body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
            h1 { color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }
            .container { max-width: 1200px; margin: 0 auto; }
            .card { background-color: #fff; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 20px; padding: 20px; }
            .summary { display: flex; flex-wrap: wrap; justify-content: space-between; margin-bottom: 20px; }
            .summary-item { text-align: center; flex: 1; min-width: 120px; padding: 15px; }
            .count { font-size: 32px; font-weight: bold; margin-bottom: 5px; }
            .severity-high { color: #f44336; }
            .severity-medium { color: #ff9800; }
            .severity-low { color: #4CAF50; }
            table { width: 100%; border-collapse: collapse; }
            th, td { text-align: left; padding: 12px; border-bottom: 1px solid #ddd; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #f9f9f9; }
            .badge { padding: 5px 10px; border-radius: 4px; font-size: 12px; font-weight: bold; color: white; }
            .badge-high { background-color: #f44336; }
            .badge-medium { background-color: #ff9800; }
            .badge-low { background-color: #4CAF50; }
            .actions { margin-top: 20px; }
            .btn { padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; }
            .btn-primary { background-color: #4CAF50; color: white; }
            .btn-primary:hover { background-color: #45a049; }
            #loading { display: none; margin-left: 10px; }
          </style>
        </head>
        <body>
          <div class="container">
            <h1>Security Posture Scanner</h1>
            
            <div class="card">
              <h2>Summary</h2>
              <div class="summary">
                <div class="summary-item">
                  <div class="count" id="total-count">3</div>
                  <div>Total Issues</div>
                </div>
                <div class="summary-item">
                  <div class="count severity-high" id="high-count">1</div>
                  <div>High Severity</div>
                </div>
                <div class="summary-item">
                  <div class="count severity-medium" id="medium-count">2</div>
                  <div>Medium Severity</div>
                </div>
                <div class="summary-item">
                  <div class="count severity-low" id="low-count">0</div>
                  <div>Low Severity</div>
                </div>
              </div>
              <div>
                <strong>Last Scan:</strong> <span id="last-scan-time">March 8, 2025</span>
              </div>
            </div>
            
            <div class="card">
              <h2>Vulnerabilities</h2>
              <table>
                <thead>
                  <tr>
                    <th>Rule</th>
                    <th>Resource</th>
                    <th>Namespace</th>
                    <th>Severity</th>
                    <th>Category</th>
                  </tr>
                </thead>
                <tbody id="vulnerabilities-table">
                  <tr>
                    <td><strong>Privileged Containers</strong><br><small>Containers should not run in privileged mode</small></td>
                    <td>Pod: nginx-pod</td>
                    <td>default</td>
                    <td><span class="badge badge-high">HIGH</span></td>
                    <td>Pod Security</td>
                  </tr>
                  <tr>
                    <td><strong>Resource Limits</strong><br><small>Containers should have CPU and memory limits</small></td>
                    <td>Deployment: frontend</td>
                    <td>visualizer</td>
                    <td><span class="badge badge-medium">MEDIUM</span></td>
                    <td>Resource Management</td>
                  </tr>
                  <tr>
                    <td><strong>Latest Tag</strong><br><small>Container images should not use the latest tag</small></td>
                    <td>Deployment: backend</td>
                    <td>visualizer</td>
                    <td><span class="badge badge-medium">MEDIUM</span></td>
                    <td>Image Management</td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <div class="actions">
              <button id="scan-button" class="btn btn-primary">Start New Scan</button>
              <span id="loading">Scanning...</span>
            </div>
          </div>

          <script>
            document.getElementById('scan-button').addEventListener('click', function() {
              this.disabled = true;
              document.getElementById('loading').style.display = 'inline';
              
              fetch('/api/scan/start', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                }
              })
              .then(response => response.json())
              .then(data => {
                alert('Security scan started!');
                setTimeout(() => {
                  location.reload();
                }, 3000);
              })
              .catch(error => {
                console.error('Error:', error);
                this.disabled = false;
                document.getElementById('loading').style.display = 'none';
              });
            });
            
            // Load real data from API
            fetch('/api/scan')
              .then(response => response.json())
              .then(data => {
                // Update summary counts
                document.getElementById('total-count').textContent = data.summary.total;
                document.getElementById('high-count').textContent = data.summary.by_severity.HIGH;
                document.getElementById('medium-count').textContent = data.summary.by_severity.MEDIUM;
                document.getElementById('low-count').textContent = data.summary.by_severity.LOW;
                
                // Update last scan time
                if (data.last_scan_time) {
                  const date = new Date(data.last_scan_time);
                  document.getElementById('last-scan-time').textContent = date.toLocaleString();
                }
                
                // Update vulnerabilities table
                if (data.vulnerabilities && data.vulnerabilities.length > 0) {
                  const tbody = document.getElementById('vulnerabilities-table');
                  tbody.innerHTML = '';
                  
                  data.vulnerabilities.forEach(vuln => {
                    const row = document.createElement('tr');
                    
                    const ruleCell = document.createElement('td');
                    ruleCell.innerHTML = '<strong>' + vuln.rule_name + '</strong><br><small>' + vuln.description + '</small>';
                    row.appendChild(ruleCell);
                    
                    const resourceCell = document.createElement('td');
                    resourceCell.textContent = vuln.resource_type + ': ' + vuln.resource_name;
                    row.appendChild(resourceCell);
                    
                    const namespaceCell = document.createElement('td');
                    namespaceCell.textContent = vuln.namespace;
                    row.appendChild(namespaceCell);
                    
                    const severityCell = document.createElement('td');
                    const severityBadge = document.createElement('span');
                    severityBadge.textContent = vuln.severity;
                    severityBadge.className = 'badge badge-' + vuln.severity.toLowerCase();
                    severityCell.appendChild(severityBadge);
                    row.appendChild(severityCell);
                    
                    const categoryCell = document.createElement('td');
                    categoryCell.textContent = vuln.category;
                    row.appendChild(categoryCell);
                    
                    tbody.appendChild(row);
                  });
                }
              })
              .catch(error => console.error('Error loading data:', error));
          </script>
        </body>
        </html>
        """

if __name__ == "__main__":
    # Generate mock data for initial testing
    generate_mock_data()
    
    # Start scheduler in a separate thread
    scheduler_thread = threading.Thread(target=start_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    # List all directories to debug
    logger.info(f"Current directory: {os.getcwd()}")
    logger.info(f"Directory contents: {os.listdir('.')}")
    if os.path.exists('/app/templates'):
        logger.info(f"Templates directory exists, contents: {os.listdir('/app/templates')}")
    else:
        logger.info("Templates directory does not exist")
    
    # Start the Flask app
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)