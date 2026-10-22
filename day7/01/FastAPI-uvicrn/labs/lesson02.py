from fastapi import FastAPI

app = FastAPI(title="Lesson 02")

@app.get("/method")
def read_method():
    return {"method": "GET", "purpose": "read"}

# swagger에서 POST 요청을 테스트할 수 있도록 status_code=201을 설정
@app.post("/method", status_code=201)
def create_method():
    return {"method": "POST", "purpose": "create"}