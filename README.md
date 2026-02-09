# 📊 Financial Monitoring System

This is a real-time crypto tracking dashboard I built while learning full-stack development.
The goal wasn't to make the next Binance — it was to actually understand how things work end-to-end.

You can log in, track your portfolio, watch live prices, set alerts, and even get AI-powered market insights.
Simple idea. Not-so-simple execution.

---

## 🚀 What This App Does

Once you're logged in, you can:

- 🔐 **Authenticate securely** using JWTs (no plain-text passwords here)
- 📈 **Watch live BTC prices** updating every few seconds via WebSockets
- 💼 **Track your crypto portfolio** in one place
- ⏰ **Set price alerts** and get notified when targets hit
- 🤖 **Ask AI for market insights** (risk analysis + trend prediction)

It's built to feel like a real product, not just a tutorial project.

---

## 🧩 Features (in plain English)

**Authentication**
Register and log in with hashed passwords and JWT-based auth.

**Live Price Updates**
BTC price streams every 5 seconds using WebSockets (no boring polling).

**Portfolio Management**
Add and track your crypto holdings.

**Price Alerts**
Set a price → get notified when it's reached.

**AI Analysis**
Uses Google Gemini to give basic risk assessment and trend insights.

---

## 🛠 Tech Stack (and why I chose it)

| Layer     | Tech          | Reason                        |
| --------- | ------------- | ----------------------------- |
| Backend   | FastAPI       | Async, fast, clean, auto docs |
| Frontend  | React + Vite  | Component-based + fast dev    |
| Database  | PostgreSQL    | Reliable & scalable           |
| Real-time | WebSockets    | Better UX than polling        |
| AI        | Google Gemini | Free tier + easy integration  |

No overengineering. Just tools that made sense for learning.

---

## 🗂 Project Structure

```
app/                      # Backend (FastAPI)
├── controllers/          # API routes
├── models/               # Database models
│   └── User, Portfolio, MarketPrice, Alert
├── services/             # Business logic (AI, pricing)
└── utils/                # JWT, password hashing, risk logic

frontend/src/             # React app
├── pages/                # Login, Dashboard, Portfolio, Alerts
└── api.js                # Centralized API calls
```

I tried to keep things organized enough that future-me doesn't cry.

---

## ▶️ How to Run It Locally

### Prerequisites

Make sure you have:
- Python 3.10+
- Node.js 18+
- PostgreSQL running on localhost:5432

### Step 1: Backend Setup

```bash
cd financial-monitoring-system
python -m venv venv
.\venv\Scripts\activate      # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend will be live at: `http://localhost:8000`
Swagger docs at: `http://localhost:8000/docs`

### Step 2: Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: `http://localhost:5173`

### Step 3: Login & Use

- Register a new account (or log in)
- Open the dashboard
- Watch prices move 📉📈

---

## 😵 Challenges I Faced (aka the real learning)

**CORS errors**
Frontend and backend refused to talk.
Fixed by explicitly allowing localhost origins.

**Python import hell**
One wrong dot in `from .models` and nothing works — with no error.

**WebSocket disconnects**
Connections randomly died. Had to add reconnect logic.

**AI rate limits**
Free tier gets exhausted fast. Added fallback responses.

**Reading my own code later**
Looked like someone else wrote it.
Solution: comments. Lots of them.

Honestly, 80% of the time was debugging, not coding — and that's where most of the learning happened.

---

## 🔮 What I'd Add Next

- Email verification
- Refresh tokens
- Support for more assets (ETH, SOL, etc.)
- Dockerized deployment
- Better alert notifications

---

## 🧠 Final Thoughts

This project was built to learn, not to impress.
It's not perfect, but it works — and more importantly, I understand every line of it.

If you're learning full-stack too:
**build → break → debug → repeat.** That's the real syllabus.
