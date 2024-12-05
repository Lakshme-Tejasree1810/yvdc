from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from yt_dlp import YoutubeDL

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)
import os
cur_dir = os.getcwd()

# Endpoint to fetch resolution options
@app.post("/get_resolutions")
def get_resolutions(link: str = Form(...)):
    ydl_opts = {"listformats": True}
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(link, download=False)
        formats = info_dict.get("formats", [])
        resolutions = [
            {"format_id": fmt["format_id"], "resolution": fmt.get("resolution", "audio-only")}
            for fmt in formats if fmt.get("format_id")
        ]
    return {"resolutions": resolutions}

# Endpoint to download a video in a specific resolution
@app.post("/download")
def download_video(link: str = Form(...), resolution: str = Form(...)):
    youtube_dl_options = {
        "format": resolution,
        "outtmpl": os.path.join(cur_dir, f"Video-{link[-11:]}.mp4"),
    }
    with YoutubeDL(youtube_dl_options) as ydl:
        ydl.download([link])
    return {"status": "Download started"}
