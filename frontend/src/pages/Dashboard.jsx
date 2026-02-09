import { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import { getLatestPrices, getPriceHistory, connectToMarketStream, getMyProfile } from '../api'
import './Dashboard.css'

function Dashboard() {
  const [user, setUser] = useState(null)
  const [prices, setPrices] = useState([])
  const [livePrice, setLivePrice] = useState(null)
  const [selectedAsset, setSelectedAsset] = useState('BTC')
  const [timeRange, setTimeRange] = useState(1) // hours

  // load user profile on mount
  useEffect(() => {
    getMyProfile()
      .then(setUser)
      .catch(console.error)
  }, [])

  // load price history when asset or time changes
  useEffect(() => {
    loadPriceHistory()
  }, [selectedAsset, timeRange])

  // connect to websocket for live prices
  useEffect(() => {
    const ws = connectToMarketStream(selectedAsset, (data) => {
      setLivePrice(data)
      // add new price to chart data
      setPrices(prev => {
        const newPoint = {
          time: formatTime(data.time),
          price: data.price
        }
        // keep last 50 points
        const updated = [...prev, newPoint].slice(-50)
        return updated
      })
    })

    // cleanup on unmount
    return () => ws.close()
  }, [selectedAsset])

  async function loadPriceHistory() {
    try {
      const data = await getPriceHistory(selectedAsset, timeRange)
      // format for chart
      const formatted = data.map(p => ({
        time: formatTime(p.timestamp),
        price: p.price
      }))
      setPrices(formatted)
    } catch (err) {
      console.error('Failed to load prices:', err)
    }
  }

  // format timestamp to readable time
  function formatTime(timestamp) {
    const date = new Date(timestamp)
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  // calculate price change
  function getPriceChange() {
    if (prices.length < 2) return { value: 0, percent: 0 }
    const first = prices[0].price
    const last = prices[prices.length - 1].price
    const change = last - first
    const percent = (change / first) * 100
    return { value: change, percent }
  }

  const change = getPriceChange()

  return (
    <div className="page">
      <div className="flex-between">
        <h1>Dashboard</h1>
        {user && <span className="text-gray">Welcome, {user.email}</span>}
      </div>

      {/* price overview cards */}
      <div className="grid-3">
        <div className="card stat-card">
          <span className="label">Current Price</span>
          <span className="value">
            ${livePrice ? livePrice.price.toFixed(2) : '---'}
          </span>
          <span className="asset">{selectedAsset}</span>
        </div>

        <div className="card stat-card">
          <span className="label">Change</span>
          <span className={`value ${change.percent >= 0 ? 'text-green' : 'text-red'}`}>
            {change.percent >= 0 ? '+' : ''}{change.percent.toFixed(2)}%
          </span>
          <span className="text-gray">
            ${change.value >= 0 ? '+' : ''}{change.value.toFixed(2)}
          </span>
        </div>

        <div className="card stat-card">
          <span className="label">Data Points</span>
          <span className="value">{prices.length}</span>
          <span className="text-gray">last {timeRange}h</span>
        </div>
      </div>

      {/* controls */}
      <div className="card">
        <div className="controls">
          <div>
            <label>Asset: </label>
            <select value={selectedAsset} onChange={(e) => setSelectedAsset(e.target.value)}>
              <option value="BTC">Bitcoin (BTC)</option>
              <option value="ETH">Ethereum (ETH)</option>
              <option value="AAPL">Apple (AAPL)</option>
            </select>
          </div>
          <div>
            <label>Time Range: </label>
            <select value={timeRange} onChange={(e) => setTimeRange(Number(e.target.value))}>
              <option value={1}>Last 1 Hour</option>
              <option value={6}>Last 6 Hours</option>
              <option value={24}>Last 24 Hours</option>
            </select>
          </div>
          <button className="btn" onClick={loadPriceHistory}>Refresh</button>
        </div>
      </div>

      {/* price chart */}
      <div className="card chart-card">
        <h3>Price History - {selectedAsset}</h3>
        {prices.length === 0 ? (
          <div className="loading">No price data yet. Wait for prices to generate...</div>
        ) : (
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={prices}>
              <XAxis 
                dataKey="time" 
                stroke="#64748b"
                tick={{ fill: '#94a3b8' }}
              />
              <YAxis 
                stroke="#64748b"
                tick={{ fill: '#94a3b8' }}
                domain={['dataMin - 100', 'dataMax + 100']}
              />
              <Tooltip 
                contentStyle={{ 
                  background: '#1e293b', 
                  border: '1px solid #334155',
                  borderRadius: '8px'
                }}
              />
              <Line 
                type="monotone" 
                dataKey="price" 
                stroke="#3b82f6" 
                strokeWidth={2}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>

      {/* live indicator */}
      {livePrice && (
        <div className="live-indicator">
          🟢 Live - Last update: {formatTime(livePrice.time)}
        </div>
      )}
    </div>
  )
}

export default Dashboard
