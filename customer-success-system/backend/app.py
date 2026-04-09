from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
import sys

# Add parent directory to path to import ml_model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
try:
    from ml_model.predict import predict_churn
except ImportError:
    # Dummy fallback
    def predict_churn(data): return 0.5

FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
CORS(app)

DATA_FILE = os.path.join(BASE_DIR, 'data', 'customers.json')

@app.route('/')
def serve_index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

def load_customers():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

@app.route('/api/customers', methods=['GET'])
def get_customers():
    customers = load_customers()
    # Enrich with predictions on the fly
    for c in customers:
        risk = predict_churn({
            "login_frequency": c["login_frequency"],
            "usage_time": c["usage_time"],
            "support_tickets": c["support_tickets"],
            "days_since_last_action": c["days_since_last_action"],
            "account_age": c["account_age"]
        })
        c["churn_probability"] = round(risk * 100, 2)
        if c["churn_probability"] > 70:
            c["risk_level"] = "High"
        elif c["churn_probability"] > 30:
            c["risk_level"] = "Medium"
        else:
            c["risk_level"] = "Low"
    return jsonify(customers)

@app.route('/api/outreach', methods=['POST'])
def generate_outreach():
    data = request.json
    customer = data.get('customer')
    if not customer:
        return jsonify({"error": "No customer data provided"}), 400
    
    prob = customer.get("churn_probability", 0)
    tickets = customer.get("support_tickets", 0)
    days_inactive = customer.get("days_since_last_action", 0)
    name = customer.get("name", "Customer")
    
    # Simple rule engine to generate personalized outreach
    campaign = {
        "channel": "Email",
        "subject": "Checking in on your experience",
        "message": "",
        "action_recommended": ""
    }
    
    if prob > 70:
        campaign["channel"] = "Phone Call"
        campaign["subject"] = "Urgent: Customer Success Check-in"
        campaign["action_recommended"] = "Schedule immediate call with account manager."
        if tickets > 2:
            campaign["message"] = f"Hi {name} team,\n\nI noticed you've had a few support tickets recently. I want to personally ensure they are resolved and discuss how we can improve your experience."
        else:
            campaign["message"] = f"Hi {name} team,\n\nWe haven't seen much activity from you lately. Is there anything we can help you with to ensure you are getting the most out of our platform?"
    elif prob > 30:
        campaign["channel"] = "Personalized Email from CS"
        campaign["subject"] = f"How are things with {name}?"
        campaign["action_recommended"] = "Send automated re-engagement sequence."
        campaign["message"] = f"Hi {name},\n\nJust checking in! I thought you might find these advanced features useful to boost your team's productivity."
    else:
        campaign["channel"] = "Automated Newsletter"
        campaign["subject"] = "Latest Updates & Tips"
        campaign["action_recommended"] = "No direct action needed. Keep in standard nurturing track."
        campaign["message"] = f"Hi {name},\n\nCheck out our latest feature updates and success tips!..."
        
    return jsonify({"campaign": campaign})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
