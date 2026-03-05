# 🚀 Smart Business Intelligence Platform

An AI-ready **Business Intelligence backend platform** that automatically analyzes uploaded business datasets and generates **KPIs, trends, growth metrics, and anomaly detection**.

This project demonstrates how modern analytics systems transform raw CSV data into actionable insights using **FastAPI, PostgreSQL, and Python data processing pipelines**.

---

# 📊 Project Overview

Businesses often rely on tools like **Excel dashboards, Power BI, or Tableau** to analyze their data.
However, those tools require manual setup and complex configuration.

The **Smart Business Intelligence Platform** automates this process by:

* Ingesting raw datasets
* Detecting numeric metrics
* Generating KPI summaries
* Computing monthly trends
* Calculating growth rates
* Detecting anomalies in business metrics

The goal is to build an **AI-driven BI system for SMEs** that provides insights automatically.

---

# ✨ Key Features

### 🔐 Authentication System

* Secure JWT authentication
* User registration and login
* Protected API routes

### 📂 Dataset Upload

* Upload CSV business datasets
* Files stored securely on server
* Dataset metadata stored in PostgreSQL

### 📈 Automatic KPI Generation

* Detects numeric business metrics
* Calculates totals and averages
* Generates structured KPI summaries

### 📅 Monthly Trend Analysis

* Automatically detects date columns
* Aggregates metrics by month
* Creates time-series business insights

### 📊 Growth Metrics

* Calculates **Month-over-Month growth**
* Provides business performance indicators

### 🚨 Anomaly Detection

* Uses statistical **Z-Score detection**
* Identifies unusual spikes or drops in metrics

### 🔍 Data Profiling

* Dataset summary
* Missing value detection
* Column type inference

---

# 🏗 System Architecture

```
Client (Swagger / Frontend)
        │
        ▼
FastAPI Backend
        │
        ├── Authentication Service
        ├── Dataset Upload Service
        ├── Data Profiling Engine
        ├── KPI Analytics Engine
        └── Anomaly Detection
        │
        ▼
PostgreSQL Database
```

---

# ⚙️ Tech Stack

Backend Framework

* FastAPI

Database

* PostgreSQL
* SQLAlchemy ORM

Data Processing

* Pandas
* NumPy

Authentication

* JWT Tokens
* OAuth2 Password Flow

Other Tools

* Uvicorn
* Python Multipart
* Passlib (bcrypt hashing)

---

# 📂 Project Structure

```
backend
│
├── api
│   ├── auth.py
│   └── datasets.py
│
├── db
│   ├── session.py
│   └── base.py
│
├── models
│   ├── user.py
│   └── datasets.py
│
├── schemas
│   └── user.py
│
├── utils
│   ├── security.py
│   └── jwt_handler.py
│
├── uploads/
│
├── main.py
├── requirements.txt
└── README.md
```

---

# 🚀 How To Run The Project

## 1️⃣ Clone the repository

```
git clone https://github.com/yourusername/smart-bi-platform.git
cd smart-bi-platform/backend
```

---

## 2️⃣ Create virtual environment

```
python -m venv venv
```

Activate environment

Windows

```
venv\Scripts\activate
```

Mac/Linux

```
source venv/bin/activate
```

---

## 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

## 4️⃣ Setup environment variables

Create `.env` file

```
DATABASE_URL=postgresql://postgres:password@localhost:5432/smartbi
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 5️⃣ Start the server

```
uvicorn main:app --reload
```

---

## 6️⃣ Open API documentation

```
http://127.0.0.1:8000/docs
```

You can now test the entire platform using Swagger UI.

---

# 📊 Example Workflow

1️⃣ Register a user
2️⃣ Login and authorize
3️⃣ Upload a dataset

```
POST /datasets/upload
```

4️⃣ Get dataset summary

```
GET /datasets/{dataset_id}/summary
```

5️⃣ Generate KPIs

```
GET /datasets/{dataset_id}/kpis
```

---

# 📈 Example Output

```
{
  "numeric_columns": ["Revenue"],
  "kpis": {
    "Revenue": {
      "total": 520000,
      "average": 26000
    }
  },
  "monthly_trend": {
    "Revenue": {
      "2024-01": 120000,
      "2024-02": 150000
    }
  },
  "growth_metrics": {
    "Revenue": {
      "2024-02": 25.0
    }
  }
}
```

---

# 🧠 Future Improvements

* Automated KPI labeling
* Machine learning forecasting
* Natural language BI queries
* Interactive dashboards
* Cloud deployment
* Multi-tenant analytics

---

# 👨‍💻 Author

**Om Vardhan**

Aspiring AI/ML Engineer building intelligent data systems.

---

# ⭐ If You Like This Project

Please consider giving the repository a **star** ⭐
It helps others discover the project.
