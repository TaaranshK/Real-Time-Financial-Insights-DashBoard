#So What it stores
#Portfolio Name ("Eg - MY Trading Account")
#Total Investment Amount
#Portfolio Type ( Eg "Equity, Mutual Funds")
#Creation and Update Dates
#Also One User Can Have Multiple Portfolios
 #Eg 1 -> Portfolio 1: "Trading account 1" 
# Portfolio 2: -> Long Term

from app import db
from datetime import datetime

class Portfolio(db.Model):
    __tablename__ = 'portfolios'

    #Primary Key
    id = db.Column(db.Integer, primary_key=True)

    #Foreign Key
    user_id = db.Column(db.Integer , db.ForeignKey('user.id') , nullable=False , index=True)
    
    #Basic info

    name = db.Column(db.String(100) , nullable = Fasle)

    #description

    description = db.Column(db.String(500))
    portfolio_type = db.Column(db.String(50) , default="Equity")
    total_invested = db.Column(db.Float , default=0.0, nullable=False)
    
    #Financial Information
    total_crrent_value = db.Column(db.Float , default = 0.0 , nullable=False)
    cash_available = db.Column( db.Float,default=0.0, nullable=False)

    #Univested Cash in Portfolio
    total_gain_loss = db.Column(db.Float , default=0.0)

    #Gain/Loss in 
    total_gain_loss_percentage = db.Column(db.Float , default=0.0)

    #TimeStamps
    created_at = db.Column(db.DateTime , default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime , default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to Holdings
    holdings = db.relationship(
        'Holding',
        backref='portfolio',
        lazy=True,
        cascade='all, delete-orphan'
    )
    
    
    def __repr__(self):
        return f'<Portfolio {self.name}>'
    
    
    def to_dict(self):
        """Convert portfolio to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'portfolio_type': self.portfolio_type,
            'total_invested': self.total_invested,
            'total_current_value': self.total_current_value,
            'cash_available': self.cash_available,
            'total_gain_loss': self.total_gain_loss,
            'total_gain_loss_percentage': self.total_gain_loss_percentage,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def calculate_returns(self):
        """Calculate gain/loss and percentage"""
        if self.total_invested > 0:
            self.total_gain_loss = self.total_current_value - self.total_invested
            self.total_gain_loss_percentage = (self.total_gain_loss / self.total_invested) * 100
        else:
            self.total_gain_loss = 0
            self.total_gain_loss_percentage = 0
