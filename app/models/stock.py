# What it stores:
# - Stock symbol (TCS, INFY, WIPRO)
# - Company name
# - Sector
# - Current price
# - Day's change
# - 52 week high/low
# - Market cap
# - Last updated time

# Used for:
# - Search stocks
# - Get stock info
# - Display market data


from app import db
from datetime import datetime

class Stock(db.Model):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True)

    #Stock Identification
    symbol = db.Column(
        db.String(20),
        unique=True,
        nullable=False,
        index=True
        # Example: TCS, INFY, WIPRO
    )

    name = db.Column(
        db.String(200),
        nullable=False
        # Example: Tata Consultancy Services Limited
    )

    sector = db.Column(db.String(100)) #IT BAnking Pharma
    industry = db.Column(db.String(100)) # Software Banking Services
    current_price = db.Column(
        db.Float,
        nullable=False,
        default=0.0
    )
    day_change = db.Column( #Change  in Price Today
        db.Float,
        default=0.0
    )
    day_change_percentage = db.Column(
        db.Float,
        default=0.0
    )
    week_52_high = db.Column(db.Float) # 52 weeks Highest Price
    week_52_low = db.Column(db.Float)
    market_cap = db.Column(db.String(50)) #Market Capatalization
    pe_ratio = db.Column(db.Float) # Price To Earnings Ratiuo
    dividend_yield = db.Column(db.Float)
    volume = db.Column(db.String(50)) #trading Volume
    
    # Timestamps
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    def __repr__(self):
        return f'<Stock {self.symbol}>'
    
    
    def to_dict(self):
        """Convert stock to dictionary"""
        return {
            'id': self.id,
            'symbol': self.symbol,
            'name': self.name,
            'sector': self.sector,
            'industry': self.industry,
            'current_price': self.current_price,
            'day_change': self.day_change,
            'day_change_percentage': self.day_change_percentage,
            'week_52_high': self.week_52_high,
            'week_52_low': self.week_52_low,
            'market_cap': self.market_cap,
            'pe_ratio': self.pe_ratio,
            'dividend_yield': self.dividend_yield,
            'volume': self.volume,
            'updated_at': self.updated_at.isoformat()
        }
