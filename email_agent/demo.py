import asyncio
async def demo():
    while(True):
        print("Hello")
        await asyncio.sleep(5)
asyncio.run(demo())