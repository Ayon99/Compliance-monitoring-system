# AI Compliance Monitoring System

## Overview

AI Compliance Monitoring System is a full-stack monitoring and anomaly detection platform designed to ingest application logs in real time, detect suspicious or non-compliant behavior using both rule-based logic and machine learning, and visualize insights through a live dashboard.

The project combines backend engineering, machine learning integration, database systems, real-time dashboards, and reporting into a single end-to-end pipeline.

---

# System Architecture

```text
Logs
  ↓
FastAPI Backend
  ↓
PostgreSQL Database
  ↓
Rule Engine + ML Anomaly Detection
  ↓
Violations Database
  ↓
REST APIs
  ↓
React Dashboard + Reports
```

---

# Features

## Real-Time Log Ingestion

* Accepts logs through FastAPI endpoints
* Stores structured logs in PostgreSQL
* Supports multiple services and users
* Handles log levels such as INFO, WARNING, and ERROR

## Rule-Based Compliance Detection

* Detects explicit violations using predefined rules
* Example detections:

  * authentication failures
  * repeated ERROR logs
  * suspicious request bursts

## ML-Based Anomaly Detection

* Uses Isolation Forest (scikit-learn)
* Performs unsupervised anomaly detection
* Aggregates user behavior into feature vectors
* Detects unusual behavioral patterns

### Current ML Features

* total requests per user
* error count
* warning count
* error ratio
* request behavior aggregation

## Authentication & Security

* JWT-based authentication
* Protected API endpoints
* Role-based access control

## React Dashboard

### Dashboard includes:

* Total logs
* Total violations
* Error logs
* ML anomalies
* Violations overview chart
* Real-time updates

## Logs Viewer

* Displays incoming logs live
* Severity highlighting
* Auto-refresh support

## Report Generation

* PDF report download
* Violation summaries
* Breakdown by violation type
* Detailed violation logs

## Real-Time Simulation

A Python-based simulator generates:

* normal traffic
* warning traffic
* burst attacks
* random spikes
* anomalous behavior patterns

---

# Machine Learning Pipeline

## Workflow

```text
Logs
  ↓
Feature Extraction
  ↓
Behavior Aggregation
  ↓
Isolation Forest
  ↓
Anomaly Prediction
  ↓
Violation Storage
```

## Why Isolation Forest?

Isolation Forest was selected because:

* works well for unsupervised anomaly detection
* efficient on smaller structured datasets
* lightweight integration
* explainable anomaly behavior
* minimal preprocessing requirements

## ML Limitations

This project focuses on demonstrating ML integration into a real-time monitoring pipeline rather than production-grade anomaly detection accuracy.

Current limitations:

* small synthetic dataset
* no labeled data
* limited feature dimensionality
* retraining instability on small samples

Future improvements:

* time-windowed aggregation
* rolling baseline models
* feature scaling
* better anomaly calibration
* model comparison (Autoencoders / One-Class SVM)

---

# Tech Stack

## Backend

* FastAPI
* Python
* PostgreSQL
* JWT Authentication

## Frontend

* React.js
* Recharts
* JavaScript
* CSS

## Machine Learning

* scikit-learn
* Isolation Forest
* pandas
* NumPy

## Tools

* Git
* GitHub
* PostgreSQL
* VS Code

---

# API Endpoints

## Authentication

### POST `/login`

Authenticate user and return JWT token.

---

## Logs

### POST `/ingest-log`

Ingest application logs.

### GET `/logs`

Retrieve stored logs.

---

## Violations

### GET `/violations`

Retrieve detected violations.

---

## Reports

### GET `/report`

Return report summary.

### GET `/report/download`

Download PDF report.

---

# Example Log Payload

```json
{
  "service": "auth-service",
  "level": "ERROR",
  "message": "Multiple failed login attempts",
  "user_id": "u1"
}
```

---

# Example Violation

```json
{
  "rule": "ml_anomaly",
  "user": "u1",
  "details": "Anomalous behavior detected",
  "timestamp": "2026-04-19 12:00:00"
}
```

---

# Project Structure

```text
frontend-react/
├── src/
│   ├── pages/
│   ├── context/
│   ├── components/
│   └── App.js
│
backend/
├── server.py
├── auth.py
├── ml_model.py
├── ml_features.py
├── simulate_logs.py
├── report_generator.py
└── requirements.txt
```

---

# Screenshots

## Dashboard

<img width="1858" height="933" alt="Screenshot 2026-05-01 033254" src="https://github.com/user-attachments/assets/3d9d2a96-a790-4075-a8e2-d6daa3f83b76" />


## Logs Page

<img width="1854" height="893" alt="Screenshot 2026-05-01 033314" src="https://github.com/user-attachments/assets/8b113e47-739f-4f32-82c8-a74d40084d82" />


## Report Page

<img width="1848" height="782" alt="Screenshot 2026-05-01 033336" src="https://github.com/user-attachments/assets/45e0d4d3-d371-474e-92a2-ca8f6e856f82" />


## Login Page

<img width="1670" height="890" alt="Screenshot 2026-05-01 033225" src="https://github.com/user-attachments/assets/45ee1e97-7682-4a9f-8aaa-d03fa532ed6f" />


---

# How To Run

## 1. Clone Repository

```bash
git clone https://github.com/Ayon99/Compliance-monitoring-system
cd Compliance-monitoring-system
```

---

## 2. Backend Setup

```bash
pip install -r requirements.txt
uvicorn server:api --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

---

## 3. Frontend Setup

```bash
cd frontend-react
npm install
npm start
```

Frontend runs at:

```text
http://localhost:3000
```

---

## 4. PostgreSQL Setup

Create database:

```sql
CREATE DATABASE compliance_db;
```

Create required tables:

* raw_logs
* violations

---

## 5. Run Log Simulator

```bash
python simulate_logs.py
```

---

# Resume Description

Designed and developed an AI-powered compliance monitoring system that detects rule-based violations and anomalous behavior using unsupervised machine learning, deployed with a FastAPI backend, PostgreSQL database, and real-time React dashboard.

---

# Key Learnings

This project involved:

* full-stack system design
* ML integration into live systems
* debugging anomaly detection behavior
* backend API development
* database integration
* authentication systems
* real-time dashboard engineering
* feature engineering for behavioral analysis

---

# Future Improvements

* Kafka/RabbitMQ-based ingestion pipeline
* time-series anomaly modeling
* advanced behavioral features
* model benchmarking
* distributed processing
* alerting system
* user activity analytics
* containerized deployment

---

# Author

Ayon Ghosh

* GitHub: [https://github.com/Ayon99](https://github.com/Ayon99)
* LinkedIn: [https://linkedin.com/in/ayon-ghosh-ml/](https://linkedin.com/in/ayon-ghosh-ml/)
