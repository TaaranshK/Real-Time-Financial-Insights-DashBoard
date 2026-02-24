# What it Stores
# Ai generated Analaysis
# Market Sentiment ( BUllish and Bearish)
# Key Insights

# Risk assessment



from app import db
from datetime import datetime

"""Market Analysis model - AI generated stock analysis"""
class MarketAnalysis(db.Model):
   
    __tablename__ = 'market_analyses'


    id = db.Column(db.Integer, primary_key=True)
    # Foreign keys
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
        index=True
    )
   # Analysis Data
    stock_symbol = db.Column(
        db.String(20),
        nullable=False,
        index=True
        # Example: TCS, INFY, WIPRO
    )
    stock_name = db.Column(db.String(200))
    # Ai Analysis Result
    sentiment = db.Column(
        db.String(50),
        nullable=False
        # Values: BULLISH, BEARISH, NEUTRAL
    )
    recommendation = db.Column(
        db.String(50),
        nullable=False
        # Values: STRONG BUY, BUY, HOLD, SELL, STRONG SELL
    )
    confidence_score = db.Column(
        db.Float,
        nullable=False
        # Range: 0-100
        # How confident is the AI about its recommendation
    )
    #Detailed Analysis
    executive_summary = db.Column(db.Text)   # Example: "TCS shows strong fundamentals with consistent revenue growth..."
    technical_analysis = db.Column(db.Text) #  Stock is above 200-day moving average, indicating uptrend..."
    fundamental_analysis = db.Column(db.Text)  # "P/E ratio of 20 is reasonable compared to industry average..."
    risk_assessment = db.Column(db.Text)  # "Market volatility, rupee depreciation, competition from global players..."
    key_insights = db.Column(db.Text)
    price_target = db.Column(db.Float)
    upside_potential = db.Column(db.Float)

    # Metadata
    #Number of data points used in analysis
    # Example: 24 (last 24 months of data)
    data_points_analyzed = db.Column(db.Integer) 
     # Timeframe of analysis
    # Example: "6 months", "1 year", "3 months"
    analysis_timeframe = db.Column(db.String(50))
    created_at = db.Column(
            db.DateTime,
            default=datetime.utcnow,
            nullable=False
        )
        # When analysis was created
        
    updated_at = db.Column(
            db.DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow
        )
    def __repr__(self):
        return f'<Analysis {self.stock_symbol}>'
    
    
    def to_dict(self):
        """Convert analysis to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'stock_symbol': self.stock_symbol,
            'stock_name': self.stock_name,
            'sentiment': self.sentiment,
            'recommendation': self.recommendation,
            'confidence_score': self.confidence_score,
            'executive_summary': self.executive_summary,
            'technical_analysis': self.technical_analysis,
            'fundamental_analysis': self.fundamental_analysis,
            'risk_assessment': self.risk_assessment,
            'key_insights': self.key_insights,
            'price_target': self.price_target,
            'upside_potential': self.upside_potential,
            'data_points_analyzed': self.data_points_analyzed,
            'analysis_timeframe': self.analysis_timeframe,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    