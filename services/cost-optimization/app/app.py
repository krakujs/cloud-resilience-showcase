from flask import Flask, render_template, jsonify, request
import os
import json
from datetime import datetime, timedelta
import random

app = Flask(__name__, 
            static_folder='../static',
            template_folder='../templates')

# Mock data for demonstration
def generate_mock_billing_data():
    services = [
        "Compute Engine", 
        "Cloud Storage", 
        "BigQuery", 
        "Kubernetes Engine", 
        "Cloud SQL", 
        "Cloud Functions"
    ]
    
    today = datetime.now()
    data = []
    
    # Generate data for the last 30 days
    for i in range(30):
        date = today - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        
        # Generate daily costs for each service
        service_costs = {}
        for service in services:
            # Add some variability and trends
            base_cost = random.uniform(5, 20)
            if service == "Kubernetes Engine":
                # GKE costs are higher
                base_cost *= 3
            elif service == "Compute Engine":
                # Compute Engine is our biggest expense
                base_cost *= 5
            
            # Weekday vs. weekend pattern
            if date.weekday() >= 5:  # Weekend
                base_cost *= 0.7
                
            # Add some randomness
            daily_cost = base_cost * (1 + random.uniform(-0.2, 0.2))
            service_costs[service] = round(daily_cost, 2)
        
        # Total cost for the day
        total_cost = sum(service_costs.values())
        
        data.append({
            "date": date_str,
            "total": round(total_cost, 2),
            "services": service_costs
        })
    
    return data

# Generate optimization recommendations
def generate_recommendations():
    return [
        {
            "category": "Compute Engine",
            "recommendation": "Right-size underutilized instances",
            "potential_savings": "$45.20/month",
            "priority": "High"
        },
        {
            "category": "Kubernetes Engine",
            "recommendation": "Scale down preemptible node pools during non-business hours",
            "potential_savings": "$32.80/month",
            "priority": "Medium"
        },
        {
            "category": "Cloud Storage",
            "recommendation": "Move infrequently accessed data to Nearline storage",
            "potential_savings": "$18.90/month",
            "priority": "Medium"
        },
        {
            "category": "Compute Engine",
            "recommendation": "Use committed use discounts for stable workloads",
            "potential_savings": "$78.60/month",
            "priority": "High"
        },
        {
            "category": "BigQuery",
            "recommendation": "Optimize query patterns to reduce data processed",
            "potential_savings": "$15.40/month",
            "priority": "Low"
        }
    ]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/billing/daily')
def daily_billing():
    billing_data = generate_mock_billing_data()
    return jsonify(billing_data)

@app.route('/api/recommendations')
def recommendations():
    return jsonify(generate_recommendations())

@app.route('/api/utilization')
def utilization():
    # Mock resource utilization data
    services = ["visualizer", "chaos-engineering", "cost-optimization", "security", "performance"]
    metrics = ["CPU", "Memory", "Storage", "Network"]
    
    data = {}
    for service in services:
        data[service] = {}
        for metric in metrics:
            # Generate a percentage between 10% and 90%
            data[service][metric] = round(random.uniform(10, 90), 1)
    
    return jsonify(data)

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
