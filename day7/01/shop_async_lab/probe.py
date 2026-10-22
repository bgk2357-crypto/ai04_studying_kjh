"""실제 HTTP로 시간표·서버 응답성·동시 요청을 검증한다. 먼저 서버를 실행하세요."""

import argparse
import asyncio
from time import perf_counter

import httpx


async def measure(client, mode):
    task = asyncio.create_task(client.get(f"/api/checkout/{mode}", params={"scale": 0.5}))
    await asyncio.sleep(0.15)
    start = perf_counter()
    response = await client.get("/api/health")
    response.raise_for_status()
    health_elapsed = perf_counter() - start
    response = await task
    response.raise_for_status()
    data = response.json()
    print(f"{mode:9s} | 조회 {data['elapsed']:.2f}초 | 작업 중 health {health_elapsed * 1000:.0f}ms")
    rows = data["results"]
    assert [row["key"] for row in rows] == ["product", "stock", "delivery"]
    if mode in ("sync", "blocking"):
        assert all(rows[i + 1]["start"] >= rows[i]["end"] - 0.005 for i in range(2)), "순차 실행 실패"
    else:
        assert max(row["start"] for row in rows) < min(row["end"] for row in rows), "작업이 겹치지 않음"
    return data, health_elapsed


async def main(base_url):
    async with httpx.AsyncClient(base_url=base_url, timeout=30, trust_env=False) as client:
        response = await client.get("/")
        assert response.status_code == 200 and 'lang="ko"' in response.text
        for path in ("/static/app.js", "/static/style.css", "/docs"):
            response = await client.get(path)
            response.raise_for_status()
        for path in ("/api/checkout/unknown", "/api/checkout/async?scale=0", "/api/checkout/async?scale=3"):
            response = await client.get(path)
            assert response.status_code == 422, f"입력 검증 실패: {path}"
        measured = {}
        for mode in ("sync", "blocking", "async", "thread"):
            measured[mode] = await measure(client, mode)
        assert measured["blocking"][1] > measured["async"][1] + 0.5, "차단 상황이 재현되지 않음: 단일 worker인지 확인하세요."
        assert measured["sync"][0]["elapsed"] > measured["async"][0]["elapsed"] + 0.5

        print("\n고객 3명의 요청을 asyncio.gather로 동시에 전송 (대기 시간 0.25배)")
        for mode in ("blocking", "async"):
            start = perf_counter()
            responses = await asyncio.gather(*(
                client.get(f"/api/checkout/{mode}", params={"scale": 0.25}) for _ in range(3)
            ))
            for response in responses:
                response.raise_for_status()
            print(f"{mode:9s} | 3명 모두 완료: {perf_counter() - start:.2f}초")
        print("\n검증 통과: 정적 화면 / 입력 검증 / 순차·동시 시간표 / 서버 응답성")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8001")
    args = parser.parse_args()
    asyncio.run(main(args.url))
