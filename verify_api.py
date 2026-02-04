import requests
import json

try:
    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json={"description": "I feel deep darkness and sorrow."}
    )
    print("Status Code:", response.status_code)
    print("Response:", json.dumps(response.json(), indent=2))
except Exception as e:
    print("Verification Failed:", e)
