import requests

intent_url = "http://127.0.0.1:8000/api/v1/structured/intent"
rag_url = "http://127.0.0.1:8000/api/v1/structured/rag-answer"
agent_url = "http://127.0.0.1:8000/api/v1/structured/agent-plan"

headers = {
    'Content-Type': 'application/json',
    "x-api-key": "dev-api-key-123",
    "x-user-id": "u_10001",
    "x-username": "dawei"
}

intent_payload = {
    "question": "我的订单怎么还没发货？",
    "model": "deepseek-chat"
}

rag_payload = {
    "question": "员工年假有几天？",
    "retrieved_context": "[doc_001] 员工入职满一年后，每年享有 5 天带薪年假。",
    "model": "deepseek-chat"
}

agent_payload = {
    "goal": "帮用户查询订单 10001 的物流状态，并给出客服回复。",
    "available_tools": "query_order(order_id: string)：根据订单号查询订单和物流状态。",
    "constraints": "不能编造物流信息；只能调用已提供的工具。",
    "model": "deepseek-chat"
}

# response = requests.post(intent_url, json=intent_payload, headers=headers)
# response = requests.post(rag_url, json=rag_payload, headers=headers)
response = requests.post(agent_url, json=agent_payload, headers=headers)
print(response.json())
print(response.status_code)
print(response.headers)