# normalization/channel.py
import re

JUNK = {"hd", "live", "tv", "channel"}

def normalize_channel(name: str) -> str:
    s = re.sub(r'[^a-zA-Z0-9\s]', ' ', name.lower())
    tokens = [t for t in s.split() if t not in JUNK]
    return ' '.join(tokens)
