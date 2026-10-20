# c_27ef25b8
import requests

url = "http://127.0.0.1:8000/api/v1/chat"

headers = {
    'Content-Type': 'application/json',
    "x-api-key": "dev-api-key-123",
    "x-user-id": "u_10001",
    "x-username": "dawei"
}

payload = {
    "messages": [
      {
        "role": "user",
        "content": "什么是 AI Agent？"
      }
    ],
    "model": "deepseek-chat",
    "temperature": 0.7,
    "stream": False,
    "session_id": "c_27ef25b8"
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
print(response.status_code)
print(response.headers)