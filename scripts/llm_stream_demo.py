import asyncio
import httpx
import json

from app.core.config import settings

async def main():
    if not settings.deepseek_api_key:
        raise RuntimeError("请先在 .env 中配置 DEEPSEEK_API_KEY")

    url = f"{settings.deepseek_base_url}/chat/completions"

    headers = {
        "Authorization": f"Bearer {settings.deepseek_api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "user",
                "content": "请用一句话解释什么是 AI Agent。",
            },
        ],
        "temperature": 0.7,
        "stream": True,
    }

    full_answer = ""
    async with httpx.AsyncClient(timeout=60) as client:
        async with client.stream(
            "POST", url, headers=headers, json=payload
        ) as response:
            print("status_code:", response.status_code)

            async for line in response.aiter_lines():
                if not line: continue
                if not line.startswith("data:"): continue

                data = line.removeprefix("data:").strip()

                if data == "[DONE]":
                    break

                chunk = json.loads(data)

                delta = chunk["choices"][0].get("delta", {})
                content = delta.get("content", "")

                if content:  # 输出流式数据
                    full_answer += content
                    print(content, end="",flush=True)

    print("\nfull_answer:", full_answer)

if __name__ == "__main__":
    asyncio.run(main())