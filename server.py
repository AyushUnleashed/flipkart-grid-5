import logging
import uvicorn
from fastapi import FastAPI, APIRouter
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])

log = logging.getLogger("rich")
log.info("[red]APP started", extra={"markup": True})

desc = """

## components
 - outfit generator
"""

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="neytiri",
    description=desc,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from main import endpoint_router

app.include_router(endpoint_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8122)
