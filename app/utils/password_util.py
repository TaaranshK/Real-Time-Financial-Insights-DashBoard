"""


What this file does:
- Hashes passwords before saving (never store plain passwords!)
- Verifies passwords when user logs in

Note: In production, use bcrypt instead of SHA256
"""

import hashlib


#HASH PASSWORD
def hash_password(password: str) -> str:
 
    
    # Convert password to bytes, then hash it
    return hashlib.sha256(password.encode()).hexdigest()


# VERIFY PASSWORD 
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks if a password matches the stored hash.
    
    Input: "password123", "ef92b778bafe..."
    Output: True or False
    """
    
    # Hash the plain password and compare
    return hash_password(plain_password) == hashed_password
