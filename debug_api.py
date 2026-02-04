import requests
import json

try:
    print("Attempting to connect to http://127.0.0.1:8000/predict ...")
    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json={"description": "test text"},
        timeout=10
    )
    print(f"Status Code: {response.status_code}")
    if response.status_code != 200:
        print("Error Response Body:", response.text)
    else:
        print("Success Response:", response.json())
except Exception as e:
    print(f"Connection Failed: {e}")
