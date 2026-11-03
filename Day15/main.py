import os
from pathlib import Path
import psycopg

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv(Path(__file__).resolve().with_name('.env'), override=True)

DB_URL = os.getenv("SUPABASE_DB_URL")

app = FastAPI()


@app.get("/")
def home():
    return {"message": "FastAPI 시작"}


@app.get("/db-test")
def db_test():

    try:
        with psycopg.connect(
            DB_URL,
            connect_timeout=5,
            sslmode="require",
        ) as conn:

            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                row = cur.fetchone()

        return {
            "database": "connected",
            "result": row[0],
        }

    except psycopg.Error as e:

        return {
            "database": "error",
            "message": str(e),
        }


import os

from dotenv import load_dotenv
from fastapi import FastAPI
from redis import Redis, RedisError

load_dotenv(override=True)

REDIS_URL = os.getenv("REDIS_URL", "")

app = FastAPI()


@app.get("/")
def home():
    return {"message": "FastAPI 실행 성공"}


@app.get("/redis-test")
def redis_test():

    try:
        with Redis.from_url(
            REDIS_URL,
            socket_connect_timeout=3,
            socket_timeout=3,
        ) as client:

            result = client.ping()

            return {
                "redis": "up",
                "ping": result,
            }

    except (RedisError, ValueError) as e:

        return {
            "redis": "down",
            "message": str(e),
        }
import psycopg
DB_URL = os.getenv("SUPABASE_DB_URL", "")
@app.get("/db-test")
def db_test():

    try:
        with psycopg.connect(
            DB_URL,
            connect_timeout=5,
            sslmode="require",
        ) as conn:

            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                row = cur.fetchone()

        return {
            "supabase": "up",
            "result": row[0],
        }

    except psycopg.Error as e:

        return {
            "supabase": "down",
            "message": str(e),
        }

from fastapi.responses import JSONResponse

@app.get("/health")
def health():

    checks = {
        "supabase": "down",
        "redis": "down",
    }

    # Supabase PostgreSQL
    try:
        with psycopg.connect(
            DB_URL,
            connect_timeout=5,
            sslmode="require",
        ) as conn:

            with conn.cursor() as cur:
                cur.execute("SELECT 1")

                if cur.fetchone() == (1,):
                    checks["supabase"] = "up"

    except psycopg.Error:
        pass

    # Redis
    try:
        with Redis.from_url(
            REDIS_URL,
            socket_connect_timeout=3,
            socket_timeout=3,
        ) as client:

            if client.ping():
                checks["redis"] = "up"

    except (RedisError, ValueError):
        pass

    # 전체 상태 확인
    ready = all(
        value == "up"
        for value in checks.values()
    )

    return JSONResponse(
        status_code=200 if ready else 503,
        content={
            "ready": ready,
            "checks": checks,
        },
    )

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from redis import Redis, RedisError

load_dotenv(override=True)

REDIS_URL = os.getenv("REDIS_URL", "")

app = FastAPI()


@app.get("/")
def home():
    return {"message": "FastAPI 실행 성공"}


@app.get("/redis-test")
def redis_test():

    try:
        with Redis.from_url(
            REDIS_URL,
            socket_connect_timeout=3,
            socket_timeout=3,
        ) as client:

            result = client.ping()

            return {
                "redis": "up",
                "ping": result,
            }

    except (RedisError, ValueError) as e:

        return {
            "redis": "down",
            "message": str(e),
        }