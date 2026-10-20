import requests 


url = "http://127.0.0.1:8000/api/v1/health"

response = requests.get(url)
print(response.status_code)
print(response.text)
print(response.headers)
