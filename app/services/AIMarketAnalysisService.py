# What it does:
# - Takes stock data
# - Uses Claude API to analyze
# - Generates buy/sell recommendations
# - Saves analysis to database
# - Returns formatted analysis



import os
import json
from datetime import datetime
from anthropic import Anthropic
from app import db
from app.models.market_analysis import MarketAnalysis
from app.models.stock import Stock
from dotenv import load_dotenv

load_dotenv()


class AiMarketAnalysis:
    #Initialize Anthropic Client
    client = Anthropic()
    Model = "claude-3-5-sonnet-20241022"

    # Analyze Stock using AI

    def analyze_stock(user_id ,  stock_symbol, stock_data=None):
        try:
            # Get or create stock in database
            stock = Stock.query.filter_by(symbol=stock_symbol).first()
            if not stock and stock_data:
                    # Create stock if doesn't exist
                    stock = Stock(
                        symbol=stock_symbol,
                        name=stock_data.get('name', stock_symbol),
                        sector=stock_data.get('sector'),
                        current_price=stock_data.get('current_price', 0),
                        pe_ratio=stock_data.get('pe_ratio'),
                        dividend_yield=stock_data.get('dividend_yield'),
                        week_52_high=stock_data.get('52_week_high'),
                        week_52_low=stock_data.get('52_week_low'),
                        market_cap=stock_data.get('market_cap')
                    )
                    db.session.add(stock)
                    db.session.commit()
                    # Prepare prompt for Claude
                    prompt = AIMarketAnalysisService._prepare_analysis_prompt(
                        stock_symbol,
                        stock_data)
                    #Call Claude API
                    analysis_text = AIMarketAnalysisService._call_claude_api(prompt)

                    parsed_analysis = AIMarketAnalysisService._parse_analysis(analysis_text)
                    
                    # Save analysis to database
                    market_analysis = MarketAnalysis(
                        user_id=user_id,
                        stock_symbol=stock_symbol,
                        stock_name=stock_data.get('name') if stock_data else stock.name,
                        sentiment=parsed_analysis.get('sentiment'),
                        recommendation=parsed_analysis.get('recommendation'),
                        confidence_score=parsed_analysis.get('confidence_score', 0),
                        executive_summary=parsed_analysis.get('executive_summary'),
                        technical_analysis=parsed_analysis.get('technical_analysis'),
                        fundamental_analysis=parsed_analysis.get('fundamental_analysis'),
                        risk_assessment=parsed_analysis.get('risk_assessment'),
                        key_insights=parsed_analysis.get('key_insights'),
                        price_target=parsed_analysis.get('price_target'),
                        upside_potential=parsed_analysis.get('upside_potential'),
                        data_points_analyzed=parsed_analysis.get('data_points_analyzed'),
                        analysis_timeframe=parsed_analysis.get('analysis_timeframe')
                    )
                    
                    db.session.add(market_analysis)
                    db.session.commit()

                    return market_analysis, "Analysis completed successfully"
        
        except Exception as e:
            db.session.rollback()
            return None, str(e)
        


        #Prompt For Claude Ai'

    @staticmethod
    def _prepare_analysis_prompt(stock_symbol, stock_data):
        """Prepare prompt for Claude API"""
        
        if not stock_data:
            stock_data = {}
        
        prompt = f"""
        Analyze the stock: {stock_symbol}
        
        Stock Information:
        - Company: {stock_data.get('name', 'Unknown')}
        - Sector: {stock_data.get('sector', 'N/A')}
        - Current Price: ₹{stock_data.get('current_price', 'N/A')}
        - P/E Ratio: {stock_data.get('pe_ratio', 'N/A')}
        - Dividend Yield: {stock_data.get('dividend_yield', 'N/A')}%
        - 52 Week High: ₹{stock_data.get('52_week_high', 'N/A')}
        - 52 Week Low: ₹{stock_data.get('52_week_low', 'N/A')}
        - Market Cap: {stock_data.get('market_cap', 'N/A')}
        
        Please provide a detailed stock analysis in JSON format with the following fields:
        {{
            "sentiment": "BULLISH/BEARISH/NEUTRAL",
            "recommendation": "STRONG BUY/BUY/HOLD/SELL/STRONG SELL",
            "confidence_score": 85,
            "executive_summary": "2-3 paragraph summary of the stock outlook",
            "technical_analysis": "Analysis of price trends and technical indicators",
            "fundamental_analysis": "Analysis of company fundamentals, P/E ratio, dividend yield",
            "risk_assessment": "Key risks and challenges",
            "key_insights": "Bullet points of important insights",
            "price_target": 3800,
            "upside_potential": 15.5,
            "data_points_analyzed": 12,
            "analysis_timeframe": "6 months"
        }}
        
        Make the analysis realistic, detailed, and suitable for Indian stock market.
        """
        
        return prompt
    
    @staticmethod
    def _call_claude_api(prompt):
        """Call Claude API"""
        
        try:
            message = AIMarketAnalysisService.client.messages.create(
                model=AIMarketAnalysisService.MODEL,
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            return message.content[0].text
        
        except Exception as e:
            print(f"Error calling Claude API: {e}")
            return None
        
    @staticmethod
    def _parse_analysis(analysis_text):
        """Parse Claude's response and extract JSON"""
        
        try:
            # Find JSON in response
            start = analysis_text.find('{')
            end = analysis_text.rfind('}') + 1
            
            if start != -1 and end > start:
                json_str = analysis_text[start:end]
                parsed = json.loads(json_str)
                return parsed
            else:
                # If no JSON found, return default structure
                return {
                    'sentiment': 'NEUTRAL',
                    'recommendation': 'HOLD',
                    'confidence_score': 50,
                    'executive_summary': analysis_text,
                    'technical_analysis': '',
                    'fundamental_analysis': '',
                    'risk_assessment': '',
                    'key_insights': '',
                    'price_target': 0,
                    'upside_potential': 0,
                    'data_points_analyzed': 0,
                    'analysis_timeframe': '6 months'
                }
        
        except json.JSONDecodeError:
            return {
                'sentiment': 'NEUTRAL',
                'recommendation': 'HOLD',
                'confidence_score': 50,
                'executive_summary': analysis_text,
                'technical_analysis': '',
                'fundamental_analysis': '',
                'risk_assessment': '',
                'key_insights': '',
                'price_target': 0,
                'upside_potential': 0,
                'data_points_analyzed': 0,
                'analysis_timeframe': '6 months'
            }
    
    
    @staticmethod
    def get_user_analyses(user_id, limit=10):
        """Get all analyses for a user"""
        try:
            analyses = MarketAnalysis.query.filter_by(user_id=user_id)\
                .order_by(MarketAnalysis.created_at.desc())\
                .limit(limit)\
                .all()
            
            return analyses
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    
    @staticmethod
    def get_analysis_by_id(analysis_id):
        """Get specific analysis"""
        try:
            return MarketAnalysis.query.get(analysis_id)
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    
    @staticmethod
    def compare_stocks(user_id, stock_symbols, stock_data_list=None):
        """
        Compare multiple stocks
        
        Args:
            user_id: User ID
            stock_symbols: List of stock symbols ["TCS", "INFY", "WIPRO"]
            stock_data_list: List of stock data dicts
        
        Returns:
            Comparison analysis
        """
        try:
            # Analyze each stock
            analyses = []
            for i, symbol in enumerate(stock_symbols):
                stock_data = stock_data_list[i] if stock_data_list else None
                analysis, msg = AIMarketAnalysisService.analyze_stock(
                    user_id,
                    symbol,
                    stock_data
                )
                if analysis:
                    analyses.append(analysis)
            
            return analyses, "Comparison completed"
        
        except Exception as e:
            return None, str(e)
    
    
    @staticmethod
    def get_portfolio_analysis(user_id, holdings_data):
        """
        Get AI analysis for entire portfolio
    
        """
        try:
            prompt = f"""
            Analyze this investment portfolio:
            
            Holdings:
            {json.dumps(holdings_data, indent=2)}
            
            Please provide:
            1. Overall portfolio health
            2. Asset allocation feedback
            3. Risk assessment
            4. Recommendations for improvement
            5. Expected portfolio performance (next 6 months)
            
            Return as JSON with these fields:
            {{
                "portfolio_health": "EXCELLENT/GOOD/AVERAGE/POOR",
                "risk_level": "LOW/MEDIUM/HIGH",
                "diversification_score": 75,
                "overall_recommendation": "Analysis text",
                "allocation_feedback": "Analysis text",
                "risk_assessment": "Analysis text",
                "improvement_suggestions": ["Suggestion 1", "Suggestion 2"],
                "expected_return": 12.5,
                "holding_recommendations": {{
                    "TCS": "HOLD/BUY/SELL",
                    "INFY": "BUY/HOLD/SELL"
                }}
            }}
            """
            
            message = AIMarketAnalysisService.client.messages.create(
                model=AIMarketAnalysisService.MODEL,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            analysis_text = message.content[0].text
            
            # Parse JSON
            start = analysis_text.find('{')
            end = analysis_text.rfind('}') + 1
            
            if start != -1 and end > start:
                json_str = analysis_text[start:end]
                parsed = json.loads(json_str)
                return parsed, "Portfolio analysis completed"
            else:
                return {"analysis": analysis_text}, "Analysis completed"
        
        except Exception as e:
            return None, str(e)

    
