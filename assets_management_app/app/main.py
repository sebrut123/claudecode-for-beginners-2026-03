from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routers import assets

app = FastAPI(title="Asset Management API")

app.include_router(assets.router)

_frontend = Path(__file__).parent.parent / "frontend"
app.mount("/ui", StaticFiles(directory=_frontend, html=True), name="frontend")


@app.get("/", include_in_schema=False)
def root():
    return FileResponse(_frontend / "index.html")
