# trust/scoring.py
from difflib import SequenceMatcher

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def score_candidate(channel_norm, url, context):
    score = 0
    reasons = []

    ctx = context.lower()

    if channel_norm in ctx:
        score += 30
        reasons.append("exact_channel_match")

    sim = similarity(channel_norm, ctx)
    if sim > 0.6:
        score += 20
        reasons.append("high_similarity")
    elif sim > 0.4:
        score += 10
        reasons.append("medium_similarity")

    if url.endswith((".m3u", ".m3u8", ".ts")):
        score += 10
        reasons.append("stream_extension")

    if "github" in ctx:
        score += 5
        reasons.append("github_source")

    BLACKLIST_WORDS = {"adult", "xxx", "porn"}
    if any(w in ctx for w in BLACKLIST_WORDS):
        score -= 50
        reasons.append("blacklisted_context")

    return score, reasons

from datetime import datetime, timezone
import math

def compute_trust_time_decay(rows, half_life_hours=24):
    """
    rows = [(success, checked_at), ...]
    """
    now = datetime.now(timezone.utc)
    score = 0.0
    weight_sum = 0.0

    for success, ts in rows:
        ts = datetime.fromisoformat(ts).replace(tzinfo=timezone.utc)
        age_hours = (now - ts).total_seconds() / 3600.0

        weight = math.exp(-math.log(2) * age_hours / half_life_hours)
        score += weight * (1 if success else -1)
        weight_sum += weight

    if weight_sum == 0:
        return 0.0

    return max(0.0, score / weight_sum)



