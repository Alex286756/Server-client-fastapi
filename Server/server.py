from fastapi import FastAPI
import uvicorn

app: FastAPI = FastAPI()


@app.post("/create")
async def create():
    return "TODO create"


@app.get('/list')
async def list_all():
    return "TODO list_all"


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
