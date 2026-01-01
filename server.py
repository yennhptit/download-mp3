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
    output = os.path.join(tmpdir, "audio.%(ext)s")  # giữ nguyên định dạng gốc

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output,
        "quiet": True,
        # Không cần postprocessor → giữ nguyên file webm
        # "postprocessors": [{
        #     "key": "FFmpegExtractAudio",
        #     "preferredcodec": "mp3",
        # }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # Lấy đường dẫn file tải về
            audio_file = ydl.prepare_filename(info)
        return FileResponse(audio_file, filename=os.path.basename(audio_file))
    except Exception as e:
        return {"error": str(e)}
