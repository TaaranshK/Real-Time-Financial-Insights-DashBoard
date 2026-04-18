"""
How it works:
- Big price change = High Risk
- Medium price change = Medium Risk
- Small price change = Low Risk
"""



def calculate_risk(prices):
  
    
    # Step 1: Need at least 2 prices to compare
    if len(prices) < 2:
        return "Low Risk (Not enough data)"
    
    # Step 2: Get the newest and oldest prices
    latest_price = prices[0].price    # First = newest
    oldest_price = prices[-1].price   # Last = oldest

    # Step 3: Calculate how much price changed
    difference = abs(latest_price - oldest_price)

    # Step 4: Decide risk level based on difference
    if difference > 500:
        return "High Risk (Large price movement)"
    elif difference > 200:
        return "Medium Risk (Moderate movement)"
    else:
        return "Low Risk (Stable price)"
