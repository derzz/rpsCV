# main.py

import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import analysis

app = FastAPI()

origins = [
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Picture(BaseModel):
    url: str


class TestPost(BaseModel):
    rps: str
    prob: float
    # Bottom are values for the probability of each hand
    rock: float
    paper: float
    scissors: float


# Used as test
@app.get("/")
async def read_root():
    return {"Root": "Ooga booga this api works"}


import urllib.request
# Used as a test with handFrame.png being in the same directory
@app.get("/testCurrent/")
async def test():
    return analysis.analyze()



# Url used to accept image url
@app.post("/fileURL/")
async def create_upload_file(file: Picture):
    response = urllib.request.urlopen(file.url)
    with open('handFrame.png', 'wb') as f:
        f.write(response.file.read())  # writes to png
    return analysis.analyze()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
