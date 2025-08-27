# Dynamic Risk-Based Two-Factor Authentication (2FA) System

**College Project Submission – IIT Patna**

---

## 📌 Project Overview

This project implements a **dynamic risk-based two-factor authentication (2FA) system** that adjusts security requirements based on the risk profile of a login attempt.  

- **Low risk** → Login succeeds with password only  
- **Medium risk** → Requires One-Time Password (OTP)  
- **High risk** → Flags for manual review  

This ensures **strong security** without compromising **usability**.

---

## 🎯 Objectives

- To demonstrate how adaptive authentication can improve login security.  
- To design and implement a **risk engine** for real-time decision-making.  
- To integrate a **Streamlit frontend** with a **FastAPI backend**.  
- To simulate real-world OTP-based verification.  

---

## 🛠 Tech Stack

- **Backend**: FastAPI (Python)  
- **Frontend**: Streamlit  
- **Database**: SQLite / JSON (demo)  
- **OTP Service**: Console-based OTP (extendable to Email/SMS)  
- **Risk Engine**: Rule-based (Machine Learning ready)  



## 📂 Project Structure


dynamic-risk-2fa/
├─ backend/
│ ├─ app.py # FastAPI backend
│ ├─ risk_engine.py # Risk scoring logic
│ ├─ otp_service.py # OTP generator & verifier
│ ├─ db.py # Demo user database
│ └─ requirements.txt # Python dependencies
├─ frontend/
│ └─ streamlit_app.py # Streamlit front end
└─ README.md # Documentation



## 🚀 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/ashutosh8021/dynamic-risk-2fa.git
cd dynamic-risk-2fa
2. Setup Environment
bash
Copy code
cd backend
python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate.bat   # Windows
pip install -r requirements.txt
3. Run Backend (FastAPI)
bash
Copy code
uvicorn app:app --reload --port 8000
API Docs: http://localhost:8000/docs

4. Run Frontend (Streamlit)
bash
Copy code
cd ../frontend
streamlit run streamlit_app.py
Frontend: http://localhost:8501

🔑 Demo Credentials
Username: alice

Password: demo-password

Risk-based behavior:

Low risk → Direct login

Medium risk → OTP required (printed in console)

High risk → Manual review

📊 Learning Outcomes
Understanding adaptive authentication models

Integration of FastAPI and Streamlit

Designing a rule-based risk engine

Implementing OTP-based verification

Awareness of production-level security measures (TLS, secret storage, rate limiting)

📈 Future Scope
Replace rule-based engine with ML-based risk prediction

Add real OTP delivery (Email/SMS APIs like Twilio/SendGrid)

Enhance UI with dashboards for login analytics

Extend DB for multi-user management

👨‍💻 Author
Ashutosh Kumar
B.S in Computer Science, IIT Patna

📜 License
This project is for academic purposes. For production use, please ensure compliance with security best practices.
