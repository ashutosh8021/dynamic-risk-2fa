🚀 Dynamic Risk-based 2FA System

Internship Project — Adaptive Two-Factor Authentication (2FA) based on user login risk

📌 Overview

This project implements a dynamic risk-based two-factor authentication system.
Instead of enforcing OTP every time, the system assigns a risk score to each login attempt and adapts security:

✅ Low risk → login success (no OTP)

⚠️ Medium risk → OTP challenge

🔴 High risk → manual review required

This balances security 🔒 with user convenience 🎯.

🏗️ Tech Stack

Backend: FastAPI (Python)

Frontend: Streamlit

Database: SQLite / JSON (demo user storage)

Risk Engine: Rules-based (with option for ML)

OTP: Email / Console log (demo)

📂 Project Structure
dynamic-2fa/
├─ backend/
│  ├─ app.py           # FastAPI backend
│  ├─ risk_engine.py   # Rules-based risk scoring
│  ├─ otp_service.py   # OTP generation/verification
│  ├─ db.py            # Simple demo user DB
│  └─ requirements.txt
├─ frontend/
│  └─ streamlit_app.py # Streamlit frontend
└─ README.md           # Project documentation

⚡ Setup Instructions
1️⃣ Clone Repo & Setup Environment
git clone https://github.com/your-username/dynamic-2fa.git
cd dynamic-2fa
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac
pip install -r backend/requirements.txt

2️⃣ Run Backend (FastAPI)
cd backend
uvicorn app:app --reload --port 8000


Backend will be available at 👉 http://localhost:8000/docs

3️⃣ Run Frontend (Streamlit)
cd ../frontend
streamlit run streamlit_app.py


Frontend will be available at 👉 http://localhost:8501

🔑 Demo Login Flow

Create demo user Alice from frontend.

Login with:

Username: alice

Password: demo-password

Risk engine decides:

Low risk → Login success

Medium risk → OTP required (printed in backend logs, e.g., 123456)

High risk → Manual review

📸 Screenshots
🟢 Login UI

⚠️ Medium Risk (OTP Challenge)

🔴 High Risk (Manual Review)

🔒 Security Notes

Demo OTPs are printed to console (use email/SMS in production).

Risk scoring can be extended with ML models (RandomForest).

For production: use HTTPS, secure secret storage, and rate limiting.

🎯 Next Steps

Add ML-based risk engine (model_train.py)

Integrate real email/SMS OTP (Twilio, SendGrid, etc.)

Extend user DB for multiple accounts

Improve frontend UX with dashboards

👨‍💻 Author

Ashutosh Kumar
BS in Computer Science, IIT Patna