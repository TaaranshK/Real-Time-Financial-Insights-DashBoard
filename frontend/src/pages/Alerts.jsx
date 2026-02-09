import { useState, useEffect } from 'react'
import { connectToMarketStream, getLatestPrices } from '../api'
import './Alerts.css'

function Alerts() {
  const [alerts, setAlerts] = useState([])
  const [triggered, setTriggered] = useState([])
  
  // form state
  const [asset, setAsset] = useState('BTC')
  const [condition, setCondition] = useState('above')
  const [price, setPrice] = useState('')
  
  // current prices for monitoring
  const [currentPrices, setCurrentPrices] = useState({})

  // connect to websocket to monitor prices
  useEffect(() => {
    // get unique assets from alerts
    const assets = [...new Set(alerts.map(a => a.asset))]
    
    // connect to each asset's stream
    const sockets = assets.map(assetName => {
      return connectToMarketStream(assetName, (data) => {
        setCurrentPrices(prev => ({
          ...prev,
          [data.asset]: data.price
        }))
        
        // check if any alerts should trigger
        checkAlerts(data.asset, data.price)
      })
    })

    // cleanup
    return () => sockets.forEach(ws => ws.close())
  }, [alerts])

  function checkAlerts(assetName, currentPrice) {
    alerts.forEach(alert => {
      if (alert.asset !== assetName) return
      if (alert.triggered) return // already triggered
      
      let shouldTrigger = false
      
      if (alert.condition === 'above' && currentPrice >= alert.price) {
        shouldTrigger = true
      }
      if (alert.condition === 'below' && currentPrice <= alert.price) {
        shouldTrigger = true
      }
      
      if (shouldTrigger) {
        // mark as triggered
        setAlerts(prev => prev.map(a => 
          a.id === alert.id ? { ...a, triggered: true } : a
        ))
        
        // add to triggered list
        const notification = {
          ...alert,
          triggeredAt: new Date().toLocaleTimeString(),
          currentPrice
        }
        setTriggered(prev => [notification, ...prev].slice(0, 10))
        
        // browser notification
        if (Notification.permission === 'granted') {
          new Notification(`Price Alert: ${alert.asset}`, {
            body: `${alert.asset} is now $${currentPrice.toFixed(2)} (${alert.condition} $${alert.price})`
          })
        }
      }
    })
  }

  function handleAddAlert(e) {
    e.preventDefault()
    if (!price) return

    const newAlert = {
      id: Date.now(),
      asset,
      condition,
      price: parseFloat(price),
      triggered: false,
      createdAt: new Date().toLocaleTimeString()
    }

    setAlerts(prev => [...prev, newAlert])
    setPrice('')
    
    // request notification permission
    if (Notification.permission === 'default') {
      Notification.requestPermission()
    }
  }

  function removeAlert(id) {
    setAlerts(prev => prev.filter(a => a.id !== id))
  }

  function clearTriggered() {
    setTriggered([])
  }

  return (
    <div className="page">
      <h1>Price Alerts</h1>
      <p className="text-gray">Get notified when prices hit your targets</p>

      {/* create alert form */}
      <div className="card">
        <h3>Create Alert</h3>
        <form onSubmit={handleAddAlert} className="alert-form">
          <select value={asset} onChange={(e) => setAsset(e.target.value)}>
            <option value="BTC">Bitcoin (BTC)</option>
            <option value="ETH">Ethereum (ETH)</option>
            <option value="AAPL">Apple (AAPL)</option>
          </select>
          
          <select value={condition} onChange={(e) => setCondition(e.target.value)}>
            <option value="above">goes above</option>
            <option value="below">goes below</option>
          </select>
          
          <input
            type="number"
            placeholder="Target price"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            step="0.01"
          />
          
          <button type="submit" className="btn">Add Alert</button>
        </form>
      </div>

      <div className="grid-2">
        {/* active alerts */}
        <div className="card">
          <h3>Active Alerts ({alerts.filter(a => !a.triggered).length})</h3>
          {alerts.filter(a => !a.triggered).length === 0 ? (
            <p className="text-gray">No active alerts</p>
          ) : (
            <div className="alert-list">
              {alerts.filter(a => !a.triggered).map(alert => (
                <div key={alert.id} className="alert-item">
                  <div className="alert-info">
                    <span className="asset-badge">{alert.asset}</span>
                    <span>
                      {alert.condition === 'above' ? '📈' : '📉'} 
                      {alert.condition} ${alert.price.toFixed(2)}
                    </span>
                    {currentPrices[alert.asset] && (
                      <span className="text-gray">
                        (now: ${currentPrices[alert.asset].toFixed(2)})
                      </span>
                    )}
                  </div>
                  <button 
                    className="btn btn-danger btn-small"
                    onClick={() => removeAlert(alert.id)}
                  >
                    Remove
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* triggered alerts */}
        <div className="card">
          <div className="flex-between">
            <h3>Triggered Alerts ({triggered.length})</h3>
            {triggered.length > 0 && (
              <button className="btn btn-small" onClick={clearTriggered}>
                Clear
              </button>
            )}
          </div>
          {triggered.length === 0 ? (
            <p className="text-gray">No triggered alerts yet</p>
          ) : (
            <div className="alert-list">
              {triggered.map((alert, i) => (
                <div key={i} className="alert-item triggered">
                  <div className="alert-info">
                    <span className="asset-badge">{alert.asset}</span>
                    <span className="text-green">
                      ✓ Triggered at ${alert.currentPrice.toFixed(2)}
                    </span>
                  </div>
                  <span className="text-gray">{alert.triggeredAt}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* notification permission notice */}
      {Notification.permission === 'default' && (
        <div className="card notice">
          💡 Enable browser notifications to get alerts even when you're on another tab.
          <button 
            className="btn btn-small"
            onClick={() => Notification.requestPermission()}
          >
            Enable
          </button>
        </div>
      )}
    </div>
  )
}

export default Alerts
