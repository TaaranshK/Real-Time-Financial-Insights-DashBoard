"""
ai_service.py - Talks to AI (Google Gemini)
============================================

What this file does:
- Sends market data to AI
- Gets human-like analysis back
- Falls back to simple message if AI is not available
"""

from .prompt_builder import build_market_prompt



GEMINI_API_KEY = "AIzaSyBkson602oa5SCp4Gf-4qumeG_g-M70OLA"


# ============ TRY TO IMPORT GEMINI ============
try:
    import google.generativeai as genai
    
    # Configure Gemini with API key
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Create the model (gemini-2.0-flash is fast and has good free tier limits)
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    gemini_available = True

except Exception:
   
    gemini_available = False
    model = None


# ============ GENERATE AI RESPONSE ============
def generate_ai_response(asset_name, prices, risk_level):
    """
    Gets AI analysis for market data using Google Gemini.
    
    Input:
    - asset_name: "BTC", "ETH", etc.
    - prices: list of price objects from database
    - risk_level: "Low Risk", "Medium Risk", etc.
    
    Output:
    - {"analysis": "...", "source": "gemini" or "fallback"}
    """

    # Step 1: Build the prompt
    prompt = build_market_prompt(asset_name, prices, risk_level)

    # Step 2: If Gemini is not configured, return fallback
    if not gemini_available or model is None:
        return {
            "analysis": f"AI service not configured. Current risk level is {risk_level}.",
            "source": "fallback"
        }

    # Step 3: Try to call Gemini
    try:
        # Add system instruction to prompt
        full_prompt = "You are a careful financial analyst.\n\n" + prompt
        
        # Generate response
        response = model.generate_content(full_prompt)

        # Step 4: Extract the response text
        ai_text = response.text

        return {
            "analysis": ai_text,
            "source": "gemini"
        }

    except Exception as e:
        # Step 5: If AI fails, check if it's a rate limit error
        error_msg = str(e).lower()
        print(f"Gemini Error: {e}")
        
        # Rate limit hit - provide helpful fallback instead of ugly error
        if "429" in str(e) or "quota" in error_msg or "rate" in error_msg:
            return {
                "analysis": f"AI is temporarily busy (free tier limit reached). Based on calculations: {risk_level}. The market shows normal volatility patterns. Try again in 1 minute for full AI analysis.",
                "source": "rate_limited"
            }
        
        # Other errors
        return {
            "analysis": f"AI unavailable. Based on data: {risk_level}.",
            "source": "error"
        }
