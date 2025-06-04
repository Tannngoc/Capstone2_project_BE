# 📈 Hubble AI Stock Prediction

### =================== BEGIN ====================

> **Group Name:** C2.SE23
> **Project Type:** Graduation Thesis – AI-powered Stock Forecasting & Visualization Web Platform  
> **Technologies Used:** Python (Flask), React, LSTM + BiLSTM (Keras), MUI, Docker, GitHub Actions

---

## 📌 Overview

This platform predicts stock prices using a combination of **historical price data** and **financial news sentiment** powered by AI. It provides:

- Interactive stock charts on regular basis
- AI-based buy/sell suggestions
- News sentiment analysis
- Role-based user experience (Investor/Admin)
- Portfolio & order management
- Live notifications and expert Q&A modules

---

## 🧠 AI Models Used

| Module | Model | Purpose |
|--------|-------|---------|
| 📊 **Price Prediction** | `BiLSTM` | Predict future stock price trends using historical price data |
| 📰 **News Sentiment** | `Embedding + BiLSTM` | Classify financial news titles into Positive / Neutral / Negative |
| ⚡ **Hybrid Model** | Combined | Improves prediction accuracy using both price and sentiment signals |

---

## 🛠️ Technologies Used

### ✅ Backend
- Python 3.10
- Flask (REST API)
- Keras / TensorFlow (AI models)
- Pandas, Numpy
- MySQL (for user & order data)
- GitHub Actions (daily data pipeline)
- Railway (optional deployment)

### ✅ Frontend
- React.js
- Material UI (MUI)
- Axios (API communication)
- Recharts / Chart.js (charts)
- Framer Motion (animations)

### ✅ Environment
- Visual Studio Code

---

## ⚙️ Installation Guide

### 📦 1. Clone the Project

```bash
# Backend
git clone https://github.com/Tannngoc/Capstone2_project_BE.git

# Frontend
git clone https://github.com/Tannngoc/Capstone2_Project_FE.git
```

# ⚙️ Backend Setup (Flask + AI)
1. Create Virtual Environment
- macOS / Linux:
```bash
cd Capstone2_project_BE
python3 -m venv venv
source venv/bin/activate
```

- Windows:
```bash
cd Capstone2_project_BE
python -m venv venv
.\venv\Scripts\activate
```

2. Install Dependencies
```bash
pip install -r requirements.txt --use-deprecated=legacy-resolver
```

3. Configure Database

Step 1: Make sure MySQL is running locally
Step 2: Create database via file starfall.sql (use MySQL Workbench or CLI)
```bash
-- Example CLI
mysql -u root -p < starfall.sql
```
Step 3: Create a .env file in project root with content like:
```bash
DATABASE_URI=mysql+pymysql://<username>:<password>@localhost:3306/<database_name>
```

4. Initialize & Migrate DB
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

5. Download github action
# macOS/ Linux:
```bash
brew install act
```
# Windows:
```shell
choco install act-cli
```


6. Run the Flask Server
```bash
flask run
```

# 💻 Frontend Setup (React)
```bash
cd ../Capstone2_Project_FE
npm install
npm run dev
```

### ==================== END =====================