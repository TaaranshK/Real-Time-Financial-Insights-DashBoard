# 💰 Financial Monitoring System

Real-time portfolio dashboard with AI-powered stock analysis. Built with FastAPI + React + Claude AI.

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📊 **Portfolios** | Create and manage multiple investment portfolios |
| 📈 **Holdings** | Track stocks with real-time prices and P&L |
| 🤖 **AI Analysis** | Claude-powered sentiment & recommendations |
| 🔐 **Security** | Secure password reset (3-step: OTP → JWT → Reset) |
| 🌙 **Dark UI** | Modern React frontend with dark theme |
| ✅ **Tests** | 22+ passing tests with pytest |

## 🚀 Quick Start

### Requirements
- Python 3.8+ and Node.js 16+
- PostgreSQL optional (SQLite works for dev)

### Backend
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python setup_schema.py               # Create database schema
python -m uvicorn app.main:app --reload
```
**API:** http://localhost:8000/docs

### Frontend
```bash
cd frontend && npm install && npm run dev
```
**App:** http://localhost:5173

### Tests
```bash
pytest -v                            # Run all tests
python test_auth_api.py              # Test authentication
```

## 📡 API Endpoints

**Auth**
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login & get token
- `POST /api/auth/forgot-password` - Request OTP
- `POST /api/auth/verify-otp` - Verify OTP, get reset token
- `POST /api/auth/reset-password` - Reset with JWT

**Portfolio**
- `POST /api/portfolio/portfolios` - Create portfolio
- `GET /api/portfolio/portfolios` - List portfolios
- `POST /api/portfolio/portfolios/{id}/holdings` - Add stock
- `GET /api/portfolio/summary` - Dashboard stats
- `PUT /api/portfolio/holdings/{id}/price` - Update price

**Analysis**
- `POST /api/market-analysis/analyze` - Analyze stock
- `GET /api/market-analysis/analyses` - History
- `GET /api/market-analysis/news` - Market news

## 🏗️ Architecture

```
Backend (FastAPI)              Frontend (React)
├── controllers/               ├── pages/
│   ├── auth_routes.py         │   ├── Dashboard
│   ├── portfolio_routes.py     │   ├── Portfolio
│   └── market_analysis_routes.py │  ├── Holdings
├── services/                  │   └── MarketAnalysis
│   ├── auth_service.py        ├── services/
│   ├── portfolio_service.py    │   └── api.js
│   └── market_analysis_service.py ├── context/
└── utils/                     │   └── AuthContext.jsx
    ├── jwt_util.py            └── styles.css
    ├── otp_util.py
    └── email_util.py
```

## 🔧 Environment Variables

Create `.env` file:
```bash
DATABASE_URL=postgresql://user:pass@localhost/financial_db
SECRET_KEY=your-secret-key
ANTHROPIC_API_KEY=sk-...
SMTP_SERVER=smtp.gmail.com
SENDER_EMAIL=your-email@gmail.com
```

## 🎯 Key Highlights

- **Clean Architecture** - Dependency injection, separated concerns
- **Password Reset** - Secure 3-step flow with OTP + JWT
- **AI Pipeline** - News → LLM → Sentiment → Recommendation
- **Testing** - Full pytest coverage with SQLite fixtures
- **Type Safe** - Pydantic validation on all endpoints
- **Database** - SQLAlchemy ORM with PostgreSQL + SQLite support

## 📝 License

MIT - Use freely for personal or commercial projects
