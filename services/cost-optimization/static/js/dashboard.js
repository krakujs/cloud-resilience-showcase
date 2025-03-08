document.addEventListener('DOMContentLoaded', function() {
    // Fetch billing data
    fetch('/api/billing/daily')
        .then(response => response.json())
        .then(data => {
            updateBillingChart(data);
            updateSpendingSummary(data);
        })
        .catch(error => console.error('Error fetching billing data:', error));

    // Fetch recommendations
    fetch('/api/recommendations')
        .then(response => response.json())
        .then(data => {
            updateRecommendations(data);
            updatePotentialSavings(data);
        })
        .catch(error => console.error('Error fetching recommendations:', error));

    // Fetch utilization data
    fetch('/api/utilization')
        .then(response => response.json())
        .then(data => {
            updateUtilization(data);
        })
        .catch(error => console.error('Error fetching utilization data:', error));
});

function updateBillingChart(data) {
    // Prepare data for the chart
    const dates = data.map(item => item.date).reverse();
    const totals = data.map(item => item.total).reverse();
    
    // Get service names
    const services = Object.keys(data[0].services);
    
    // Prepare datasets
    const serviceData = {};
    services.forEach(service => {
        serviceData[service] = data.map(item => item.services[service]).reverse();
    });
    
    // Create datasets for stacked chart
    const datasets = services.map((service, index) => {
        const colors = [
            'rgba(255, 99, 132, 0.7)',
            'rgba(54, 162, 235, 0.7)',
            'rgba(255, 206, 86, 0.7)',
            'rgba(75, 192, 192, 0.7)',
            'rgba(153, 102, 255, 0.7)',
            'rgba(255, 159, 64, 0.7)'
        ];
        
        return {
            label: service,
            data: serviceData[service],
            backgroundColor: colors[index % colors.length]
        };
    });
    
    // Create chart
    const ctx = document.getElementById('billing-chart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dates,
            datasets: datasets
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    stacked: true
                },
                y: {
                    stacked: true,
                    title: {
                        display: true,
                        text: 'Cost ($)'
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top'
                },
                title: {
                    display: true,
                    text: 'Daily Cloud Spending by Service'
                }
            }
        }
    });
}

function updateSpendingSummary(data) {
    // Calculate total monthly spending
    const total = data.reduce((sum, item) => sum + item.total, 0);
    const formattedTotal = '$' + total.toFixed(2);
    
    // Update UI
    document.getElementById('monthly-spending').textContent = formattedTotal;
    
    // Calculate percentage of budget used
    const creditLimit = 300;
    const percentUsed = (total / creditLimit) * 100;
    const formattedPercent = Math.min(percentUsed, 100).toFixed(1) + '%';
    
    // Update progress bar
    const progressBar = document.getElementById('spending-progress');
    progressBar.style.width = formattedPercent;
    progressBar.textContent = formattedPercent;
    progressBar.setAttribute('aria-valuenow', percentUsed.toFixed(1));
    
    // Change color based on percentage
    if (percentUsed < 50) {
        progressBar.className = 'progress-bar bg-success';
    } else if (percentUsed < 75) {
        progressBar.className = 'progress-bar bg-warning';
    } else {
        progressBar.className = 'progress-bar bg-danger';
    }
    
    // Calculate days remaining (assuming 90-day credit period)
    const daysRemaining = 90 - Math.min(data.length, 90);
    document.getElementById('days-remaining').textContent = daysRemaining + ' days';
}

function updateRecommendations(recommendations) {
    const tbody = document.getElementById('recommendations-table');
    tbody.innerHTML = '';
    
    recommendations.forEach(rec => {
        const row = document.createElement('tr');
        
        const categoryCell = document.createElement('td');
        categoryCell.textContent = rec.category;
        row.appendChild(categoryCell);
        
        const recommendationCell = document.createElement('td');
        recommendationCell.textContent = rec.recommendation;
        row.appendChild(recommendationCell);
        
        const savingsCell = document.createElement('td');
        savingsCell.textContent = rec.potential_savings;
        row.appendChild(savingsCell);
        
        const priorityCell = document.createElement('td');
        const priorityBadge = document.createElement('span');
        priorityBadge.className = 'badge ' + getPriorityClass(rec.priority);
        priorityBadge.textContent = rec.priority;
        priorityCell.appendChild(priorityBadge);
        row.appendChild(priorityCell);
        
        tbody.appendChild(row);
    });
}

function getPriorityClass(priority) {
    switch (priority.toLowerCase()) {
        case 'high':
            return 'badge-danger';
        case 'medium':
            return 'badge-warning';
        case 'low':
            return 'badge-info';
        default:
            return 'badge-secondary';
    }
}

function updatePotentialSavings(recommendations) {
    // Extract potential savings from recommendations
    const totalSavings = recommendations.reduce((sum, rec) => {
        const value = parseFloat(rec.potential_savings.replace('$', ''));
        return sum + value;
    }, 0);
    
    document.getElementById('potential-savings').textContent = '$' + totalSavings.toFixed(2) + '/month';
}

function updateUtilization(data) {
    const tbody = document.getElementById('utilization-table');
    tbody.innerHTML = '';
    
    for (const service in data) {
        const row = document.createElement('tr');
        
        const serviceCell = document.createElement('td');
        serviceCell.textContent = service;
        row.appendChild(serviceCell);
        
        for (const metric of ['CPU', 'Memory', 'Storage', 'Network']) {
            const cell = document.createElement('td');
            
            const value = data[service][metric];
            const progressContainer = document.createElement('div');
            progressContainer.className = 'progress';
            
            const progressBar = document.createElement('div');
            progressBar.className = getUtilizationClass(value);
            progressBar.style.width = value + '%';
            progressBar.textContent = value + '%';
            
            progressContainer.appendChild(progressBar);
            cell.appendChild(progressContainer);
            row.appendChild(cell);
        }
        
        tbody.appendChild(row);
    }
}

function getUtilizationClass(value) {
    if (value < 50) {
        return 'progress-bar bg-success';
    } else if (value < 80) {
        return 'progress-bar bg-warning';
    } else {
        return 'progress-bar bg-danger';
    }
}
