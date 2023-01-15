import aiohttp
import asyncio
import re

async def visit(path, session):
    text = await (await session.get(path)).text()
    if "Index of" not in text:
        print(text)
        return

    await asyncio.gather(*[
        visit(path + "/" + match.group(1), session)
        for match in re.finditer(r"HREF=(\w+)/", text)
    ])

async def main():
    async with aiohttp.ClientSession() as session:
        await visit("https://depth.q.2023.ugractf.ru/lkv2x8ejmsuxumkb", session)

asyncio.run(main())
