const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const axios = require('axios');
const promClient = require('prom-client');

// Create Express app
const app = express();
const port = process.env.PORT || 3000;

// Enable CORS and logging
app.use(cors());
app.use(morgan('combined'));
app.use(express.json());

// Initialize Prometheus metrics
const register = new promClient.Registry();
promClient.collectDefaultMetrics({ register });

// Custom metrics
const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status'],
  buckets: [0.1, 0.3, 0.5, 0.7, 1, 3, 5, 7, 10]
});
register.registerMetric(httpRequestDuration);

// Generate mock cluster metrics
function generateMockClusterMetrics() {
  return {
    cpu: {
      usage: Math.random() * 100,
      capacity: 100,
      trend: Array.from({ length: 24 }, () => Math.random() * 100)
    },
    memory: {
      usage: Math.random() * 100,
      capacity: 100,
      trend: Array.from({ length: 24 }, () => Math.random() * 100)
    },
    storage: {
      usage: Math.random() * 100,
      capacity: 100,
      trend: Array.from({ length: 24 }, () => Math.random() * 100)
    },
    network: {
      inbound: Math.random() * 1000,
      outbound: Math.random() * 1000,
      trend: Array.from({ length: 24 }, () => ({
        inbound: Math.random() * 1000,
        outbound: Math.random() * 1000
      }))
    }
  };
}

// Generate mock service metrics
function generateMockServiceMetrics() {
  const services = ['visualizer', 'chaos-engineering', 'cost-optimization', 'security', 'performance'];
  
  return services.map(service => {
    return {
      name: service,
      status: Math.random() > 0.9 ? 'Warning' : 'Healthy',
      cpu: Math.random() * 100,
      memory: Math.random() * 100,
      latency: Math.random() * 1000,
      requests: Math.floor(Math.random() * 1000),
      errorRate: Math.random() * 5
    };
  });
}

// Generate mock load test results
function generateMockLoadTestResults() {
  return {
    timestamp: new Date().toISOString(),
    duration: 300, // 5 minutes
    concurrentUsers: 100,
    totalRequests: 5000,
    successRate: 98.5,
    averageResponseTime: 245,
    p95ResponseTime: 450,
    p99ResponseTime: 750,
    errors: [
      { code: 500, count: 45, message: 'Internal Server Error' },
      { code: 504, count: 30, message: 'Gateway Timeout' }
    ],
    throughput: 16.7, // requests per second
    breakdown: [
      { endpoint: '/api/resources', count: 1500, avgTime: 200 },
      { endpoint: '/api/metrics', count: 1800, avgTime: 250 },
      { endpoint: '/api/health', count: 1700, avgTime: 150 }
    ]
  };
}

// Routes
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

app.get('/api/cluster/metrics', (req, res) => {
  const metrics = generateMockClusterMetrics();
  res.json(metrics);
});

app.get('/api/services/metrics', (req, res) => {
  const metrics = generateMockServiceMetrics();
  res.json(metrics);
});

app.get('/api/loadtest/results', (req, res) => {
  const results = generateMockLoadTestResults();
  res.json(results);
});

app.post('/api/loadtest/start', (req, res) => {
  // Simulate starting a load test
  setTimeout(() => {
    console.log('Mock load test completed');
  }, 5000);
  
  res.json({
    status: 'started',
    message: 'Load test started',
    estimatedCompletionTime: new Date(Date.now() + 5 * 60 * 1000).toISOString()
  });
});

// Start server
app.listen(port, () => {
  console.log(`Performance Metrics Hub backend running on port ${port}`);
});
