"""
forecast_utils.py - Analyzes Price Trends
==========================================

What this file does:
- Looks at recent prices
- Tells if price is going up, down, or staying same

Simple trend analysis:
- If latest > oldest = going up
- If latest < oldest = going down
- If same = sideways
"""


# ============ ANALYZE TREND ============
def analyze_trend(prices):
    """
    Analyzes if price is trending up, down, or sideways.
    
    Input: list of price objects from database
    Output: "Upward trend", "Downward trend", or "Sideways trend"
    """
    
    # Step 1: Need at least 2 prices to compare
    if len(prices) < 2:
        return "No clear trend"

    # Step 2: Get newest and oldest prices
    latest = prices[0].price    # First = newest
    previous = prices[-1].price # Last = oldest

    # Step 3: Compare and decide trend
    if latest > previous:
        return "Upward trend"
    elif latest < previous:
        return "Downward trend"
    else:
        return "Sideways trend"
