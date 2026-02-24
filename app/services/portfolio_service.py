#BASICALLY It Creates A Portfolio
#Get User PortFolios
#Add Holdings To Portfolio
#Add Holding To Portfolio
#Update Holding Price
#Delte Portfolio
#Calculate Portfolio Metricesx

from app import db
from app.models.portfolio import Portfolio
from app.models.holding import Holding
from datetime import datetime

class PortfolioService:

    def create_portfolio(user_id, name, description=None, portfolio_type="Equity"):
        try:
            # Check if portfolio with same name exists
            existing = Portfolio.query.filter_by(
                user_id=user_id,
                name=name
            ).first()
            
            if existing:
                return None, "Portfolio with this name already exists"
            
            # Create portfolio
            portfolio = Portfolio(
                user_id=user_id,
                name=name,
                description=description,
                portfolio_type=portfolio_type
            )
            
            db.session.add(portfolio)
            db.session.commit()
            
            return portfolio, "Portfolio created successfully"
        
        except Exception as e:
            db.session.rollback()
            return None, str(e)
        

        #Get All The Portfolio
    @staticmethod
    def get_user_portfolios(user_id):
        
        try:
            portfolios = Portfolio.query.filter_by(user_id=user_id).all()
            return portfolios
        except Exception as e:
            print(f"Error: {e}")
            return []
        
    """Get portfolio by ID"""
    @staticmethod
    def get_portfolio_by_id(portfolio_id):
        
        try:
            return Portfolio.query.get(portfolio_id)
        except Exception as e:
            print(f"Error: {e}")
            return None
   
   
   
   # Update Portfolio Information
    @staticmethod
    def update_portfolio(portfolio_id, **kwargs):
       
        try:
            portfolio = Portfolio.query.get(portfolio_id)
            
            if not portfolio:
                return None, "Portfolio not found"
            
            allowed_fields = ['name', 'description', 'portfolio_type']
            
            for key, value in kwargs.items():
                if key in allowed_fields:
                    setattr(portfolio, key, value)
            
            db.session.commit()
            return portfolio, "Portfolio updated successfully"
        
        except Exception as e:
            db.session.rollback()
            return None, str(e)

      #Delete Portfolio  
    @staticmethod
    def delete_portfolio(portfolio_id):
        
        try:
            portfolio = Portfolio.query.get(portfolio_id)
            
            if not portfolio:
                return None, "Portfolio not found"
            
            db.session.delete(portfolio)
            db.session.commit()
            
            return True, "Portfolio deleted successfully"
        
        except Exception as e:
            db.session.rollback()
            return None, str(e)
        

        #add Holding
    @staticmethod
    def add_holding(portfolio_id, stock_symbol, stock_name, quantity, buy_price, sector=None):
        try:
            portfolio = Portfolio.query.get(portfolio_id)
            if not portfolio: 
                return None , "Portfolio Not Found"
            
            #Check If Holding Already exists
            existing = Holding.query.filter_by(
                portfolio_id=portfolio_id,
                stock_symbol=stock_symbol
            ).first()

            if existing:
                return None, "This stock is already in portfolio"
            
            # Calculate total investment
            total_investment = quantity * buy_price
            # Create holding
            holding = Holding(
                portfolio_id=portfolio_id,
                stock_symbol=stock_symbol,
                stock_name=stock_name,
                quantity=quantity,
                average_buy_price=buy_price,
                total_investment=total_investment,
                current_price=buy_price,
                current_value=total_investment,
                sector=sector
            )
            
            # Update portfolio totals
            portfolio.total_invested += total_investment
            portfolio.total_current_value += total_investment
            portfolio.calculate_returns()
            
            db.session.add(holding)
            db.session.commit()
            
            return holding, "Stock added to portfolio"
        
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    @staticmethod
    def get_portfolio_holdings(portfolio_id):
        """Get all holdings in a portfolio"""
        try:
            holdings = Holding.query.filter_by(portfolio_id=portfolio_id).all()
            return holdings
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    
    @staticmethod
    def update_holding_price(holding_id, new_price):
       
        try:
            holding = Holding.query.get(holding_id)
            
            if not holding:
                return None, "Holding not found"
            
            # Get old values for portfolio update
            old_value = holding.current_value
            
            # Update holding price
            holding.update_current_value(new_price)
            
            # Update portfolio totals
            portfolio = holding.portfolio
            new_value = holding.current_value
            value_change = new_value - old_value
            
            portfolio.total_current_value += value_change
            portfolio.calculate_returns()
            
            # Update allocation percentages
            PortfolioService._update_allocations(portfolio)
            
            db.session.commit()
            
            return holding, "Price updated successfully"
        
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    
    
    @staticmethod
    def remove_holding(holding_id):
        try:
            holding = Holding.query.get(holding_id)
            
            if not holding:
                return None, "Holding not found"
            
            portfolio = holding.portfolio
            
            # Update portfolio totals
            portfolio.total_invested -= holding.total_investment
            portfolio.total_current_value -= holding.current_value
            
            db.session.delete(holding)
            db.session.commit()
            
            # Recalculate portfolio
            portfolio.calculate_returns()
            if portfolio.total_current_value > 0:
                PortfolioService._update_allocations(portfolio)
            
            db.session.commit()
            
            return True, "Holding removed from portfolio"
        
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    

    @staticmethod
    def _update_allocations(portfolio):
        """Update allocation percentages for all holdings"""
        holdings = portfolio.holdings
        total_value = portfolio.total_current_value
        
        if total_value > 0:
            for holding in holdings:
                holding.calculate_allocation(total_value)
    
    
    @staticmethod
    def get_portfolio_summary(portfolio_id):
     
        try:
            portfolio = Portfolio.query.get(portfolio_id)
            
            if not portfolio:
                return None
            
            holdings = portfolio.holdings
            
            summary = {
                'portfolio': portfolio.to_dict(),
                'holdings': [h.to_dict() for h in holdings],
                'total_holdings': len(holdings)
            }
            
            return summary
        
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    # Kis Id ko allcoate Hua hai
    @staticmethod
    def get_portfolio_allocation(portfolio_id):
      
        try:
            portfolio = Portfolio.query.get(portfolio_id)
            
            if not portfolio:
                return None
            
            holdings = portfolio.holdings
            allocation = []
            
            for holding in holdings:
                allocation.append({
                    'symbol': holding.stock_symbol,
                    'name': holding.stock_name,
                    'quantity': holding.quantity,
                    'value': holding.current_value,
                    'percentage': holding.allocation_percentage
                })
            
            return allocation
        
        except Exception as e:
            print(f"Error: {e}")
            return None

        

    