import requests

url = "http://127.0.0.1:8000/api/v1/chat"
headers = {
    "Content-Type": "application/json",
    "x-api-key": "dev-api-key-123",
    "x-user-id": "u_10001",
    "x-username": "dawei"
}

payload = {
     "messages": [
      {
        "role": "system",
        "content": "你是一个专业的 AI Agent 课程助教。"
      },
      {
        "role": "user",
        "content": "请用一句话解释什么是统一 LLM Provider 架构。"
      }
    ],
    "model": "deepseek-chat",
    "temperature": 0.7,
    "stream": False
}

response = requests.post(url, headers=headers, json=payload)
print("status_code:", response.status_code)
print("response:", response.json())