"""Integration test for password reset endpoints"""

def test_password_reset_flow(client):
    """Test complete password reset flow"""
    
    # First, register a user
    print("\n=== Step 1: Register User ===")
    register_response = client.post(
        "/api/auth/register",
        json={
            "username": "resetuser",
            "email": "resetuser@test.com",
            "password": "password123",
            "first_name": "Reset",
            "last_name": "User"
        }
    )
    print(f"Register Status: {register_response.status_code}")
    assert register_response.status_code == 201
    user_data = register_response.json()
    print(f"User created: {user_data['user']['email']}")
    
    # Step 2: Request password reset
    print("\n=== Step 2: Request Password Reset (Forgot Password) ===")
    forgot_response = client.post(
        "/api/auth/forgot-password",
        json={"email": "resetuser@test.com"}
    )
    print(f"Forgot Password Status: {forgot_response.status_code}")
    print(f"Response: {forgot_response.json()}")
    assert forgot_response.status_code == 200
    assert forgot_response.json()["success"] == True
    
    # Step 3: Get the OTP from the utility (in real scenario, user gets from email)
    print("\n=== Step 3: Extract OTP from utility ===")
    from app.utils import otp_util
    otp_store = otp_util.OTP_STORE
    assert otp_store, "OTP store is empty after forgot-password request"
    latest_user_id = next(reversed(otp_store))
    otp_code = otp_store[latest_user_id]["code"]
    print(f"OTP Code: {otp_code}")
    
    # Step 4: Verify OTP
    print("\n=== Step 4: Verify OTP ===")
    verify_response = client.post(
        "/api/auth/verify-otp",
        json={
            "email": "resetuser@test.com",
            "otp_code": otp_code
        }
    )
    print(f"Verify OTP Status: {verify_response.status_code}")
    verify_data = verify_response.json()
    print(f"Response: {verify_data}")
    assert verify_response.status_code == 200
    assert verify_data["success"] == True
    reset_token = verify_data["reset_token"]
    
    # Step 5: Reset password with token
    print("\n=== Step 5: Reset Password with JWT Token ===")
    reset_response = client.post(
        "/api/auth/reset-password",
        json={
            "reset_token": reset_token,
            "new_password": "newpassword456"
        }
    )
    print(f"Reset Password Status: {reset_response.status_code}")
    reset_data = reset_response.json()
    print(f"Response: {reset_data}")
    assert reset_response.status_code == 200
    assert reset_data["success"] == True
    
    # Step 6: Try to login with new password
    print("\n=== Step 6: Login with New Password ===")
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "resetuser@test.com",
            "password": "newpassword456"
        }
    )
    print(f"Login Status: {login_response.status_code}")
    assert login_response.status_code == 200
    login_data = login_response.json()
    print(f"Login successful! Token: {login_data['data']['access_token'][:20]}...")
    
    print("\n✅ Complete password reset flow works correctly!")

if __name__ == "__main__":
    test_password_reset_flow()
