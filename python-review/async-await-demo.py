import asyncio


async def hello_world():
    print("Hello World")
    await asyncio.sleep(1)
    print("Goodbye World")
    return "Hello World"


res = asyncio.run(hello_world())


async def query_api():
    await asyncio.sleep(1)
    return "API Response"

async def query_order_api():
    await asyncio.sleep(1)
    return "Order API Response"

async def main():
    results = await asyncio.gather(
        query_api(), 
        query_order_api()
    )
    return results