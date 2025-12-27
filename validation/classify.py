def classify_url(url: str) -> str:
    url = url.lower()

    if url.endswith(".m3u8"):
        return "STREAM_HLS"

    if url.endswith(".mpd"):
        return "STREAM_DASH"

    if any(url.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".svg", ".gif"]):
        return "STATIC_ASSET"

    return "UNKNOWN"
