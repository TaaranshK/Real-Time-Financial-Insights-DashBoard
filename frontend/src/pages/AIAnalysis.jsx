import { useState } from 'react'
import { getMarketSummary } from '../api'
import './AIAnalysis.css'

function AIAnalysis() {
  const [query, setQuery] = useState('')
  const [asset, setAsset] = useState('BTC')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [history, setHistory] = useState([])

  // predefined questions to help users
  const quickQueries = [
    'What is the current market trend?',
    'Should I buy or sell right now?',
    'What is the risk level?',
    'Give me a market summary'
  ]

  async function handleSubmit(e) {
    e.preventDefault()
    await analyzeAsset()
  }

  async function analyzeAsset() {
    setLoading(true)
    setResult(null)

    try {
      const data = await getMarketSummary(asset)
      
      const newResult = {
        asset: data.asset,
        risk: data.risk,
        trend: data.trend,
        analysis: data.analysis,
        timestamp: new Date().toLocaleTimeString()
      }
      
      setResult(newResult)
      
      // add to history
      setHistory(prev => [newResult, ...prev].slice(0, 5))
      
    } catch (err) {
      setResult({
        error: err.message,
        timestamp: new Date().toLocaleTimeString()
      })
    } finally {
      setLoading(false)
    }
  }

  function handleQuickQuery(q) {
    setQuery(q)
    analyzeAsset()
  }

  // get color for risk level
  function getRiskColor(risk) {
    if (!risk) return 'text-gray'
    const lower = risk.toLowerCase()
    if (lower.includes('low')) return 'text-green'
    if (lower.includes('high')) return 'text-red'
    return 'text-yellow'
  }

  return (
    <div className="page">
      <h1>AI Market Analysis</h1>
      <p className="text-gray">Ask questions about market conditions in natural language</p>

      {/* query form */}
      <div className="card">
        <form onSubmit={handleSubmit} className="query-form">
          <div className="form-row">
            <select value={asset} onChange={(e) => setAsset(e.target.value)}>
              <option value="BTC">Bitcoin (BTC)</option>
              <option value="ETH">Ethereum (ETH)</option>
              <option value="AAPL">Apple (AAPL)</option>
            </select>
            
            <input
              type="text"
              placeholder="Ask something about the market..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            
            <button type="submit" className="btn" disabled={loading}>
              {loading ? 'Analyzing...' : 'Analyze'}
            </button>
          </div>
        </form>

        {/* quick queries */}
        <div className="quick-queries">
          <span className="text-gray">Quick questions: </span>
          {quickQueries.map((q, i) => (
            <button 
              key={i} 
              className="quick-btn"
              onClick={() => handleQuickQuery(q)}
            >
              {q}
            </button>
          ))}
        </div>
      </div>

      {/* loading state */}
      {loading && (
        <div className="card loading-card">
          <div className="spinner"></div>
          <p>AI is analyzing {asset} market data...</p>
        </div>
      )}

      {/* result display */}
      {result && !loading && (
        <div className="card result-card">
          {result.error ? (
            <div className="error">{result.error}</div>
          ) : (
            <>
              <div className="result-header">
                <h3>{result.asset} Analysis</h3>
                <span className="text-gray">{result.timestamp}</span>
              </div>

              <div className="metrics">
                <div className="metric">
                  <span className="label">Risk Level</span>
                  <span className={`value ${getRiskColor(result.risk)}`}>
                    {result.risk || 'Unknown'}
                  </span>
                </div>
                <div className="metric">
                  <span className="label">Trend</span>
                  <span className="value">{result.trend || 'Unknown'}</span>
                </div>
              </div>

              <div className="analysis-text">
                <h4>AI Analysis</h4>
                <p>{result.analysis}</p>
              </div>
            </>
          )}
        </div>
      )}

      {/* history */}
      {history.length > 0 && (
        <div className="card">
          <h3>Recent Queries</h3>
          <div className="history-list">
            {history.map((item, i) => (
              <div key={i} className="history-item">
                <span className="asset-badge">{item.asset}</span>
                <span className={getRiskColor(item.risk)}>{item.risk}</span>
                <span className="text-gray">{item.timestamp}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default AIAnalysis
