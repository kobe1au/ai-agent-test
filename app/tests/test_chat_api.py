# 测试用例
import requests

# url = "http://127.0.0.1:8000/api/v1/chat"

# payload = {
#     "message": "What is the meaning of life?",
#     "model": "gpt-3.5-turbo",
#     "streaming": False,
# }

# response = requests.post(url, json=payload)

# print(response.json())
# print(response.status_code)


url = "http://127.0.0.1:8000/api/v1/agents/run?debug=true"

payload = {
    "question": "帮我查询订单状态",
    "agent_id": "agent_order"
}

headers = {
    "Content-Type": "application/json",
    "x-api-key": "dev-api-key-123",
    "x-user-id": "test-user-id",
    "x-username": "kobeliu",
}
response = requests.post(url, json=payload,headers=headers)

print(response.json())
print(response.status_code)

