import requests

url = "http://127.0.0.1:8000/api/v1/chat"

headers = {
    "Content-Type": "application/json",
    "x-api-key": "dev-api-key-123",
    "x-user-id": "u-10001",
    "x-username": "kobeliu"
}

payload = {
    "messages": [],
    "model": "deepseek-chat",
    "temperature": 3,
    "stream": False
}

response = requests.post(url=url,json=payload,headers=headers)

print(response.headers)
print(response.status_code)
print(response.text)