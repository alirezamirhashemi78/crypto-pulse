import os
import glob
import yt_dlp
from yt_dlp.utils import DownloadError
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUBS_DIR = os.path.join(BASE_DIR, "subs")
os.makedirs(SUBS_DIR, exist_ok=True)

delay = random.randint(1, 8)

ydl_opts = {
    "skip_download": True,
    "writesubtitles": True,
    "writeautomaticsub": True,
    "subtitleslangs": ["en"],
    "subtitlesformat": "vtt",
    "outtmpl": os.path.join(SUBS_DIR, "%(id)s.%(ext)s"),

    # کم کردن احتمال 429
    "headers": {
        "User-Agent": "PostmanRuntime/7.32.3",
        "Accept-Language": "en-US,en;q=0.9",
    },
    "extractor_args": {
        "youtube": {
            "player_client": ["android"]
        },
    },
    "retries": 3,
    "fragment_retries": 3,
    "sleep_interval_requests": delay,
}


def download_english_subtitles(url: str) -> str | None:
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
    except DownloadError as e:
        msg = str(e)
        if "HTTP Error 429" in msg:
            print("[WARN] Got 429 from YouTube (Too Many Requests).")
            return None
        else:
            print("[ERROR] yt-dlp error:", msg)
            return None

    video_id = info.get("id")
    pattern = os.path.join(SUBS_DIR, f"{video_id}*.vtt")
    matches = glob.glob(pattern)

    if not matches:
        print("[INFO] No English subtitles found.")
        return None

    return matches[0]
