# 🔒 DPRP — Digital Privacy Risk Assessment Platform

A web-based system that helps users assess their digital privacy risk based on their online habits, and provides personalized recommendations to improve their privacy and security.

> Final Year Project — Development of a Web-Based System for Assessing Users' Digital Privacy Risk

---

## 📋 Overview

DPRP allows users to register, take a 15-question privacy assessment covering five key categories, and instantly receive a privacy risk score (0–100) with a corresponding risk level (Low, Medium, High, Critical) and personalized tips for improvement.

---

## ✨ Features

- 🔐 **User Authentication** — secure registration and login with hashed passwords
- 📋 **Privacy Assessment** — 15-question quiz across 5 categories with a live progress bar
- 📊 **Risk Scoring Engine** — weighted scoring algorithm producing a 0–100 risk score
- 💡 **Personalized Recommendations** — tailored tips based on risk level
- 📜 **Assessment History** — users can view all their past assessments
- ⚙️ **Admin Dashboard** — overview of all users, assessments, and risk statistics

---

## 🧠 Assessment Categories

| Category | Focus |
|---|---|
| Social Media | Oversharing & privacy settings |
| Password & Authentication | Password strength & 2FA |
| Device Security | Updates, antivirus, device locks |
| Browsing Habits | VPN use, phishing awareness |
| Data Sharing | App permissions, HTTPS awareness |

---

## 🛠️ Tech Stack

- **Backend:** Python (Flask)
- **Frontend:** HTML5, CSS3, JavaScript
- **Database:** SQLite
- **ORM:** Flask-SQLAlchemy
- **Authentication:** Flask-Login, Werkzeug

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/dprp.git
cd dprp

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

The app will be available at `http://127.0.0.1:5000`

---

## 🔑 Creating an Admin Account

After registering a user account, run the following to grant admin access:

```bash
python -c "
from app import app
from models import db, User
with app.app_context():
    user = User.query.filter_by(email='your@email.com').first()
    user.is_admin = True
    db.session.commit()
    print('Admin set successfully!')
"
```

Then visit `/admin` while logged in with that account.

---

## 📁 Project Structure

```
dprp/
├── app.py              # Main Flask application & routes
├── config.py           # App configuration
├── models.py           # Database models (User, Assessment, Answer)
├── templates/           # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── assessment.html
│   ├── results.html
│   ├── history.html
│   └── admin/
│       └── dashboard.html
├── static/
│   ├── css/style.css
│   └── js/main.js
└── requirements.txt
```

---

## 📈 How Scoring Works

Each question is assigned a weight (1–3) based on its privacy significance. A "risky" answer adds its weight to the total risk points. The final score is calculated as:

```
Score = (Total Risk Points / Maximum Possible Points) × 100
```

| Score Range | Risk Level |
|---|---|
| 0 – 25 | Low |
| 26 – 50 | Medium |
| 51 – 75 | High |
| 76 – 100 | Critical |

---

## 📄 License

This project was developed as part of a final year academic project.
