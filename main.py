import asyncio
from normalization.channel import normalize_channel
from ingestion.fetcher import fetch_many
from ingestion.extractors import extract_with_context
from trust.scoring import score_candidate
from trust.scoring import compute_trust_time_decay
from validation.classify import classify_url
from trust.trust_query import fetch_validation_rows
from validation.stream_probe import probe_many
from player.launcher import play_url


def load_seeds(path="seeds.txt"):
    seeds = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                if (line.startswith('"') and line.endswith('"')) or \
                   (line.startswith("'") and line.endswith("'")):
                    line = line[1:-1].strip()

                if not line or " " in line:
                    continue

                seeds.append(line)
    except FileNotFoundError:
        print(f"[!] seeds.txt not found at {path}")

    return seeds


SEEDS = load_seeds()

async def run(channel: str):
    print(f"\n[+] Channel input: {channel}")
    ch_norm = normalize_channel(channel)
    print(f"[+] Normalized channel: {ch_norm}")

    # ---- Fetch documents ----
    docs = await fetch_many(SEEDS)
    print(f"[+] Fetched {len(docs)} documents")

    # ---- Extract + score ----
    candidates = {}
    total_urls = 0

    for doc in filter(None, docs):
        extracted = extract_with_context(doc)
        total_urls += len(extracted)

        for url, ctx in extracted:
            score, reasons = score_candidate(ch_norm, url, ctx)

            if score >= 20:
                if url not in candidates or score > candidates[url]["score"]:
                    candidates[url] = {
                        "score": score,
                        "reasons": reasons
                    }

    print(f"[+] Extracted {total_urls} raw URLs")
    print(f"[+] {len(candidates)} URLs survived heuristic filtering")

    # ---- Rank ----
    ranked = sorted(
        candidates.items(),
        key=lambda x: x[1]["score"],
        reverse=True
    )

    top = ranked[:20]
    top_urls = [url for url, _ in top]
    if not top_urls:
        print("[!] No viable stream candidates found for this channel.")
        return


    print(f"[+] Top {len(top_urls)} candidates:")
    for url, meta in top:
        print(f"  SCORE {meta['score']:>2} | {url}")
        print(f"    reasons: {meta['reasons']}")

    # ---- Validate ----
    print(f"\n[+] Validating {len(top_urls)} candidates...")
    results = await probe_many(top_urls)
    playable = []
    index_map = []

    for idx, url in enumerate(top_urls, start=1):
        ok, info = results[url]
        stype = classify_url(url)

        status = "✔" if ok else "✘"
        print(f"[{idx}] {status} {url} — {info} [{stype}]")

        if ok and stype.startswith("STREAM"):
            playable.append(url)
            index_map.append(idx)

    if not playable:
        print("\n[!] No playable streams found.")
        return


    while(1):
        choice = input("\nSelect stream number to play (or Enter to skip): ").strip()
        if choice.isdigit():
            num = int(choice)
            if num in index_map:
                play_idx = index_map.index(num)
                url = playable[play_idx]
                ok, msg = play_url(url)
                print(f"[+] {msg}" if ok else f"[!] {msg}")
            else:
                print("[!] Selected stream is not playable.")
        else:
            break



if __name__ == "__main__":
    asyncio.run(run("star life"))
