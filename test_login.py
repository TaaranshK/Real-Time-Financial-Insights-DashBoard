import urllib.request
import json

try:
    data = json.dumps({'email': 'taaransh.kapoor@gmail.com', 'password': 'password123'}).encode('utf-8')
    req = urllib.request.Request(
        'http://127.0.0.1:8000/auth/login', 
        data=data, 
        headers={'Content-Type': 'application/json'}
    )
    response = urllib.request.urlopen(req, timeout=10)
    print("SUCCESS!")
    print(response.read().decode())
except urllib.error.HTTPError as e:
    print(f"HTTP ERROR {e.code}: {e.read().decode()}")
except Exception as e:
    print(f"ERROR: {e}")
