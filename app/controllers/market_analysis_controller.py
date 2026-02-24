# # ndpoints:
# 1. POST /analyze - Analyze a single stock
# 2. GET /analyses - Get user's analysis history
# 3. GET /analyses/{id} - Get specific analysis
# 4. POST /compare - Compare multiple stocks
# # 5. POST /portfolio-analysis - Analyze entire portfolio

from flask import Blueprint, request, jsonify
from app.services.ai_market_analysis_service import AIMarketAnalysisService

# Create blueprint
market_analysis_bp = Blueprint('market_analysis', __name__, url_prefix='/api/market-analysis')


# SINGLE STOCK ANALYSIS

@market_analysis_bp.route('/analyze', methods=['POST'])
@token_required
def analyze_stock():
    try:
        data = request.get_json()
        user_id = request.user_data.get('user_id')
        
        # Validate required fields
        if not data or not data.get('stock_symbol'):
            return jsonify({'message': 'Stock symbol is required'}), 400
        
        stock_symbol = data.get('stock_symbol').upper()
        stock_data = data.get('stock_data')
        
        # Call AI analysis service
        analysis, message = AIMarketAnalysisService.analyze_stock(
            user_id=user_id,
            stock_symbol=stock_symbol,
            stock_data=stock_data
        )
        
        if not analysis:
            return jsonify({'message': message}), 400
        
        return jsonify({
            'message': 'Analysis completed successfully',
            'analysis': analysis.to_dict()
        }), 201 # Success
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500 # Internal Server Error


#Get All Analysis For Loggedd in

@market_analysis_bp.route('/analyses', methods=['GET'])
@token_required
def get_analyses():
    """Get all analyses for logged-in user"""
    try:
        user_id = request.user_data.get('user_id')
        limit = request.args.get('limit', 10, type=int)
        
        analyses = AIMarketAnalysisService.get_user_analyses(user_id, limit)
        
        return jsonify({
            'message': 'Analyses retrieved successfully',
            'analyses': [a.to_dict() for a in analyses],
            'total': len(analyses)
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

"""Get specific analysis"""
@market_analysis_bp.route('/analyses/<int:analysis_id>', methods=['GET'])
@token_required
def get_analysis(analysis_id):
    
    try:
        user_id = request.user_data.get('user_id')
        analysis = AIMarketAnalysisService.get_analysis_by_id(analysis_id)
        
        if not analysis:
            return jsonify({'message': 'Analysis not found'}), 404
        
        # Check if user owns this analysis
        if analysis.user_id != user_id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        return jsonify({
            'message': 'Analysis retrieved successfully',
            'analysis': analysis.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    
# Compare Multiple Stocks
@market_analysis_bp.route('/compare', methods=['POST'])
@token_required
def compare_stocks():
    try:
        data = request.get_json()
        user_id = request.user_data.get('user_id')
        
        # Validate required fields
        if not data or not data.get('stock_symbols'):
            return jsonify({'message': 'Stock symbols array is required'}), 400
        
        stock_symbols = [s.upper() for s in data.get('stock_symbols')]
        stock_data_list = data.get('stock_data')
        
        if len(stock_symbols) > 5:
            return jsonify({'message': 'Can compare maximum 5 stocks at a time'}), 400
        
        # Compare stocks
        analyses, message = AIMarketAnalysisService.compare_stocks(
            user_id=user_id,
            stock_symbols=stock_symbols,
            stock_data_list=stock_data_list
        )
        
        if not analyses:
            return jsonify({'message': message}), 400
        
        return jsonify({
            'message': message,
            'analyses': [a.to_dict() for a in analyses],
            'total': len(analyses)
        }), 201
    
    except Exception as e:
        return jsonify({'message': str(e)}),

@market_analysis_bp.route('/portfolio-analysis', methods=['POST'])
@token_required
def analyze_portfolio():
    try:
        data = request.get_json()
        user_id = request.user_data.get('user_id')
        
        # Validate required fields
        if not data or not data.get('holdings'):
            return jsonify({'message': 'Holdings array is required'}), 400
        
        holdings_data = data.get('holdings')
        
        if len(holdings_data) == 0:
            return jsonify({'message': 'Portfolio cannot be empty'}), 400
        
        # Get portfolio analysis from AI
        analysis, message = AIMarketAnalysisService.get_portfolio_analysis(
            user_id=user_id,
            holdings_data=holdings_data
        )
        
        if not analysis:
            return jsonify({'message': message}), 400
        
        return jsonify({
            'message': message,
            'portfolio_analysis': analysis
        }), 201
    
    except Exception as e:
        return jsonify({'message': str(e)}),

@market_analysis_bp.route('/sentiment', methods=['POST'])
@token_required
def get_sentiment():
   
    try:
        data = request.get_json()
        user_id = request.user_data.get('user_id')
        
        if not data or not data.get('stock_symbol'):
            return jsonify({'message': 'Stock symbol is required'}), 400
        
        stock_symbol = data.get('stock_symbol').upper()
        news_summary = data.get('news_summary', '')
        
        # Quick sentiment analysis using Claude
        prompt = f"""
        Analyze the sentiment for stock {stock_symbol}
        
        News/Info: {news_summary}
        
        Provide quick sentiment analysis in JSON:
        {{
            "sentiment": "BULLISH/NEUTRAL/BEARISH",
            "confidence": 85,
            "reason": "Brief explanation"
        }}
        """
        
        from app.services.ai_market_analysis_service import AIMarketAnalysisService
        message = AIMarketAnalysisService.client.messages.create(
            model=AIMarketAnalysisService.MODEL,
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        
        # Parse JSON
        import json
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        
        if start != -1 and end > start:
            json_str = response_text[start:end]
            sentiment_data = json.loads(json_str)
        else:
            sentiment_data = {"sentiment": "NEUTRAL", "confidence": 50}
        
        return jsonify({
            'message': 'Sentiment analysis completed',
            'data': sentiment_data
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500