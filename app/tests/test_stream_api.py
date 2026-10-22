import requests
import httpx
import asyncio

url = "http://127.0.0.1:8000/api/v1/chat/stream"
headers = {
    "Content-Type": "application/json",
    "x-api-key": "dev-api-key-123",
    "x-user-id": "u_10001",
    "x-username": "dawei"
}

payload = {
     "messages": [
      {
        "role": "user",
        "content": "请用三句话解释什么是 Streaming 流式输出。"
      }
    ],
    "model": "deepseek-chat",
    "temperature": 0.7,
    "stream": True
}

# requests 同步版
def requests_demo():
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        stream=True,
    )

    print("status_code:", response.status_code)
    print("content-type:", response.headers.get("content-type"))

    for line in response.iter_lines(decode_unicode=True):
        if line:
            print("chunk:", line)

# ==========================================================================
# httpx 异步版
async def httpx_demo():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers=headers,
            json=payload,
            stream=True,
        )

        print("status_code:", response.status_code)
        print("content-type:", response.headers.get("content-type"))

        async for line in response.aiter_lines():
                if line:
                    print(line)

if __name__ == "__main__":
    asyncio.run(httpx_demo())
    # requests_demo()
