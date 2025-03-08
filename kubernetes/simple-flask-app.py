from flask import Flask, render_template, jsonify, request
import os
import json
import random
from datetime import datetime, timedelta

app = Flask(__name__)

# Mock data for demonstration
def generate_mock_billing_data():
    services = ["Compute Engine", "Cloud Storage", "BigQuery", "Kubernetes Engine", "Cloud SQL", "Cloud Functions"]
    today = datetime.now()
    data = []
    
    # Generate data for the last 30 days
    for i in range(30):
        date = today - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        
        # Generate daily costs for each service
        service_costs = {}
        for service in services:
            base_cost = random.uniform(5, 20)
            if service == "Kubernetes Engine":
                base_cost *= 3
            elif service == "Compute Engine":
                base_cost *= 5
            
            daily_cost = base_cost * (1 + random.uniform(-0.2, 0.2))
            service_costs[service] = round(daily_cost, 2)
        
        total_cost = sum(service_costs.values())
        data.append({
            "date": date_str,
            "total": round(total_cost, 2),
            "services": service_costs
        })
    
    return data

@app.route('/')
def index():
    return "Cost Optimization Analyzer"

@app.route('/api/billing/daily')
def daily_billing():
    billing_data = generate_mock_billing_data()
    return jsonify(billing_data)

@app.route('/api/recommendations')
def recommendations():
    # Mock recommendations
    return jsonify([
        {
            "category": "Compute Engine",
            "recommendation": "Right-size underutilized instances",
            "potential_savings": "$45.20/month",
            "priority": "High"
        },
        {
            "category": "Kubernetes Engine",
            "recommendation": "Scale down node pools during off-hours",
            "potential_savings": "$32.80/month",
            "priority": "Medium"
        }
    ])

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
