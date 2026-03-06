"""
AI Market Analysis Service

Pipeline: News Fetch -> LLM Summarization -> Sentiment Analysis -> Buy/Sell Decision

Uses Anthropic Claude API if ANTHROPIC_API_KEY is set,
otherwise falls back to a rule-based mock so the app still works.
"""

import json
import os
import random
import time
from datetime import datetime

# try to import anthropic - its optional
try:
    from anthropic import Anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


# check if we have an api key
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
USE_AI = HAS_ANTHROPIC and len(API_KEY) > 5

if USE_AI:
    client = Anthropic(api_key=API_KEY)
    MODEL = "claude-3-5-sonnet-20241022"
    print("[AI Service] Claude API connected")
else:
    client = None
    MODEL = None
    print("[AI Service] No API key found - using mock analysis")


# in a real app you'd call NewsAPI or similar
MOCK_NEWS = [
    {
        "title": "Tech earnings beat expectations across the board",
        "source": "Reuters",
        "timestamp": "2026-03-06T09:30:00",
        "category": "Technology",
        "snippet": "Major tech companies reported stronger than expected Q4 earnings, driven by AI adoption.",
    },
    {
        "title": "Fed signals potential rate pause in upcoming meeting",
        "source": "Bloomberg",
        "timestamp": "2026-03-06T08:15:00",
        "category": "Economy",
        "snippet": "Federal Reserve officials hinted at holding rates steady as inflation shows signs of cooling.",
    },
    {
        "title": "Oil prices surge amid Middle East supply concerns",
        "source": "CNBC",
        "timestamp": "2026-03-06T07:45:00",
        "category": "Energy",
        "snippet": "Crude oil jumped 3.2% as geopolitical tensions threaten supply chain disruptions.",
    },
    {
        "title": "Retail sector shows resilience despite inflation fears",
        "source": "MarketWatch",
        "timestamp": "2026-03-05T16:00:00",
        "category": "Retail",
        "snippet": "Consumer spending remained solid with retail sales up 1.4% month over month.",
    },
    {
        "title": "Global semiconductor demand continues to climb",
        "source": "Financial Times",
        "timestamp": "2026-03-05T14:30:00",
        "category": "Technology",
        "snippet": "Chip manufacturers report record backlogs as AI and EV demand drives growth.",
    },
    {
        "title": "Banking sector outlook positive as credit quality holds",
        "source": "WSJ",
        "timestamp": "2026-03-05T11:00:00",
        "category": "Finance",
        "snippet": "Major banks reported lower loan losses and improving net interest margins.",
    },
]


def get_mock_news():
    """return some realistic-looking market news"""
    return MOCK_NEWS


def _build_analysis_prompt(symbol, stock_info, news_headlines):
    """
    Build a prompt that makes the AI act like a financial analyst.
    We give it stock info and recent news, and ask for structured JSON output.
    """
    news_text = ""
    # Take The First Threee Headlines of The News With The news Title and The Source
    for n in news_headlines[:4]:
        news_text += f"- {n['title']} ({n['source']})\n"

    prompt = f"""You are a senior financial analyst at a major investment firm.
Analyze the stock {symbol} based on the information below and recent market news.

Stock Details:
- Symbol: {symbol}
- Company: {stock_info.get('name', symbol)}
- Sector: {stock_info.get('sector', 'N/A')}
- Current Price: {stock_info.get('current_price', 'N/A')}

Recent Market News:
{news_text}

Based on your analysis, provide your assessment in ONLY valid JSON format (no extra text):

{{
    "summary": "2-3 sentence overview of the stock outlook based on the news and market conditions",
    "market_sentiment": "Bullish" or "Bearish" or "Neutral",
    "recommendation": {{
        "action": "BUY" or "SELL" or "HOLD",
        "confidence": "High" or "Medium" or "Low",
        "reason": "1-2 sentence explanation for your recommendation"
    }}
}}

Keep your analysis practical and grounded. Do not make unrealistic claims.
Reply with ONLY the JSON object, nothing else."""

    return prompt


