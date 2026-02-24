# User forgets password
#   → System generates OTP: 123456
#   → Sends OTP to user's email
#   → User enters OTP
#   → System verifies: Is 123456 correct? 
 #   → If correct, user can reset password

import  random
from datetime import datetime , timedelta

class OtpUtil:
    #Utility Class for OTP operations
    @staticmethod
    def generate_otp(length=6):
        #Generate a random 6 digit otp
        otp = ' '.join([str(random.randint(0,9)) for _ in range(length)])
        return otp
    
    @staticmethod
    def is_otp_valid(stored_otp , provided_otp , otp_expiry):
        #if OTP Matches
        if stored_otp != provided_otp:
            print("OTP is Incorrect")
            return False
        
        #if OTP is expired
        if dattetime.utcnow() > otp_expiry:
            print("OTP has expired")
            return False
       
        #OTP is Valide

        print("OTP is correct and expired")
        return True
    @staticmethod
    def get_otp_expiry(minutes=10): # get OTP expiry time
        expiry = datetime.utcnow() + timedelta(minutes= minutes)
        return expiry
    @staticmethod # Is the Otp Expiry
    def is_otp_expired(otp_expiry):
        return datetime.utcnow() > otp_expiry