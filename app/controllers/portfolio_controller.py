Endpoints:
"""
POST /portfolios - Create portfolio
2. GET /portfolios - Get all user portfolios
3. GET /portfolios/{id} - Get specific portfolio
4. PUT /portfolios/{id} - Update portfolio
5. DELETE /portfolios/{id} - Delete portfolio
6. GET /portfolios/{id}/holdings - Get portfolio holdings
7. POST /portfolios/{id}/holdings - Add holding
8. PUT /holdings/{id}/price - Update holding price
9. DELETE /holdings/{id} - Remove holding
10. GET /portfolios/{id}/summary - Get portfolio summary
11. GET /portfolios/{id}/allocation - Get asset allocation
"""


from flask import Blueprint, request, jsonify
from app.services.portfolio_service import PortfolioService




portfolio_bp = Blueprint('portfolio', __name__, url_prefix='/api/portfolio')


#Create a new Portfolio
@portfolio_bp.route('/portfolios', methods=['POST'])
@token_required
def create_portfolio():
  
    try:
        data = request.get_json()
        user_id = request.user_data.get('user_id')
        
        # Validate required fields
        if not data or not data.get('name'):
            return jsonify({'message': 'Portfolio name is required'}), 400
        
        # Create portfolio
        portfolio, message = PortfolioService.create_portfolio(
            user_id=user_id,
            name=data.get('name'),
            description=data.get('description'),
            portfolio_type=data.get('portfolio_type', 'Equity')
        )
        
        if not portfolio:
            return jsonify({'message': message}), 400
        
        return jsonify({
            'message': message,
            'portfolio': portfolio.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


"""Get all portfolios for logged-in user"""

@portfolio_bp.route('/portfolios', methods=['GET'])
@token_required
def get_user_portfolios():
   
    try:
        user_id = request.user_data.get('user_id')
        
        portfolios = PortfolioService.get_user_portfolios(user_id)
        
        return jsonify({
            'message': 'Portfolios retrieved successfully',
            'portfolios': [p.to_dict() for p in portfolios],
            'total': len(portfolios)
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

 """Get specific portfolio"""
@portfolio_bp.route('/portfolios/<int:portfolio_id>', methods=['GET'])
@token_required
def get_portfolio(portfolio_id):
    
    try:
        portfolio = PortfolioService.get_portfolio_by_id(portfolio_id)
        
        if not portfolio:
            return jsonify({'message': 'Portfolio not found'}), 404
        
        # Check if user owns this portfolio
        if portfolio.user_id != request.user_data.get('user_id'):
            return jsonify({'message': 'Unauthorized'}), 403
        
        return jsonify({
            'message': 'Portfolio retrieved successfully',
            'portfolio': portfolio.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

 """Update portfolio"""
@portfolio_bp.route('/portfolios/<int:portfolio_id>', methods=['PUT'])
@token_required
def update_portfolio(portfolio_id):
    
    try:
        data = request.get_json()
        
        portfolio = PortfolioService.get_portfolio_by_id(portfolio_id)
        
        if not portfolio:
            return jsonify({'message': 'Portfolio not found'}), 404
        
        # Check authorization
        if portfolio.user_id != request.user_data.get('user_id'):
            return jsonify({'message': 'Unauthorized'}), 403
        
        # Update portfolio
        updated_portfolio, message = PortfolioService.update_portfolio(
            portfolio_id,
            **data
        )
        
        if not updated_portfolio:
            return jsonify({'message': message}), 400
        
        return jsonify({
            'message': message,
            'portfolio': updated_portfolio.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

   """Delete portfolio"""
@portfolio_bp.route('/portfolios/<int:portfolio_id>', methods=['DELETE'])
@token_required
def delete_portfolio(portfolio_id):
    
    try:
        portfolio = PortfolioService.get_portfolio_by_id(portfolio_id)
        
        if not portfolio:
            return jsonify({'message': 'Portfolio not found'}), 404
        
        # Check authorization
        if portfolio.user_id != request.user_data.get('user_id'):
            return jsonify({'message': 'Unauthorized'}), 403
        
        # Delete portfolio
        success, message = PortfolioService.delete_portfolio(portfolio_id)
        
        if not success:
            return jsonify({'message': message}), 400
        
        return jsonify({'message': message}), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500



 """Get all holdings in a portfolio"""


@portfolio_bp.route('/portfolios/<int:portfolio_id>/holdings', methods=['GET'])
@token_required
def get_holdings(portfolio_id):
    """Get all holdings in a portfolio"""
    try:
        portfolio = PortfolioService.get_portfolio_by_id(portfolio_id)
        
        if not portfolio:
            return jsonify({'message': 'Portfolio not found'}), 404
        
        # Check authorization
        if portfolio.user_id != request.user_data.get('user_id'):
            return jsonify({'message': 'Unauthorized'}), 403
        
        holdings = PortfolioService.get_portfolio_holdings(portfolio_id)
        
        return jsonify({
            'message': 'Holdings retrieved successfully',
            'holdings': [h.to_dict() for h in holdings],
            'total': len(holdings)
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

#Add a Stock To Portfolio
@portfolio_bp.route('/portfolios/<int:portfolio_id>/holdings', methods=['POST'])
@token_required
def add_holding(portfolio_id):
   
    try:
        data = request.get_json()
        
        portfolio = PortfolioService.get_portfolio_by_id(portfolio_id)
        
        if not portfolio:
            return jsonify({'message': 'Portfolio not found'}), 404
        
        # Check authorization
        if portfolio.user_id != request.user_data.get('user_id'):
            return jsonify({'message': 'Unauthorized'}), 403
        
        # Validate required fields
        required = ['stock_symbol', 'stock_name', 'quantity', 'buy_price']
        if not all(data.get(field) for field in required):
            return jsonify({'message': 'Missing required fields'}), 400
        
        # Add holding
        holding, message = PortfolioService.add_holding(
            portfolio_id=portfolio_id,
            stock_symbol=data.get('stock_symbol'),
            stock_name=data.get('stock_name'),
            quantity=float(data.get('quantity')),
            buy_price=float(data.get('buy_price')),
            sector=data.get('sector')
        )
        
        if not holding:
            return jsonify({'message': message}), 400
        
        return jsonify({
            'message': message,
            'holding': holding.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Update holding price (simulate price change)
@portfolio_bp.route('/holdings/<int:holding_id>/price', methods=['PUT'])
@token_required
def update_holding_price(holding_id):
  
    try:
        data = request.get_json()
        
        if not data or 'new_price' not in data:
            return jsonify({'message': 'New price is required'}), 400
        
        new_price = float(data.get('new_price'))
        
        # Update price
        holding, message = PortfolioService.update_holding_price(holding_id, new_price)
        
        if not holding:
            return jsonify({'message': message}), 400
        
        return jsonify({
            'message': message,
            'holding': holding.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

 """Remove a holding from portfolio"""
@portfolio_bp.route('/holdings/<int:holding_id>', methods=['DELETE'])
@token_required
def remove_holding(holding_id):
   
    try:
        success, message = PortfolioService.remove_holding(holding_id)
        
        if not success:
            return jsonify({'message': message}), 400
        
        return jsonify({'message': message}), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500


"""Get complete portfolio summary"""

@portfolio_bp.route('/portfolios/<int:portfolio_id>/summary', methods=['GET'])
@token_required
def get_portfolio_summary(portfolio_id):
    
    try:
        portfolio = PortfolioService.get_portfolio_by_id(portfolio_id)
        
        if not portfolio:
            return jsonify({'message': 'Portfolio not found'}), 404
        
        # Check authorization
        if portfolio.user_id != request.user_data.get('user_id'):
            return jsonify({'message': 'Unauthorized'}), 403
        
        summary = PortfolioService.get_portfolio_summary(portfolio_id)
        
        return jsonify({
            'message': 'Summary retrieved successfully',
            'data': summary
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

 Get asset allocation (for pie chart)
@portfolio_bp.route('/portfolios/<int:portfolio_id>/allocation', methods=['GET'])
@token_required
def get_allocation(portfolio_id):
   
    
   
    try:
        portfolio = PortfolioService.get_portfolio_by_id(portfolio_id)
        
        if not portfolio:
            return jsonify({'message': 'Portfolio not found'}), 404
        
        # Check authorization
        if portfolio.user_id != request.user_data.get('user_id'):
            return jsonify({'message': 'Unauthorized'}), 403
        
        allocation = PortfolioService.get_portfolio_allocation(portfolio_id)
        
        return jsonify({
            'message': 'Allocation retrieved successfully',
            'allocation': allocation
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500
