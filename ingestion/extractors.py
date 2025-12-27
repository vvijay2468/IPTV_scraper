# ingestion/extractors.py
import re

URL_RE = re.compile(r'(https?://[^\s\'"]+)')

def extract_with_context(text, window=120):
    results = []
    for m in URL_RE.finditer(text):
        start = max(0, m.start() - window)
        end = min(len(text), m.end() + window)
        ctx = text[start:end]
        results.append((m.group(1), ctx))
    return results
