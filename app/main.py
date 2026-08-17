from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.inference import make_prediction
from app.schemas import ClientData


BASE_DIR = Path(__file__).resolve().parents[1]
FRONTEND_DIR = BASE_DIR / "frontend"
FRONTEND_PATH = FRONTEND_DIR / "index.html"

app = FastAPI(title="Bank Marketing API")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def show_frontend():
    return FileResponse(FRONTEND_PATH)


@app.post("/predict")
def predict(data: ClientData):
    return make_prediction(data.model_dump())
