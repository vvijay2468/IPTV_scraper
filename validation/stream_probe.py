# validation/stream_probe.py
import asyncio
import aiohttp

async def probe_stream(url, timeout=8):
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
            # Try a HEAD first
            async with session.head(url) as r:
                if r.status == 200:
                    return True, "HEAD OK"
            # Fallback to a short GET
            async with session.get(url) as r:
                chunk = await r.content.read(512)
                if chunk:
                    return True, "GET OK"
        return False, "No Data"
    except Exception as e:
        return False, str(e)

async def probe_many(urls):
    tasks = [probe_stream(u) for u in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return dict(zip(urls, results))
