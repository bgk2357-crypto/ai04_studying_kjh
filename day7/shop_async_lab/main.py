"""쇼핑몰 조회로 배우는 동기·비동기. 실행: python -m uvicorn main:app --port 8001"""

import asyncio
import time
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

BASE = Path(__file__).resolve().parent
app = FastAPI(title="장바구니 실험실", description="외부 서비스의 I/O 대기를 재현하는 교육용 앱")
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")

SERVICES = (
    ("product", "상품 정보", 1.2, "데일리 캔버스 백 · 32,000원"),
    ("stock", "재고 확인", 1.8, "내추럴 색상 · 구매 가능 (12개)"),
    ("delivery", "배송 조회", 1.0, "서울 기준 · 내일 도착 예정 / 무료배송"),
)
Mode = Literal["sync", "blocking", "async", "thread"]


@app.get("/", include_in_schema=False)
async def index():
    return FileResponse(BASE / "static" / "index.html")


@app.get("/api/health")
async def health():
    """같은 이벤트 루프가 다른 요청에 응답할 수 있는지 확인한다."""
    return {"status": "ok"}


def finish(service, started, origin):
    key, label, _, value = service
    return {"key": key, "label": label, "value": value,
            "start": round(started - origin, 4),
            "end": round(time.perf_counter() - origin, 4)}


def legacy_lookup(service, scale, origin):
    """비동기를 지원하지 않는 기존 SDK/DB 호출의 대기 시간을 흉내낸다."""
    started = time.perf_counter()
    time.sleep(service[2] * scale)
    return finish(service, started, origin)


async def async_lookup(service, scale, origin):
    started = time.perf_counter()
    await asyncio.sleep(service[2] * scale)
    return finish(service, started, origin)


async def blocking_lookup(service, scale, origin):
    # 학습을 위한 잘못된 예: async def라도 time.sleep은 이벤트 루프를 막는다.
    return legacy_lookup(service, scale, origin)


def sequential_lookup(scale, origin):
    return [legacy_lookup(service, scale, origin) for service in SERVICES]


@app.get("/api/checkout/{mode}")
async def checkout(mode: Mode, scale: float = Query(1.0, ge=0.25, le=2.0)):
    origin = time.perf_counter()
    if mode == "sync":
        # 동기 함수 안에서는 순서대로 실행. FastAPI의 일반 def 경로처럼
        # 작업을 스레드에서 실행하므로 이벤트 루프는 다른 요청을 처리할 수 있다.
        results = await asyncio.to_thread(sequential_lookup, scale, origin)
    elif mode == "blocking":
        results = await asyncio.gather(*(
            blocking_lookup(service, scale, origin) for service in SERVICES
        ))
    elif mode == "async":
        results = await asyncio.gather(*(
            async_lookup(service, scale, origin) for service in SERVICES
        ))
    else:
        results = await asyncio.gather(*(
            asyncio.to_thread(legacy_lookup, service, scale, origin)
            for service in SERVICES
        ))
    return {"mode": mode, "elapsed": round(time.perf_counter() - origin, 4),
            "results": results}
