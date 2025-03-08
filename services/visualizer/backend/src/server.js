const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const helmet = require('helmet');
const { Pool } = require('pg');
require('dotenv').config();

// Database connection
const pool = new Pool({
  user: process.env.DB_USER || 'crs_user',
  host: process.env.DB_HOST || 'postgres.shared.svc.cluster.local',
  database: process.env.DB_NAME || 'crs_db',
  password: process.env.DB_PASSWORD || 'changeme',
  port: parseInt(process.env.DB_PORT || '5432'),
});

// Initialize express app
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(cors());
app.use(morgan('combined'));
app.use(helmet());

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok' });
});

// Test database connection
app.get('/db-test', async (req, res) => {
  try {
    const result = await pool.query('SELECT NOW()');
    res.status(200).json({ success: true, data: result.rows[0] });
  } catch (error) {
    console.error('Database connection error:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// GCP Resources endpoint (placeholder)
app.get('/api/resources', (req, res) => {
  // This would be replaced with actual GCP API calls
  const mockResources = {
    compute: [
      { id: 'vm-1', name: 'crs-cluster-dev-node-1', type: 'e2-small', zone: 'europe-west9-a' },
      { id: 'vm-2', name: 'crs-cluster-dev-node-2', type: 'e2-small', zone: 'europe-west9-a' }
    ],
    networking: [
      { id: 'net-1', name: 'crs-network-dev', type: 'VPC Network' },
      { id: 'subnet-1', name: 'crs-subnet-dev', type: 'Subnet', cidr: '10.0.0.0/20' }
    ],
    kubernetes: [
      { id: 'gke-1', name: 'crs-cluster-dev', location: 'europe-west9-a', version: '1.27.3-gke.100' }
    ]
  };
  
  res.status(200).json(mockResources);
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
