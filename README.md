# Dynamic Risk-Based Two-Factor Authentication (2FA) System

**Adaptive Authentication with Contextual Risk Scoring**  
📌 *College Project Submission – IIT Patna*  
👨‍💻 Author: Ashutosh Kumar  

---

## 📖 Overview

Traditional password-based authentication is weak against modern attacks, and static 2FA (OTP every time) either frustrates users or fails to block sophisticated threats like phishing and SIM-swapping.  

This project implements a **Dynamic Risk-Based 2FA System** that evaluates the risk level of every login attempt using contextual signals (IP, device, location, time, failed attempts, velocity). Based on the risk score:

- ✅ **Low Risk** → Allow login directly  
- 🔑 **Medium Risk** → Require One-Time Password (OTP)  
- 🚨 **High Risk** → Block or flag for manual review  

The goal is to balance **security** and **user experience** by applying friction only when necessary.

---

## 🎯 Problem Statement

- Static OTPs apply the same friction to all users → poor user experience  
- Susceptible to **phishing, credential stuffing, SIM-swap attacks**  
- Traditional systems ignore **contextual signals** (device, IP, geolocation, login time, velocity)  
- Need for an **explainable, adaptive authentication system** that only challenges suspicious logins:contentReference[oaicite:0]{index=0}  

---

## ✅ Proposed Solution

- A **rules-based risk engine** assigns weighted scores to features like IP change, device fingerprint, login time anomalies, distance from last location, and failed attempts.  
- The **risk score** maps to actions:  
  - Low (<30) → Allow  
  - Medium (30–69) → OTP  
  - High (≥70) → Manual review  

Benefits:  
- Fewer false alarms  
- Reduced login friction for safe users  
- Explainable decisions (transparent scoring)

---

## 🏗 System Architecture

+-------------------+ +-------------------------+
| Streamlit UI | ----> | FastAPI Backend |
| - Login form | | - Risk Engine |
| - OTP input | | - OTP Service |
| - Show responses | | - User Store (JSON/DB) |
+-------------------+ +-------------------------+

markdown
Copy code

- **Frontend (Streamlit)**: login/OTP forms, risk visualization  
- **Backend (FastAPI)**: APIs `/login`, `/verify_otp`, `/create_demo_user`  
- **Core Components**:
  - 🧠 **Risk Engine** – weighted rule scoring  
  - 🔑 **OTP Service** – generates OTP (console, extendable to email/SMS)  
  - 🗄 **User Store** – simple JSON (can be upgraded to SQLite/SQLModel)  

---

## 🔬 Risk Features & Scoring

| Feature           | Description | Example Weight |
|-------------------|-------------|----------------|
| `ip_unknown`      | New IP for user | +40 |
| `device_unknown`  | New device fingerprint | +30 |
| `time_anomaly`    | Login at unusual time | +20 |
| `geo_distance_km` | Distance from last location | +0.5/km |
| `failed_attempts` | Recent failed logins | +10 each |
| `velocity`        | Impossible travel speed | optional |

**Thresholds:**  
- `<30` → Low Risk  
- `30–69` → Medium Risk (OTP)  
- `≥70` → High Risk (manual review)  

Example: New IP (40) + New Device (30) + Geo Distance 50km (25) = **95 → High Risk**

---

## 🔄 Authentication Flow

1. User submits **username + password + metadata** (IP, UA, location, timestamp).  
2. Backend computes **risk features** & score.  
3. System returns:  
   - `low` → Success  
   - `medium` → Generate & verify OTP  
   - `high` → Block / manual review  
4. OTP (if required) is printed in backend logs (demo).  

**Sample Response (Medium Risk):**
```json
{
  "risk_level": "medium",
  "next_action": "send_otp",
  "explain": {
    "score": 45.2,
    "reasons": ["new IP", "unknown device"]
  }
}
📂 Project Structure
csharp
Copy code
dynamic-risk-2fa/
├─ backend/
│  ├─ app.py              # FastAPI backend
│  ├─ risk_engine.py      # Risk scoring logic
│  ├─ otp_service.py      # OTP generation & delivery
│  ├─ db.py               # Demo user database
│  └─ requirements.txt    # Dependencies
├─ frontend/
│  └─ streamlit_app.py    # Streamlit-based UI
└─ README.md              # Documentation
⚙️ Setup & Running
1. Clone the repo
bash
Copy code
git clone https://github.com/ashutosh8021/dynamic-risk-2fa.git
cd dynamic-risk-2fa
2. Create virtual environment & install deps
bash
Copy code
cd backend
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate.bat  # Windows
pip install -r requirements.txt
3. Run Backend
bash
Copy code
uvicorn app:app --reload --port 8000
Docs → http://localhost:8000/docs

4. Run Frontend
bash
Copy code
cd ../frontend
streamlit run streamlit_app.py
Frontend → http://localhost:8501

🧪 Demo Instructions
Create a demo user (alice) from the UI.

Login with:

Username: alice

Password: demo-password

Vary metadata (IP, location, UA, time) to simulate:

Low → seamless login

Medium → OTP required (check console)

High → flagged

📊 Learning Outcomes
Designed an adaptive authentication system.

Integrated FastAPI backend with Streamlit frontend.

Implemented a rules-based risk engine.

Explored context-aware security models.

Prepared system for future ML integration.

🚀 Future Work
🔒 Replace JSON store with SQLite/SQLModel & secure password hashing (bcrypt).

🛡 Add rate limiting on login/OTP endpoints.

📩 Real OTP delivery via SMTP/Twilio.

🤖 Build ML-based risk engine (RandomForest vs rules baseline).

📊 Admin dashboards for login analytics.

📜 Conclusion
This prototype demonstrates a practical, explainable approach to adaptive authentication. It reduces friction for safe logins while strengthening protection for risky ones. The modular design makes it easy to extend with machine learning models and integrate with real-world identity systems.

👨‍💻 Author
Ashutosh Kumar
BS in Computer Science, IIT Patna
📧 ashutosh_2312res778@iitp.ac.in
🔗 GitHub Repo


