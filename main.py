import os
import json
import urllib.request
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

class ObjectData(BaseModel):
    scale: dict
    position: dict
    rotation: dict

class AvatarInfo(BaseModel):
    resourceId: str
    objectData: ObjectData

class SceneInfo(BaseModel):
    resourceId: str
    objectData: ObjectData

class CareRecipientRequest(BaseModel):
    avatar_id: str
    scene_id: str
    storage_links: List[str]

class SaveRequest(BaseModel):
    title: str
    sceneInfo: SceneInfo
    avatarsInfo: List[AvatarInfo]

@app.get("/")
def healthcheck():
    return JSONResponse(content={"status": "healthy"}, status_code=200)



@app.post("/care-recipient")
async def receive_care_recipient_data(request: CareRecipientRequest):
    data_folder = "./data"
    os.makedirs(data_folder, exist_ok=True)
    for link in request.storage_links:
        file_name = os.path.basename(link)
        file_path = os.path.join(data_folder, file_name)
        try:
            urllib.request.urlretrieve(link, file_path)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to download file: {e}")
    return {"message": "Data saved successfully"}


@app.post("/save")
async def save_to_flutter(request: SaveRequest):
    # 플러터로 데이터 전송
    flutter_url = "flutter-api-endpoint"
    headers = {'Content-Type': 'application/json'}
    data = json.dumps(request.dict()).encode('utf-8')
    req = urllib.request.Request(flutter_url, data=data, headers=headers, method='POST')
    try:
        response = urllib.request.urlopen(req)
        response_data = response.read().decode('utf-8')
        return json.loads(response_data)
    except urllib.error.HTTPError as e:
        raise HTTPException(status_code=e.code, detail=f"Failed to send data to Flutter: {e.reason}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# Static Files Serving
from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory="."), name="static")
