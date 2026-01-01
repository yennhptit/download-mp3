# server.py
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
import yt_dlp
import tempfile
import os

app = FastAPI()

@app.get("/download")
def download_audio(url: str = Query(..., description="YouTube URL")):
    tmpdir = tempfile.mkdtemp()
    output = os.path.join(tmpdir, "audio.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output,
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return FileResponse(os.path.join(tmpdir, "audio.mp3"), filename="audio.mp3")
    except Exception as e:
        return {"error": str(e)}
