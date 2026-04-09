import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

def create_synthetic_data(num_samples=500):
    np.random.seed(42)
    # Features
    login_frequency = np.random.randint(1, 30, num_samples) # logins per month
    usage_time = np.random.randint(5, 120, num_samples) # total hours per month
    support_tickets = np.random.randint(0, 5, num_samples) # tickets opened
    days_since_last_action = np.random.randint(0, 60, num_samples) # days
    account_age = np.random.randint(1, 48, num_samples) # months

    # Calculate churn probability logic (hidden logic our model needs to learn)
    churn_prob = (support_tickets * 0.15) + (days_since_last_action * 0.01) - (login_frequency * 0.02) - (usage_time * 0.005) + np.random.normal(0, 0.1, num_samples)
    churn = (churn_prob > 0.4).astype(int)

    df = pd.DataFrame({
        'login_frequency': login_frequency,
        'usage_time': usage_time,
        'support_tickets': support_tickets,
        'days_since_last_action': days_since_last_action,
        'account_age': account_age,
        'churn': churn
    })
    return df

def train_model():
    print("Generating synthetic data...")
    df = create_synthetic_data(1000)
    X = df.drop('churn', axis=1)
    y = df['churn']

    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Save model
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model saved successfully to {model_path}")

if __name__ == '__main__':
    train_model()
