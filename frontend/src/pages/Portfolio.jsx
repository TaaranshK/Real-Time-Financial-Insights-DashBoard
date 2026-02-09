import { useState, useEffect } from 'react'
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts'
import { getMyPortfolio, addToPortfolio, getLatestPrices } from '../api'
import './Portfolio.css'

// colors for pie chart
const COLORS = ['#3b82f6', '#22c55e', '#eab308', '#ef4444', '#8b5cf6', '#ec4899']

function Portfolio() {
  const [portfolio, setPortfolio] = useState([])
  const [loading, setLoading] = useState(true)
  const [adding, setAdding] = useState(false)
  const [error, setError] = useState('')
  
  // form state
  const [assetName, setAssetName] = useState('BTC')
  const [quantity, setQuantity] = useState('')

  // load portfolio on mount
  useEffect(() => {
    loadPortfolio()
  }, [])

  async function loadPortfolio() {
    setLoading(true)
    try {
      const data = await getMyPortfolio()
      
      // get current prices for each asset
      const withPrices = await Promise.all(
        data.map(async (item) => {
          try {
            const prices = await getLatestPrices(item.asset_name)
            const currentPrice = prices.length > 0 ? prices[0].price : 0
            return {
              ...item,
              price: currentPrice,
              value: currentPrice * item.quantity
            }
          } catch {
            return { ...item, price: 0, value: 0 }
          }
        })
      )
      
      setPortfolio(withPrices)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function handleAdd(e) {
    e.preventDefault()
    if (!quantity || quantity <= 0) return

    setAdding(true)
    setError('')
    
    try {
      await addToPortfolio(assetName, parseFloat(quantity))
      setQuantity('')
      loadPortfolio() // refresh list
    } catch (err) {
      setError(err.message)
    } finally {
      setAdding(false)
    }
  }

  // calculate total portfolio value
  const totalValue = portfolio.reduce((sum, item) => sum + (item.value || 0), 0)

  // prepare data for pie chart
  const chartData = portfolio.map(item => ({
    name: item.asset_name,
    value: item.value || 0
  }))

  if (loading) {
    return <div className="page loading">Loading portfolio...</div>
  }

  return (
    <div className="page">
      <h1>Portfolio</h1>

      {error && <div className="card error-card">{error}</div>}

      {/* add asset form */}
      <div className="card">
        <h3>Add Asset</h3>
        <form onSubmit={handleAdd} className="add-form">
          <select value={assetName} onChange={(e) => setAssetName(e.target.value)}>
            <option value="BTC">Bitcoin (BTC)</option>
            <option value="ETH">Ethereum (ETH)</option>
            <option value="AAPL">Apple (AAPL)</option>
            <option value="GOOGL">Google (GOOGL)</option>
            <option value="TSLA">Tesla (TSLA)</option>
          </select>
          
          <input
            type="number"
            placeholder="Quantity"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            step="0.0001"
            min="0"
          />
          
          <button type="submit" className="btn" disabled={adding}>
            {adding ? 'Adding...' : 'Add to Portfolio'}
          </button>
        </form>
      </div>

      <div className="grid-2">
        {/* portfolio summary */}
        <div className="card">
          <h3>Total Value</h3>
          <div className="total-value">${totalValue.toFixed(2)}</div>
          <p className="text-gray">{portfolio.length} assets</p>
        </div>

        {/* pie chart */}
        <div className="card">
          <h3>Allocation</h3>
          {chartData.length === 0 ? (
            <p className="text-gray">No assets yet</p>
          ) : (
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie
                  data={chartData}
                  cx="50%"
                  cy="50%"
                  innerRadius={50}
                  outerRadius={80}
                  dataKey="value"
                  label={({ name }) => name}
                >
                  {chartData.map((entry, index) => (
                    <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip 
                  formatter={(value) => `$${value.toFixed(2)}`}
                  contentStyle={{ background: '#1e293b', border: '1px solid #334155' }}
                />
              </PieChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      {/* asset list */}
      <div className="card">
        <h3>Your Assets</h3>
        {portfolio.length === 0 ? (
          <p className="text-gray">Add your first asset above!</p>
        ) : (
          <table className="asset-table">
            <thead>
              <tr>
                <th>Asset</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Value</th>
                <th>% of Portfolio</th>
              </tr>
            </thead>
            <tbody>
              {portfolio.map((item) => (
                <tr key={item.id}>
                  <td className="asset-name">{item.asset_name}</td>
                  <td>{item.quantity.toFixed(4)}</td>
                  <td>${item.price?.toFixed(2) || '0.00'}</td>
                  <td className="text-green">${item.value?.toFixed(2) || '0.00'}</td>
                  <td>
                    {totalValue > 0 
                      ? ((item.value / totalValue) * 100).toFixed(1) 
                      : 0}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default Portfolio
