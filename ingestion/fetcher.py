# ingestion/fetcher.py
import aiohttp
import asyncio
import ssl

TIMEOUT = aiohttp.ClientTimeout(total=10)
MAX_BYTES = 1_000_000  # 1MB
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

async def fetch(url):
    timeout = aiohttp.ClientTimeout(total=15)
    async with aiohttp.ClientSession(timeout=timeout) as s:
        async with s.get(url, ssl=ssl_ctx) as r:
            return await r.text(errors="ignore")

async def fetch_many(urls):
    return await asyncio.gather(*(fetch(u) for u in urls))
