from fastapi import FastAPI
import httpx
import os

app = FastAPI()
BASE_URL = 'http://127.0.01:9000'


@app.get('/health')
async def health():
    return {'ststus': 'ok'}

import asyncio
from time import perf_counter

async def fetch(client, item_id):
    response = await client.get(f'/items/{item_id}')
    response.rasie_for_status()
    return response.json()

@app.get('/summary') # 비동기 순차실행
async def summary():
    start = perf_counter()
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=3, trust_env=False) as client:
        items = []
        for item_id in [1, 2, 3]:
            items.append(await fetch(client, item_id))
    return {'items': items, 'elapsed': round(perf_counter() - start, 3)}

@app.get('/labels') # 비동기 병렬실행
async def labels():
    ids = [1, 2, 3]
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=3, trust_env=False) as client:
        tasks = [fetch(client, item_id) for item_id in ids]
        completed = []
        for task in asyncio.as_completed(tasks):
            completed.append(await task)
    return [{'requested_id': item_id, 'data': data}
            for item_id, data in zip(ids, completed)]

