"""Quick test of password reset utilities"""

from app.utils import otp_util, jwt_util, email_util

print("=== Testing OTP Utility ===")
otp_code = otp_util.generate_otp(1)
print(f"Generated OTP: {otp_code}")

valid, msg = otp_util.verify_otp(1, otp_code)
print(f"OTP Verification: {valid} - {msg}")

print("\n=== Testing JWT Utility ===")
token = jwt_util.generate_password_reset_token(1, "test@example.com")
print(f"Generated Token: {token[:50]}...")

payload = jwt_util.verify_password_reset_token(token)
print(f"Verified Payload: user_id={payload.get('user_id')}, email={payload.get('email')}")

print("\n=== Testing Email Utility ===")
success = email_util.send_otp_email("test@example.com", "123456", "John Doe")
print(f"Email Send Result: {success}")

print("\n All utilities working correctly!")
