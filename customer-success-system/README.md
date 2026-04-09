# SuccessOS - Predictive Customer Success Platform

An intelligent, proactive customer success system designed to analyze user behavior patterns, predict accounts at risk of churn, and optimize automated outreach. 

## 🚀 Features

- **AI-Powered Churn Prediction:** Uses a Random Forest machine learning model to evaluate customer engagement traits (login frequency, usage time, support tickets, account age) and assign real-time churn probability scores.
- **Dynamic Single Page Dashboard:** A fully responsive, modern web interface displaying KPI overviews, a health index of all clients, and filtering capabilities—seamlessly updating without page reloads.
- **Automated Outreach Engine:** A smart rule engine that evaluates churn probability and generates personalized communication strategies (e.g., automated email sequences, urgent phone calls from account managers) with dynamically drafted subject lines and messaging.
- **Live Search & Filtering:** Effortlessly sort through hundreds of monitored accounts instantly, and narrow down views to focus strictly on High and Medium risk accounts.

## 🛠️ Technology Stack

- **Frontend:** Vanilla HTML5, CSS3 with extensive use of CSS variables and glassmorphism design, and Vanilla JavaScript (`app.js`).
- **Backend:** Python + Flask (`app.py`), acting as a lightweight API gateway and static file server.
- **Machine Learning:** `scikit-learn`, `pandas`, and `numpy` used for generating synthetic training data and creating the Random Forest Classifier.

## 📦 Project Structure

```text
customer-success-system/
├── backend/          # Flask application logic and API routes
│   └── app.py        # Main entry point for the backend server
├── data/             # Datastores
│   └── customers.json# Dynamic JSON datastore containing mock customer metrics
├── frontend/         # UI Files
│   ├── css/          # Styling (glassmorphism dashboard)
│   ├── js/           # Single-page navigation logic and API handlers
│   └── index.html    # The main UI entrypoint
├── ml_model/         # AI Logic and models
│   ├── train.py      # Script to generate synthetic data and train the model
│   └── predict.py    # Endpoint logic for predicting live customer data
└── requirements.txt  # Python environment dependencies
```

## ⚙️ Getting Started

### Prerequisites

Ensure you have Python 3.8+ installed on your machine.

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd customer-success-system
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Train the ML Model:** (If `model.pkl` doesn't exist yet)
   ```bash
   python ml_model/train.py
   ```

4. **Run the Backend Server:**
   ```bash
   python backend/app.py
   ```

5. **View the Application:**
   Open your browser and navigate to `http://127.0.0.1:5000/`.

## 🤝 Contribution & Usage

This project was developed as a comprehensive mock-up and foundation for an advanced AI integration pipeline. You can modify the generated models by tweaking `train.py` or modify the automated outreach messaging templates from the `generate_outreach` route in the `app.py` service.
