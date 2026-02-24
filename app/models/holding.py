from app import db
from database import datetime

class Holding(db.Model):
    __tablename__ = 'holdings'

    #Primary Key
    id = db.Column(db.Integer, primary_key=True)
    #Foreign Key
    portfolio_id = db.Column(db.Integer , db.ForeignKey('portfolio.id') , nullable=False , index=True)
    stock_symbol = db.Column(    db.String(20), nullable=False,  index=True) #TCS WIPRO
    stock_name = db.Column(db.String(100)) # TATA TECHNOLOGIES
    sector = db.Column(db.String(50)) #IT , BANKING

    #Purchase Information
    quatity = db.Column(db.Float , nullable=False) #No of Shares
    avg_buy_price = db.Column(db.Float,nullable=False) # Avg Price Of share
    total_investment = db.Column(db.Float , nullable=False) #Total Amount Invested

    #Current Market Info
    current_price = db.Column(db.Float,default=0.0) # Current  market Price Per share EG 370
    current_value =db.Clumn(db.Float,default=0.0) #EG 3700
    
    
    #Calculated Fields
    gain_loss = db.Column(
        db.Float,
        default=0.0
    )
    gain_loss_percentage = db.Column(
        db.Float,
        default=0.0
    )

    #Portfolio Allocation
    allocation_percentage = db.Column(
        db.Float,
        default=0.0
    )

    #Timestamps
    purchased_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
     # When stock was purchased
    
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f'<Holding {self.stock_symbol}>'
    
    
    def to_dict(self):
        """Convert holding to dictionary"""
        return {
            'id': self.id,
            'portfolio_id': self.portfolio_id,
            'stock_symbol': self.stock_symbol,
            'stock_name': self.stock_name,
            'sector': self.sector,
            'quantity': self.quantity,
            'average_buy_price': self.average_buy_price,
            'total_investment': self.total_investment,
            'current_price': self.current_price,
            'current_value': self.current_value,
            'gain_loss': self.gain_loss,
            'gain_loss_percentage': self.gain_loss_percentage,
            'allocation_percentage': self.allocation_percentage,
            'purchased_at': self.purchased_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    def update_current_value(self, new_price):
        """
        Update holding with new stock price
        
        Args:
            new_price: Current market price per share
        """
        self.current_price = new_price
        self.current_value = self.quantity * new_price
        self.gain_loss = self.current_value - self.total_investment
        
        if self.total_investment > 0:
            self.gain_loss_percentage = (self.gain_loss / self.total_investment) * 100
        else:
            self.gain_loss_percentage = 0
    
    def calculate_allocation(self, total_portfolio_value):
        """
        Calculate this holding's percentage of total portfolio
        
        Args:
            total_portfolio_value: Total value of all holdings in portfolio
        """
        if total_portfolio_value > 0:
            self.allocation_percentage = (self.current_value / total_portfolio_value) * 100
        else:
            self.allocation_percentage = 0