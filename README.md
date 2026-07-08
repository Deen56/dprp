# 🔒 DPRP — Digital Privacy Risk Assessment Platform

A web application that helps everyday internet users understand and improve their digital privacy through a quick assessment, personalised risk scoring, and an AI-powered privacy assistant.

---

## What Problem Does It Solve?

Most people have no idea how exposed their personal information is online. They reuse passwords, share their location publicly, ignore two-factor authentication, and click suspicious links — not out of negligence, but because no one has ever shown them the risk in a clear, personalised way.

DPRP changes that. In under 5 minutes, any internet user can take a 15-question assessment and get a clear picture of where they stand — and what to do about it.

---

##  Features

- **Privacy Risk Assessment** — 15 weighted questions across 5 categories: Social Media, Password & Authentication, Device Security, Browsing Habits, and Data Sharing
- **Risk Scoring** — Calculates a personalised score from 0–100 with Low, Medium, High, and Critical risk levels
- **Personalised Recommendations** — Tailored advice based on the user's specific answers
- **Assessment History** — Users can track their privacy score over time
- **Veyr — AI Privacy Assistant** — A RAG-powered chatbot that answers privacy questions and gives personalised advice based on the user's actual assessment data
- **Admin Dashboard** — View all users and assessments
- **Secure Authentication** — User registration, login, and session management

---

##  How Veyr Works (RAG Architecture)

Veyr is not a generic chatbot. It uses **Retrieval-Augmented Generation (RAG)** to answer questions accurately from a curated privacy knowledge base, and it connects directly to the user's assessment data to give personalised responses.

```
User asks a question
      ↓
Question converted to a vector (embedding)
      ↓
Similarity search finds the most relevant knowledge base section
      ↓
User's real score and weak areas fetched from the database
      ↓
All context sent to the language model
      ↓
Veyr responds with accurate, personalised advice
```

This means when you ask "What are my weak areas?" — Veyr doesn't guess. It looks up your actual answers.

---

##  Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask, Flask-Login |
| Database | SQLite, SQLAlchemy |
| AI Model | Google Gemini 2.5 Flash |
| Embeddings | Google Gemini Embedding 001 |
| Vector Search | NumPy (cosine similarity) |
| Frontend | HTML, CSS, JavaScript (Fetch API) |
| Auth | Werkzeug password hashing |
| Environment | python-dotenv |

---

##  Project Structure

```
dprp/
├── app.py              # Main Flask application and routes
├── rag.py              # RAG system — embeddings, retrieval, Veyr logic
├── models.py           # Database models (User, Assessment, Answer)
├── questions.py        # Assessment questions and weights
├── config.py           # App configuration
├── knowledge.txt       # Veyr's privacy knowledge base
├── .env                # API keys (not tracked in Git)
├── requirements.txt    # Python dependencies
├── static/
│   ├── css/style.css   # Styling
│   └── js/main.js      # Frontend JavaScript
└── templates/
    ├── base.html        # Base layout with navigation
    ├── index.html       # Landing page
    ├── assessment.html  # 15-question assessment form
    ├── results.html     # Score and recommendations
    ├── history.html     # Assessment history
    ├── chat.html        # Veyr chat interface
    ├── login.html       # Login page
    ├── register.html    # Registration page
    └── admin/
        └── dashboard.html  # Admin panel
```

---

##  Getting Started

### Prerequisites
- Python 3.10+
- A Google Gemini API key (free at [aistudio.google.com](https://aistudio.google.com))

### Installation

```bash
# Clone the repository
git clone https://github.com/Deen56/dprp.git
cd dprp

# Install dependencies
pip install -r requirements.txt

# Create your .env file
echo "GEMINI_API_KEY=your-api-key-here" > .env

# Run the app
python app.py
```

Then open your browser and go to `http://127.0.0.1:5000`

---

##  How the Scoring Works

Each of the 15 questions is assigned a weight (1–3) based on its privacy impact. A risky answer contributes that question's weight to the total risk points.

```
Risk Score = (Total Risk Points / Total Possible Points) × 100
```

| Score Range | Risk Level |
|---|---|
| 0 – 25 | Low |
| 26 – 50 | Medium |
| 51 – 75 | High |
| 76 – 100 | Critical |

---

##  What I Learned Building This

- Designing and building a full stack web application from scratch with Flask and SQLAlchemy
- Implementing secure user authentication with hashed passwords and session management
- Building a RAG system from scratch — chunking documents, generating embeddings, and implementing cosine similarity search using NumPy
- Integrating a live AI API (Google Gemini) into a web backend
- Building a real-time chat interface using JavaScript Fetch API without page reloads
- Connecting an AI assistant to a live database so it gives personalised, data-driven responses rather than generic answers
- Managing API keys and sensitive data securely with environment variables

---

##  Future Plans

- Deploy to a cloud platform (Render or Railway)
- Add a desktop agent version that can scan system privacy settings
- Expand the knowledge base with more detailed privacy guidance
- Add email notifications for score improvements
- Support multiple languages

---

##  Author

**Deen** — Final Year Computer Science Student  
GitHub: [github.com/Deen56](https://github.com/Deen56)

---

> Built as a final year graduation project. Designed to be a genuinely useful tool, not just an academic exercise.
