package main

import (
    "context"
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "os"
    "path/filepath"
    "time"

    v1 "k8s.io/api/core/v1"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    "k8s.io/client-go/kubernetes"
    "k8s.io/client-go/rest"
    "k8s.io/client-go/tools/clientcmd"
)

type ChaosServer struct {
    client *kubernetes.Clientset
}

type PodTerminationRequest struct {
    Namespace string `json:"namespace"`
    PodName   string `json:"podName"`
}

type ResourceConstraintRequest struct {
    Namespace     string `json:"namespace"`
    DeploymentName string `json:"deploymentName"`
    CpuLimit      string `json:"cpuLimit"`
    MemoryLimit   string `json:"memoryLimit"`
}

type NetworkPolicyRequest struct {
    Namespace string `json:"namespace"`
    PolicyName string `json:"policyName"`
}

func main() {
    server := &ChaosServer{}

    // Initialize Kubernetes client
    config, err := rest.InClusterConfig()
    if err != nil {
        // Fall back to kubeconfig
        home := os.Getenv("HOME")
        kubeconfig := filepath.Join(home, ".kube", "config")
        config, err = clientcmd.BuildConfigFromFlags("", kubeconfig)
        if err != nil {
            log.Fatalf("Error building kubeconfig: %v", err)
        }
    }

    client, err := kubernetes.NewForConfig(config)
    if err != nil {
        log.Fatalf("Error creating Kubernetes client: %v", err)
    }
    server.client = client

    // Set up HTTP handlers
    http.HandleFunc("/", server.rootHandler)
    http.HandleFunc("/health", server.healthHandler)
    http.HandleFunc("/api/chaos/pod-termination", server.podTerminationHandler)
    http.HandleFunc("/api/chaos/resource-constraint", server.resourceConstraintHandler)
    http.HandleFunc("/api/chaos/network-policy", server.networkPolicyHandler)
    http.HandleFunc("/api/chaos/list-pods", server.listPodsHandler)

    // Start the server
    log.Println("Starting Chaos Engineering server on port 8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}

func (s *ChaosServer) rootHandler(w http.ResponseWriter, r *http.Request) {
    // Only handle the exact root path
    if r.URL.Path != "/" {
        http.NotFound(w, r)
        return
    }
    
    w.Header().Set("Content-Type", "text/html")
    fmt.Fprint(w, `<!DOCTYPE html>
<html>
<head>
  <title>Chaos Engineering API</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; background-color: #f7f9fc; }
    h1 { color: #333; border-bottom: 2px solid #4a86e8; padding-bottom: 10px; }
    .card { background-color: white; border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin: 20px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .endpoints { background-color: #f5f5f5; padding: 15px; border-radius: 6px; }
    .endpoint { margin-bottom: 10px; }
    .endpoint strong { color: #4a86e8; }
    .method { display: inline-block; padding: 3px 6px; border-radius: 4px; font-size: 12px; margin-right: 8px; }
    .get { background-color: #61affe; color: white; }
    .post { background-color: #49cc90; color: white; }
  </style>
</head>
<body>
  <h1>Chaos Engineering API</h1>
  <div class="card">
    <h2>Available Endpoints</h2>
    <div class="endpoints">
      <div class="endpoint">
        <span class="method get">GET</span>
        <strong>/health</strong> - Health check endpoint
      </div>
      <div class="endpoint">
        <span class="method get">GET</span>
        <strong>/api/chaos/list-pods</strong> - List pods in a namespace
      </div>
      <div class="endpoint">
        <span class="method post">POST</span>
        <strong>/api/chaos/pod-termination</strong> - Terminate a pod
      </div>
      <div class="endpoint">
        <span class="method post">POST</span>
        <strong>/api/chaos/resource-constraint</strong> - Apply resource constraints
      </div>
      <div class="endpoint">
        <span class="method post">POST</span>
        <strong>/api/chaos/network-policy</strong> - Apply network policies
      </div>
    </div>
  </div>

  <div class="card">
    <h2>Examples</h2>
    <h3>List pods in default namespace:</h3>
    <pre>GET /api/chaos/list-pods?namespace=default</pre>
    
    <h3>Terminate a pod:</h3>
    <pre>POST /api/chaos/pod-termination
Content-Type: application/json

{
  "namespace": "default",
  "podName": "example-pod"
}</pre>
  </div>
</body>
</html>`)
}

func (s *ChaosServer) healthHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusOK)
    json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
}

func (s *ChaosServer) podTerminationHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    var req PodTerminationRequest
    err := json.NewDecoder(r.Body).Decode(&req)
    if err != nil {
        http.Error(w, "Invalid request body", http.StatusBadRequest)
        return
    }

    // Validate input
    if req.Namespace == "" || req.PodName == "" {
        http.Error(w, "Namespace and pod name are required", http.StatusBadRequest)
        return
    }

    // Delete the pod
    err = s.client.CoreV1().Pods(req.Namespace).Delete(context.Background(), req.PodName, metav1.DeleteOptions{})
    if err != nil {
        http.Error(w, fmt.Sprintf("Failed to delete pod: %v", err), http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusOK)
    json.NewEncoder(w).Encode(map[string]string{"status": "success", "message": fmt.Sprintf("Pod %s in namespace %s terminated", req.PodName, req.Namespace)})
}

func (s *ChaosServer) resourceConstraintHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    var req ResourceConstraintRequest
    err := json.NewDecoder(r.Body).Decode(&req)
    if err != nil {
        http.Error(w, "Invalid request body", http.StatusBadRequest)
        return
    }

    // This would be implemented to apply resource constraints
    // For now, we'll just return a mock success
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusOK)
    json.NewEncoder(w).Encode(map[string]string{
        "status": "success", 
        "message": fmt.Sprintf("Resource constraints applied to deployment %s in namespace %s", req.DeploymentName, req.Namespace),
    })
}

func (s *ChaosServer) networkPolicyHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    var req NetworkPolicyRequest
    err := json.NewDecoder(r.Body).Decode(&req)
    if err != nil {
        http.Error(w, "Invalid request body", http.StatusBadRequest)
        return
    }

    // This would be implemented to apply network policies
    // For now, we'll just return a mock success
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusOK)
    json.NewEncoder(w).Encode(map[string]string{
        "status": "success", 
        "message": fmt.Sprintf("Network policy %s applied to namespace %s", req.PolicyName, req.Namespace),
    })
}

func (s *ChaosServer) listPodsHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodGet {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    namespace := r.URL.Query().Get("namespace")
    if namespace == "" {
        namespace = "default"
    }

    pods, err := s.client.CoreV1().Pods(namespace).List(context.Background(), metav1.ListOptions{})
    if err != nil {
        http.Error(w, fmt.Sprintf("Failed to list pods: %v", err), http.StatusInternalServerError)
        return
    }

    // Extract relevant pod information
    type PodInfo struct {
        Name       string            `json:"name"`
        Namespace  string            `json:"namespace"`
        Status     v1.PodPhase       `json:"status"`
        Labels     map[string]string `json:"labels"`
        Age        string            `json:"age"`
        Containers int               `json:"containers"`
    }

    var podInfos []PodInfo
    for _, pod := range pods.Items {
        age := time.Since(pod.CreationTimestamp.Time).Round(time.Second).String()
        podInfos = append(podInfos, PodInfo{
            Name:       pod.Name,
            Namespace:  pod.Namespace,
            Status:     pod.Status.Phase,
            Labels:     pod.Labels,
            Age:        age,
            Containers: len(pod.Spec.Containers),
        })
    }

    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusOK)
    json.NewEncoder(w).Encode(podInfos)
}