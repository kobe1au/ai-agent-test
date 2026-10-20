import requests

url = "http://127.0.0.1:8000/api/v1/rag/query"

headers = {
  'Content-Type': 'application/json',
  "x-api-key": "dev-api-key-123",
  "x-user-id": "u_10001",
  "x-username": "kobeliu",
  "x-workspace-id": "kobeliu"
}

payload = {
  "question": "什么是RAG?",
  "knowledge_base_id": "kb_error",
  "top_k":5,
  "rerank": True,
  "metadata_filter": {}
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
print(response.status_code)
print(response.headers)