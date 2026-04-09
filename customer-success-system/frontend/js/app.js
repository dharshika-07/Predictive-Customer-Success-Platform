document.addEventListener('DOMContentLoaded', () => {
    fetchCustomers();
});

let customersData = [];

async function fetchCustomers() {
    try {
        const response = await fetch('/api/customers');
        const data = await response.json();
        customersData = data;
        updateDashboard(data);
    } catch (error) {
        console.error("Failed to fetch customers:", error);
    }
}

function updateDashboard(customers) {
    const totalCustomersEl = document.getElementById('total-customers');
    const atRiskEl = document.getElementById('at-risk');
    const healthyEl = document.getElementById('healthy');
    const listEl = document.getElementById('customer-list');

    totalCustomersEl.textContent = customers.length;
    
    const highRisk = customers.filter(c => c.risk_level === 'High').length;
    atRiskEl.textContent = highRisk;
    
    const healthy = customers.filter(c => c.risk_level === 'Low').length;
    healthyEl.textContent = healthy;

    listEl.innerHTML = '';
    
    customers.forEach((c) => {
        const row = document.createElement('tr');
        
        let riskClass = 'risk-low';
        let riskColor = 'green';
        if (c.risk_level === 'High') { riskClass = 'risk-high'; riskColor = 'red'; }
        if (c.risk_level === 'Medium') { riskClass = 'risk-medium'; riskColor = 'orange'; }

        row.innerHTML = `
            <td>
                <div class="client-name">${c.name}</div>
                <div style="font-size:0.75rem; color:var(--text-secondary)">${c.contact}</div>
            </td>
            <td><span class="tier-badge">${c.tier}</span></td>
            <td>${c.days_since_last_action} days ago</td>
            <td>${c.support_tickets}</td>
            <td>
                <div class="risk-pill ${riskClass}">
                    ${c.churn_probability}% Risk
                </div>
            </td>
            <td>
                <button class="generate-btn" onclick="generateOutreach('${c.id}')">Generate Outreach</button>
            </td>
        `;
        listEl.appendChild(row);
    });
}

async function generateOutreach(customerId) {
    const customer = customersData.find(c => c.id === customerId);
    if (!customer) return;

    try {
        const response = await fetch('/api/outreach', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ customer: customer })
        });
        
        const data = await response.json();
        openModal(customer, data.campaign);
    } catch (error) {
        console.error("Failed to generate outreach:", error);
    }
}

function openModal(customer, campaign) {
    document.getElementById('modal-customer-name').textContent = `For ${customer.name}`;
    document.getElementById('modal-channel').textContent = campaign.channel;
    document.getElementById('modal-action').textContent = campaign.action_recommended;
    document.getElementById('modal-subject').textContent = campaign.subject;
    document.getElementById('modal-message').value = campaign.message;
    
    document.getElementById('outreach-modal').classList.add('active');
}

document.getElementById('close-modal').addEventListener('click', () => {
    document.getElementById('outreach-modal').classList.remove('active');
});

// Close modal when clicking outside
window.addEventListener('click', (e) => {
    const modal = document.getElementById('outreach-modal');
    if (e.target === modal) {
        modal.classList.remove('active');
    }
});

const searchInput = document.getElementById('search-input');
if (searchInput) {
    searchInput.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        const filtered = customersData.filter(c => 
            (c.name && c.name.toLowerCase().includes(term)) || 
            (c.contact && c.contact.toLowerCase().includes(term))
        );
        updateDashboard(filtered);
    });
}

const editBtn = document.getElementById('edit-msg-btn');
if (editBtn) {
    editBtn.addEventListener('click', () => {
        const msgArea = document.getElementById('modal-message');
        msgArea.readOnly = false;
        msgArea.focus();
    });
}

const dispatchBtn = document.getElementById('dispatch-btn');
if (dispatchBtn) {
    dispatchBtn.addEventListener('click', () => {
        alert('Outreach dispatched successfully!');
        document.getElementById('outreach-modal').classList.remove('active');
    });
}

// Sidebar Navigation Logic
const navItems = document.querySelectorAll('.nav-item');
const headerTitle = document.querySelector('.header-section h1');
const headerDesc = document.querySelector('.header-section p');
const kpiGrid = document.querySelector('.kpi-grid');
const tableContainer = document.querySelector('.table-container');

navItems.forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        
        navItems.forEach(n => n.classList.remove('active'));
        e.currentTarget.classList.add('active');
        
        const label = e.currentTarget.textContent.trim();
        
        if (label === 'Dashboard') {
            headerTitle.textContent = 'Overview';
            headerDesc.textContent = 'AI-Powered Churn Predictions and Outreach Insights';
            kpiGrid.style.display = 'grid';
            tableContainer.style.display = 'block';
            updateDashboard(customersData);
        } else if (label === 'Customers') {
            headerTitle.textContent = 'Customers';
            headerDesc.textContent = 'Manage and view all your customer accounts.';
            kpiGrid.style.display = 'none';
            tableContainer.style.display = 'block';
            updateDashboard(customersData);
        } else if (label === 'Outreach Tasks') {
            headerTitle.textContent = 'Outreach Tasks';
            headerDesc.textContent = 'Accounts requiring attention and outreach.';
            kpiGrid.style.display = 'none';
            tableContainer.style.display = 'block';
            const tasks = customersData.filter(c => c.risk_level === 'High' || c.risk_level === 'Medium');
            updateDashboard(tasks);
        }
    });
});

