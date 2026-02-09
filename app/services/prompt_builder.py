"""


What this file does:
- Takes market data
- Converts it into a text prompt for AI
- AI reads this prompt and generates analysis

Input:
    - asset_name: "BTC", "ETH", etc.
    - prices: list of price objects
    - risk_level: "Low Risk", etc.
    
    Output: A text prompt for AI
"""



def build_market_prompt(asset_name, prices, risk_level):


    # Step 1: Convert prices to readable text
    price_lines = []
    
    for price in prices:
        line = f"Price: ${price.price:.2f} at {price.timestamp}"
        price_lines.append(line)

    # Step 2: Join all lines with newlines
    price_history_text = "\n".join(price_lines)

    # Step 3: Build the final prompt
    prompt = f"""
You are a financial market analyst.

Asset: {asset_name}

Recent price history:
{price_history_text}

Risk level: {risk_level}

Task:
- Explain current market situation
- Mention risk clearly
- Keep explanation simple and grounded
- Do not make unrealistic predictions
"""

    return prompt
