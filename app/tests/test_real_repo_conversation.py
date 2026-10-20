import requests

url = "http://127.0.0.1:8000/api/v1/conversations"

headers = {
    'Content-Type': 'application/json',
    "x-api-key": "dev-api-key-123",
    "x-user-id": "u_10001",
    "x-username": "dawei"
}

payload = {
    "title": "测试会话"
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
print(response.status_code)
print(response.headers)