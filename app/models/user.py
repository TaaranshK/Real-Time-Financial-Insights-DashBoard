from app import db 
from datetime import datetime
import enum

class UserRole(enum.ENUM):
    "User Roles in the System"
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    INVESTOR = " INVESTOR"
    USER = "USER"

class User(db.Model):

    __tablename__ = 'users'

    #Primary key

    id = db.Column(db.Integer , primary_key = True)
    
    #Basic Information
    username = db.Column( db.String(80) , unique=True, nullable=False , index=True)
    email = db.Column(  db.String(120),unique=True,nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    phone = db.Column(db.String(20))


    #Account Status
    is_active = db.Column(db.Boolean , default=True)
    is_verified = db.Column(db.Boolean , default=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.INVESTOR,nullable=False)

    #OTP 
    otp = db.Column(db.String(6))
    otp_expiry = db.Column(db.DateTime)

    #password Reset
    reset_token = db.Column(db.String(255))
    reset_token_expiry = db.Column(db.DateTime)

    #Timestamp
    created_at  = db.Column(db.DateTime, default=datetime.utcnow,nullable=False)
    updated_at = db.Column(db.DateTime,default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    #To String 
    def __repr__(self):
        """String representation of user"""
        return f'<User {self.email}>'
    
    #To Dict or To JSON
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'role': self.role.value,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }