import os
import pickle
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')

def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    with open(MODEL_PATH, 'rb') as f:
        return pickle.load(f)

def predict_churn(customer_data):
    """
    customer_data expects dictionary with:
    login_frequency, usage_time, support_tickets, days_since_last_action, account_age
    """
    model = load_model()
    if not model:
        # Fallback heuristic if model isn't trained
        score = customer_data.get("support_tickets", 0) * 0.15 + customer_data.get("days_since_last_action", 0) * 0.01
        return min(max(score, 0), 1)

    df = pd.DataFrame([customer_data])
    # The random forest predict_proba returns [prob_class_0, prob_class_1]
    prob = model.predict_proba(df)[0][1]
    return prob
