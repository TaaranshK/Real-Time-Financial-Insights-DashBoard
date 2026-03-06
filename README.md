# Financial Monitoring System

Full-stack financial monitoring app with AI-powered market analysis.

**Tech Stack:** FastAPI (Python) + React + Anthropic Claude API

---

## What it does

- **Portfolio Management** - Create portfolios, add stock holdings, track prices
- **AI Market Analysis** - Analyze any stock and get sentiment + buy/sell recommendations
- **Market News** - See latest financial news headlines
- **Dashboard** - Overview of your portfolio value, P&L, and recent AI insights

---

## Project Structure

```
app/
  main.py              <- All API routes + Pydantic validation models
  services/
    ai_service.py      <- GenAI pipeline (news -> LLM -> sentiment -> recommendation)
  utils/
    risk_utils.py      <- Risk calculation helpers
    forecast_utils.py  <- Trend analysis helpers

frontend/src/
  pages/               <- Dashboard, Portfolio, Holdings, MarketAnalysis, etc.
  components/          <- Navbar, Sidebar
  context/             <- Auth state management
  services/api.js      <- Axios API client

test_apis.py           <- pytest backend tests
test_login.py          <- Auth flow tests
```

---

## Getting Started

### Backend

```bash
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt

# optional: set your API key for real AI analysis
set ANTHROPIC_API_KEY=your_key_here

uvicorn app.main:app --reload
```

API docs at http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Opens at http://localhost:5173

### Run Tests

```bash
pytest test_apis.py test_login.py -v
```

---

## AI Analysis Pipeline

The market analysis feature follows this pipeline:

1. **Fetch News** - Gets relevant financial news
2. **Build Prompt** - Combines stock info + news into a prompt
3. **Call LLM** - Sends to Claude API with retry logic
4. **Parse Response** - Extracts structured JSON
5. **Return Result** - Summary, sentiment, and buy/sell recommendation

If no API key is set, it falls back to a mock analysis so the app still works.

---

## API Endpoints

| Method | Endpoint                                | Description       |
| ------ | --------------------------------------- | ----------------- |
| POST   | /api/auth/register                      | Register new user |
| POST   | /api/auth/login                         | Login             |
| GET    | /api/auth/profile                       | Get profile       |
| PUT    | /api/auth/profile                       | Update profile    |
| POST   | /api/portfolio/portfolios               | Create portfolio  |
| GET    | /api/portfolio/portfolios               | List portfolios   |
| POST   | /api/portfolio/portfolios/{id}/holdings | Add holding       |
| GET    | /api/portfolio/portfolios/{id}/holdings | Get holdings      |
| PUT    | /api/portfolio/holdings/{id}/price      | Update price      |
| GET    | /api/portfolio/summary                  | Dashboard stats   |
| POST   | /api/market-analysis/analyze            | Run AI analysis   |
| GET    | /api/market-analysis/analyses           | Past analyses     |
| GET    | /api/market-analysis/news               | Market news       |
