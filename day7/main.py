import asyncio
import time
from fastapi import FastAPI
app = FastAPI()

def legay_lookup():
    '''기존 동기 라이브러리의 느린 조회를 흉내내는 함수 '''
    time.sleep(10)
    return {'name':'학습자'}

@app.get("/health")
async def health():
    return {'status': 'ok'}

@app.get('/bad')
async def bad():
    # 의도된 버그 : 비동기 함수에서 동기함수를 직접 호출
    user = legay_lookup()
    return {'route':'bad', 'user':user}

@app.get('/good')
async def good():
    # 실제 api호출을 흉내..응답을 기다리는 시간을 흉내
    await asyncio.sleep(2)
    return{'route':'good', 'user':{'name':'학습지'}}