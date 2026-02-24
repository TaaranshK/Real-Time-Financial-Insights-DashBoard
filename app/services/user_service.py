from app import db 
from app.models.user import User
from app.utils.password_util import PasswordUtil
from app.utils.jwt_util import JwtUtil
from datetime import datetime

class UserService:
    # "Service Class For User Operations"


    ##### CRRRRREEEEAAAATINNNGGG AAA USSSSEERRR
    @staticmethod
    def create_user(username , email , password, first_name=None, last_name=None, phone=None):
        #Check if user already exissts
        try:
            if User.query.filter_by(email=email).first():
                return None, "Email Already Exists"
            
            if User.query.filter_by(username=username).first():
                return None, "Username already exists"
            
            #Creates A new user 
            new_uer = User(
                username=username, email=email , first_name=first_name , last_name=last_name ,phone=phone)
            
             # Hash password
            new_user.password_hash = PasswordUtil.hash_password(password)
            
            # Save to database
            db.session.add(new_user)
            db.session.commit()

            return new_user , "User Created Successfully"
        
        except Exception as e:
            db.session.rollback()
            return None, str(e)
        

        # Generating a token to Validate The User And Logging him/her successfully
    @staticmethod
    def authenticate_user(email, password):
       #Find User by email
        try:
            user = User.query.filter_by(email=email).first()
            if not user:
                return None, "User not found"
            # Verify password
            if not PasswordUtil.verify_password(password, user.password_hash):
                return None, "Invalid password"
             # Check if user is active
            if not user.is_active:
                return None, "User account is inactive"
            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()
             # Generate tokens
            access_token = JwtUtil.generate_access_token(
                user_id=user.id,
                email=user.email,
                username=user.username,
                role=user.role.value
            )
            response = {
                'user': user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            return response, "Login successful"
        except Exception as e:
            return None, str(e)
        
    @staticmethod
    def get_user_by_id(user_id):
        try:
            return User.query.get(user_id)
        except Exception as e:
            print(f"Error: {e}")
            return None
   
   
    @staticmethod
    def update_user(user_id, **kwargs):
        try:
            user = User.query.get(user_id)
            
            if not user:
                return None, "User not found"
            
            # Update allowed fields
            allowed_fields = ['first_name', 'last_name', 'phone']
            
            for key, value in kwargs.items():
                if key in allowed_fields:
                    setattr(user, key, value)
            
            db.session.commit()
            return user, "User updated successfully"
        
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def change_password(user_id, old_password, new_password):
       
        try:
            user = User.query.get(user_id)
            
            if not user:
                return None, "User not found"
            
            # Verify old password
            if not PasswordUtil.verify_password(old_password, user.password_hash):
                return None, "Old password is incorrect"
            
            # Set new password
            user.password_hash = PasswordUtil.hash_password(new_password)
            db.session.commit()
            
            return user, "Password changed successfully"
        
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    
    @staticmethod
    def delete_user(user_id):
       
        try:
            user = User.query.get(user_id)
            
            if not user:
                return None, "User not found"
            
            db.session.delete(user)
            db.session.commit()
            
            return True, "User deleted successfully"
        
        except Exception as e:
            db.session.rollback()
            return None, str(e)

