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
        "content": "我的订单怎么还没发货？"
      }
    ],
    "model": "deepseek-chat",
    "temperature": 0.3,
    "stream": False,
    "prompt_scenario": "ecommerce_customer_service",
    "metadata": {
      "business_rules": "普通商品付款后 48 小时内发货；定制商品付款后 7 个工作日内发货；没有订单号不能查询具体物流。",
      "order_info": "用户未提供订单号。"
    }
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
print(response.status_code)
print(response.headers)