def _call_llm_with_retry(prompt, max_retries=2):
    """
    Call Claude API with simple retry logic.
    Returns the response text or None if it fails.
    """
    if not USE_AI:
        return None

    for attempt in range(max_retries + 1):
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=800,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text
        except Exception as e:
            print(f"[AI Service] API call failed (attempt {attempt + 1}): {e}")
            if attempt < max_retries:
                # wait a bit before retrying
                time.sleep(1.5 * (attempt + 1))
            else:
                print("[AI Service] All retries failed, using mock data")
                return None
    return None


def _parse_ai_response(text):
    """
    Try to extract valid JSON from the AI response.
    Claude sometimes wraps JSON in markdown code blocks.
    """
    if not text:
        return None

    # strip markdown code fences if present
    cleaned = text.strip()
    if cleaned.startswith("```"):
        # remove first line (```json or ```) and last line (```)
        lines = cleaned.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        cleaned = "\n".join(lines)

    try:
        # find the json object in the response
        start = cleaned.find("{")
        end = cleaned.rfind("}") + 1
        if start != -1 and end > start:
            parsed = json.loads(cleaned[start:end])
            return parsed
    except json.JSONDecodeError as e:
        print(f"[AI Service] Failed to parse JSON: {e}")

    return None


# I generated A simple Logic In the Case When we dont have The API KEY OR THe APi TOkens Expired
def _generate_mock_analysis(symbol, stock_info):
   
    # just pick some random but plausible values
    sentiments = ["Bullish", "Neutral", "Bearish"]
    actions = ["BUY", "HOLD", "SELL"]
    confidences = ["High", "Medium", "Low"]

    # make it slightly weighted towards positive 
    weights = [0.45, 0.35, 0.20]
    sentiment = random.choices(sentiments, weights=weights, k=1)[0]

    if sentiment == "Bullish":
        action = "BUY"
        confidence = random.choice(["High", "Medium"])
        reason = f"Positive market conditions and strong sector momentum favor {symbol}."
    elif sentiment == "Bearish":
        action = "SELL"
        confidence = random.choice(["Medium", "Low"])
        reason = f"Cautious outlook due to market headwinds affecting {stock_info.get('sector', 'this sector')}."
    else:
        action = "HOLD"
        confidence = "Medium"
        reason = f"Mixed signals for {symbol}. Monitor for clearer trend before taking action."

    sector = stock_info.get("sector", "the broader market")
    summary = (
        f"{symbol} is showing {sentiment.lower()} signals based on current market conditions. "
        f"Recent news around {sector} suggests {'opportunity for growth' if sentiment == 'Bullish' else 'some caution is warranted' if sentiment == 'Bearish' else 'a wait-and-watch approach'}. "
        f"Trading activity remains within normal ranges."
    )

    return {
        "summary": summary,
        "market_sentiment": sentiment,
        "recommendation": {
            "action": action,
            "confidence": confidence,
            "reason": reason,
        },
    }


def analyze_stock_with_ai(symbol, stock_info):
    """
    Main analysis function. This is the full pipeline:
    1. Fetch news (mock for now)
    2. Build prompt with stock data + news
    3. Call LLM for summarization + sentiment + recommendation
    4. Parse and return structured output

    Returns a dict with: summary, market_sentiment, recommendation, news_headlines
    """
    # step 1: get relevant news
    news = get_mock_news()

    # step 2: build the prompt
    prompt = _build_analysis_prompt(symbol, stock_info, news)

    # step 3: call the LLM
    raw_response = _call_llm_with_retry(prompt)

    # step 4: parse the response
    result = _parse_ai_response(raw_response)

    # if AI didn't work, use our fallback
    if not result:
        result = _generate_mock_analysis(symbol, stock_info)

    # make sure the output has all required fields
    output = {
        "summary": result.get("summary", "Analysis unavailable"),
        "market_sentiment": result.get("market_sentiment", "Neutral"),
        "recommendation": result.get("recommendation", {
            "action": "HOLD",
            "confidence": "Low",
            "reason": "Insufficient data for analysis",
        }),
        "news_headlines": [n["title"] for n in news[:4]],
    }

    return output
