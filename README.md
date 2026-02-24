# Financial Monitoring System

This project is a full-stack Financial Monitoring System designed to help users track, analyze, and manage their investment portfolios. It features a Python FastAPI backend and a modern React frontend.

---

## Features

- **User Authentication:** Secure login, registration, and JWT-based session management
- **Portfolio Management:** Track holdings, view portfolio performance, and manage assets
- **Market Analysis:** AI-powered market analysis and forecasting tools
- **Risk Assessment:** Utilities for risk analysis and portfolio optimization
- **Email & OTP:** Email notifications and OTP-based password reset
- **Modern UI:** Responsive React frontend with dashboard, holdings, market analysis, and settings pages

---

## Project Structure

### Backend (`app/`)

- `main.py`: FastAPI entry point
- `database.py`: Database connection and models
- `controllers/`: API route handlers (user, portfolio, market analysis)
- `models/`: ORM models for users, holdings, stocks, etc.
- `services/`: Business logic (AI analysis, user, portfolio, password reset)
- `utils/`: Utility modules (email, JWT, OTP, password, risk, forecasting)

### Frontend (`frontend/src/`)

- `components/`: Navbar, Sidebar, and reusable UI components
- `pages/`: Dashboard, Holdings, Market Analysis, Portfolio, Login, Register, Settings
- `context/`: Global authentication context
- `services/`: API service for backend communication

---

## Getting Started

### Backend Setup

1. **Install dependencies:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   pip install -r requirements.txt
   ```
2. **Run the backend server:**
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. **Navigate to frontend folder:**
   ```bash
   cd frontend
   ```
2. **Install dependencies:**
   ```bash
   npm install
   ```
3. **Run the frontend app:**
   ```bash
   npm run dev
   ```

---

## Usage

1. Register or log in as a user.
2. Add and manage your investment holdings.
3. Analyze your portfolio and view AI-powered market insights.
4. Use risk and forecasting tools to optimize your investments.

---

## Additional Documentation

- See `FRONTEND_SETUP_GUIDE.txt` and `FRONTEND_IMPLEMENTATION_COMPLETE_GUIDE.txt` in the `frontend/` folder for more details on the frontend.
- See `Project_Summary.txt` for a high-level overview.

---

## License

This project is for educational purposes. Please check individual files for license details.
