from app import db
from app.models.user import User
from app.utils.otp_util import OtpUtil
from app.utils.email_util import EmailUtil
from app.utils.password_util import PasswordUtil
from datetime import datetime

class PasswordResetService:


    # Forgot Password
    @staticmethod
    def request_password_reset(email):
        try:
            #Step 1: Find User
            user = User.query.filter_by(email=email).first()
            if not user: # if user not Found
                return False
            
            #Generate OTP 
            otp = OtpUtil.generate_otp(length=6)

            #Set the OTP Expiry
            otp_expiry = OtpUtil.get_otp_expiry(minutes)

            #Save OTP to user
            user.otp = otp
            user.otp_expiry = otp_expiry
            db.session.commit()

            #Send OTP via Email
            email_sent = EmailUtil.send_otp_email( to_email=email,otp=otp,user_name=user.first_name)

            if not email_sent:
                return False # Failed To Send OTP
            
            return True # OTP Send to your Email
        
        except Exception as e:
            db.session.rollback()
            return False, str(e)
        
        #Step 1: Verify OTP 

        @staticmethod
        def verify_otp(email, otp):
            
            try: 
                #Step 1: Find The User
                user = User.query.filter_by(email=email).first()
                if not user:
                    return False, "User Not Found"
                #Step 2 : Check if the user has OTP 
                if not user.otp:
                    return False, "No OTP Found Request OTP first"
                
                #Step 3 : Verify OTP 
                is_valid = OtpUtil.is_otp_valid(
                    stored_otp=user.otp,
                    provided_otp=otp,
                    otp_expiry=user.otp_expiry
                )
                if not is_valid:
                    return False, "Otp is Incorrect or expired"
                #Step 4: OTP expired! Clear OTP
                user.otp = None
                user.otp_expiry = None
                db.session.commit()

                return True, "OTP verified successfully"
            except Exception as e:
                db.session.rollback()
                return False , str(e)
            #Step 2: Reset password After OTP Verification

        @staticmethod
        def reset_password(email , new_password):
            try:
                #Step 1: Find the User
                user = User.query.filter_by(email=email).first()
                if not user:
                    return False , "User Not Found"

                #Step 2: Hash new Password
                new_password_hash = PasswordUtil.hash_password(new_password)
                
                #Step 3: Update Password
                user.password_hash= new_password_hash
                db.session.commit()

                return True , "Password Reset Successfully"
            
            except Exception e:
                db.session.rollback()
                return False, str(e)
                
    #Step 3 : Forgot Password Flow
    def complete_password_reset(email , otp , new_password):
        try:
             #Find the User
             user = User.query.filter_by(email=email).first()
             if not user:
                 return False , "User not Found"
            #Verify The OTP
            is_valid = OtpUtil.is_otp_valid(
                stored_otp=user.otp,
                provided_otp=otp,
                otp_expiry=user.otp_expiry
            )
            if not is_valid:
                return False, "OTP is incorrect or expired"
            #Reset Password

            new_password_hash = PasswordUtil.hash_password(new_password)
            user.password_hash = new_password_hash
            user.otp = None
            user.otp_expiry = None
            
            db.session.commit()
            return True, "Password reset successfully"
        except Exception as e:
            db.session.rollback()
            return False ,  str(e)