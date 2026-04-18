# FinVue - Quick Start Guide

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 16+ with npm
- Git

### Installation

#### 1. Backend Setup

```bash
cd c:\Projects-1\financial-monitoring-system

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Install missing packages
npm install framer-motion axios
```

---

## 🏃 Running the Application

### Terminal 1 - Backend Server

```bash
cd c:\Projects-1\financial-monitoring-system
.\venv\Scripts\Activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend running at: **http://localhost:8000**

API Docs: http://localhost:8000/docs

### Terminal 2 - Frontend Dev Server

```bash
cd c:\Projects-1\financial-monitoring-system\frontend
npm run dev
```

✅ Frontend running at: **http://localhost:8080**

---

## 🧪 Testing

### Run All Tests

```bash
cd c:\Projects-1\financial-monitoring-system

# Backend API tests (21 tests)
python -m pytest test_apis.py -v

# Integration tests (6 tests)
python -m pytest integration_test.py -v

# All tests
python -m pytest -v
```

### Expected Results

```
✅ 21 Backend API tests passed
✅ 6 Integration tests passed
✅ Total: 27 tests passed
```

---

## 📱 Using the Application

### 1. Open Frontend

Navigate to: **http://localhost:8080**

### 2. Create Account

- Click "Create account" on login page
- Enter: name, email, password
- Click "Sign Up"

### 3. Login

- Enter email and password
- Click "Sign In"

### 4. Dashboard

- View portfolio summary and stats
- See portfolio performance chart
- Check recent market analyses
- Browse market news

### 5. Create Portfolio

- Go to "Portfolio" page
- Click "+ Create Portfolio"
- Enter portfolio name and type
- Click "Create"

### 6. Add Holdings

- Click on portfolio card
- Click "+ Add Holding"
- Enter: stock symbol, name, quantity, buy price
- Click "Add"

### 7. Analyze Stock

- Go to "Market Analysis"
- Enter stock symbol (e.g., AAPL)
- Click "Analyze with AI"
- View sentiment and recommendation

---

## 📁 Project Structure

```
financial-monitoring-system/
├── app/                          # Backend (FastAPI)
│   ├── controllers/              # Route handlers
│   ├── services/                 # Business logic
│   ├── models/                   # Data models
│   ├── main.py                   # App entry point
│   └── database.py               # Database config
├── frontend/                     # Frontend (React + Vite)
│   ├── src/
│   │   ├── pages/                # Page components
│   │   ├── components/           # Shared components
│   │   ├── contexts/             # React contexts
│   │   ├── lib/                  # Utilities & API
│   │   └── index.css             # Global styles
│   ├── package.json              # Dependencies
│   └── vite.config.ts            # Vite config
├── test_apis.py                  # Backend tests
├── integration_test.py            # Integration tests
├── requirements.txt              # Python dependencies
└── INTEGRATION_SUMMARY.md        # Full documentation
```

---

## 🔧 Configuration

### Backend Environment (optional)

Create `app/.env` if needed:

```
DATABASE_URL=sqlite:///./finvue.db
OPENAI_API_KEY=your_key_here
SECRET_KEY=your_secret_key

# For mock mode (default):
# Leave these commented/empty
```

### Frontend Environment (optional)

Create `frontend/.env` if needed:

```
VITE_API_BASE_URL=http://localhost:8000
```

---

## 🎯 Key Features

✅ **Authentication**

- User registration and login
- JWT token-based auth
- Secure password storage

✅ **Portfolio Management**

- Create multiple portfolios
- Track stock holdings
- Monitor buy price vs current price
- Calculate P&L automatically

✅ **Market Analysis**

- AI-powered stock analysis
- Sentiment analysis
- Buy/Sell/Hold recommendations
- Market news integration

✅ **Dashboard**

- Real-time portfolio stats
- Performance charts
- Asset allocation by sector
- Recent analyses

✅ **User Settings**

- Update profile
- Change password
- View account info

---

## 🐛 Troubleshooting

### Frontend won't connect to backend

- ✅ Check backend is running: `http://localhost:8000/docs`
- ✅ Check CORS is enabled in backend
- ✅ Verify API base URL in `frontend/src/lib/api.ts`

### Tests failing

- ✅ Ensure both servers are running
- ✅ Check database is clean: `rm finvue.db` (if using SQLite)
- ✅ Verify Python and Node versions

### Build errors

- ✅ Clear cache: `rm -rf node_modules && npm install`
- ✅ Clear Python cache: `rm -rf __pycache__ .pytest_cache`

### Port already in use

```bash
# Change backend port
python -m uvicorn app.main:app --reload --port 8001

# Change frontend port in frontend/vite.config.ts
```

---

## 📚 API Documentation

### Live API Docs

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Base URL

```
http://localhost:8000/api
```

### Authentication

All requests (except auth) require:

```
Authorization: Bearer <access_token>
```

### Main Endpoints

**Auth**

- `POST /auth/register` - Create account
- `POST /auth/login` - Login
- `GET /auth/profile` - Get profile

**Portfolio**

- `POST /portfolio/portfolios` - Create portfolio
- `GET /portfolio/portfolios` - List portfolios
- `POST /portfolio/portfolios/{id}/holdings` - Add holding
- `GET /portfolio/summary` - Get stats

**Market Analysis**

- `POST /market-analysis/analyze` - Analyze stock
- `GET /market-analysis/analyses` - List analyses
- `GET /market-analysis/news` - Get news

---

## 📊 Testing Strategy

### Unit Tests

- Backend service tests in `test_apis.py`
- 21 tests covering all major features
- Run: `pytest test_apis.py -v`

### Integration Tests

- Full feature tests in `integration_test.py`
- 6 tests validating frontend-backend communication
- Run: `pytest integration_test.py -v`

### Manual Testing

1. Create account
2. Create portfolio
3. Add holdings
4. View dashboard
5. Analyze stocks
6. Update settings

---

## 🚀 Deployment

### Build Frontend

```bash
cd frontend
npm run build
# Output: frontend/dist/
```

### Production Backend Command

```bash
# Using Gunicorn (production ASGI server)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app
```

### Docker Support (optional)

See `Dockerfile` and `docker-compose.yml` if available

---

## 📝 Notes

- All user data is stored in SQLite database (`finvue.db`)
- Tokens expire and should be refreshed via `refresh_token`
- AI analysis uses mock data when API key is not set
- Frontend is production-built with all assets minified

---

## ❓ FAQ

**Q: How do I reset the database?**
A: Delete `finvue.db` file - it will be recreated on next run

**Q: Can I use a different database?**
A: Yes, update `DATABASE_URL` in backend config

**Q: Is the frontend mobile-responsive?**
A: Yes, built with mobile-first approach using Tailwind CSS

**Q: How do I deploy to production?**
A: Use Docker or deploy to cloud service (Azure, AWS, Vercel)

**Q: Can I customize the UI?**
A: Yes, all CSS is in `frontend/src/index.css` and Tailwind config

---

**Created**: March 9, 2026
**Last Updated**: March 9, 2026
**Status**: ✅ Ready for Production
