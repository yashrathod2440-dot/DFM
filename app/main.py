from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.api.cad import router as cad_router


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
INDEX_FILE = STATIC_DIR / "index.html"


app = FastAPI(
    title="DFM Analysis Software",
    description="Design for Manufacturing Analysis Software",
    version="1.0.0"
)


# Serve static files
app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)


# Main website
@app.get("/", response_class=HTMLResponse)
async def home():
    html = INDEX_FILE.read_text(encoding="utf-8")
    return HTMLResponse(content=html)


# Health check
@app.get("/health")
def health():
    return {
        "status": "OK"
    }


# CAD / DFM API
app.include_router(cad_router)
