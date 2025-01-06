# main.py

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class TestPost(BaseModel):
    name: str


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/test")
async def test():
    return {"content": "This is a test"}


@app.post("/gib")
async def gib(item: TestPost):
    return "Gib " + item.name

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
