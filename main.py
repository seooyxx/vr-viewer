import os
import json
import urllib.request
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from starlette.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

logger = logging.getLogger("uvicorn.error")
logging.basicConfig(level=logging.INFO)


@app.get("/")
def healthcheck():
    logger.info("Health check called")
    return JSONResponse(content={"status": "healthy"}, status_code=200)
