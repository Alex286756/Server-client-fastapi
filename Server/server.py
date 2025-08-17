from fastapi import FastAPI
import uvicorn

from Server.routers.record_router import router as record_router

app: FastAPI = FastAPI()
app.include_router(record_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
