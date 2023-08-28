import yt_dlp as youtube_dl

from logger import logger


def get_youtube_video_info(url: str):
    options = {
        "quiet": False,  # Don't suppress console output
        "extract_flat": True,  # Extract info only (no download)
        "force_generic_extractor": True,  # Use generic extractor
        "skip_download": True,  # Skip downloading the video
        "format": "bestaudio/best",  # Choose the best audio quality
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(url, download=False)

    video_title = info_dict.get("title", "Title unknown")
    url = info_dict.get("url", "None")
    logger.info(f"Got video info for {video_title} ({url})")

    return {"title": video_title, "url": url}
