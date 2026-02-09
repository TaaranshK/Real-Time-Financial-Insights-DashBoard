// api.js - handles all calls to the backend

const API_URL = 'http://localhost:8000'

// get token from storage
function getToken() {
  return localStorage.getItem('token')
}

// save token after login
export function saveToken(token) {
  localStorage.setItem('token', token)
}

// clear token on logout
export function clearToken() {
  localStorage.removeItem('token')
}

// check if user is logged in
export function isLoggedIn() {
  return !!getToken()
}

// make API request with proper headers
async function request(endpoint, options = {}) {
  const token = getToken()
  
  const headers = {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` })
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers
  })

  // if response is not ok, throw error
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || 'Something went wrong')
  }

  return response.json()
}

// === AUTH APIs ===

export async function login(email, password) {
  // send email and password, get back token
  const data = await request('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password })
  })
  saveToken(data.access_token)
  return data
}

export async function register(email, password) {
  // create new account
  return request('/users/', {
    method: 'POST',
    body: JSON.stringify({ email, password })
  })
}

// === USER APIs ===

export async function getMyProfile() {
  return request('/users/me')
}

// === PORTFOLIO APIs ===

export async function getMyPortfolio() {
  return request('/portfolio/me')
}

export async function addToPortfolio(assetName, quantity) {
  return request('/portfolio/add', {
    method: 'POST',
    body: JSON.stringify({ asset_name: assetName, quantity })
  })
}

// === MARKET APIs ===

export async function getLatestPrices(assetName) {
  return request(`/market/latest/${assetName}`)
}

export async function getPriceHistory(assetName, hours = 24) {
  return request(`/market/history/${assetName}?hours=${hours}`)
}

// === AI APIs ===

export async function getMarketSummary(assetName) {
  return request(`/ai/market-summary/${assetName}`)
}

// === WEBSOCKET ===

export function connectToMarketStream(assetName, onMessage) {
  // connect to websocket for live prices
  const ws = new WebSocket(`ws://localhost:8000/ws/market/${assetName}`)
  
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    onMessage(data)
  }

  ws.onerror = (error) => {
    console.log('WebSocket error:', error)
  }

  // return the socket so caller can close it later
  return ws
}
