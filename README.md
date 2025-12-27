# IPTV Stream Discovery & Validation Engine (Python)

A Python-based IPTV discovery system that automatically crawls public IPTV sources, extracts candidate stream URLs, scores them against a user-provided channel name, validates stream availability, and allows direct playback via a local media player.

> This project is **not** an IPTV provider and does **not** host streams.  
> It is a **search, filtering, and validation engine** for publicly accessible IPTV streams.

---

## Why This Project Exists

Finding working IPTV streams manually is painful:

- IPTV playlists are massive and noisy  
- Many links are dead, geo-blocked, or mislabeled  
- Channel names vary wildly across sources  
- Popular channels are mixed with irrelevant content  
- Clicking random links in browsers is slow and unsafe  

This project solves **one specific problem**:

> **Given a channel name, find the most likely working public IPTV streams and verify them automatically.**

No scraping dashboards.  
No illegal redistribution.  
No pretending to be a “TV app”.

**Just engineering.**

---

## What This Project Does (End-to-End)

- Takes a channel name as input (e.g. `Fox News`)
- Fetches hundreds of public IPTV sources
- Extracts tens of thousands of URLs
- Scores each URL against the channel name
- Filters likely matches
- Actively validates each candidate stream
- Shows ✔ / ✘ status for each link
- Lets the user play a selected stream in VLC

---

## What This Project Does NOT Do

- ❌ Host IPTV streams  
- ❌ Guarantee legality of third-party links  
- ❌ Bypass DRM or authentication  
- ❌ Replace IPTV services (NGINX, Xtream, etc.)  
- ❌ Provide a polished UI (CLI by design)

---

## Architecture Overview

User Input (Channel Name)
↓
Seed URL Loader
↓
Async Fetcher (aiohttp)
↓
Extractor (URLs + Context)
↓
Scoring Engine
↓
Candidate Ranking
↓
Stream Validation
↓
Interactive Selection
↓
Local Playback (VLC)

yaml
Copy code

---

## Project Structure

Project_2/
├── main.py
├── seeds.txt
│
├── ingestion/
│ ├── fetcher.py # Async HTTP fetcher
│ └── extractors.py # URL + context extraction
│
├── normalization/
│ └── channel.py # Channel name normalization
│
├── trust/
│ └── scoring.py # Heuristic scoring logic
│
├── validation/
│ ├── stream_probe.py # HEAD/GET stream validation
│ └── classify.py # Stream type classification
│
├── player/
│ └── launcher.py # VLC launcher
│
└── README.md



---

## Seed Sources (`seeds.txt`)

`seeds.txt` contains public IPTV indexes, playlists, and aggregator sites.

### Rules

- One URL per line  
- Quotes optional  
- Blank lines ignored  

### Example

```txt
https://iptv-org.github.io/iptv/index.m3u
https://raw.githubusercontent.com/iptv-org/iptv/master/streams/us.m3u
https://epg.pw/test_channels.m3u
You can add hundreds or thousands of sources.

Scoring Logic (How URLs Are Ranked)
Each extracted URL is scored using simple but effective heuristics:

Signal	Score
Exact channel name in context	+30
High text similarity	+20
Medium similarity	+10
Stream file extension (.m3u8, .ts)	+10
GitHub source	+5
Blacklisted keywords	−50

Only URLs with score ≥ 20 survive.

This is intentional — aggressive filtering beats noise.

Validation Logic
Each candidate URL is actively probed:

HEAD request preferred

GET fallback if needed

Timeout & SSL failures handled

Result is classified as:

STREAM_HLS

STATIC_ASSET

UNKNOWN

Output Example


✔ 1 - https://fox-foxnewsnow.amagi.tv/playlist.m3u8 - HEAD OK [STREAM_HLS]
✘ 2 - http://example.com/broken.m3u8 - No Data [STREAM_HLS]
Playback (VLC Integration)
Validated streams can be played directly.

Requirements
VLC Media Player installed

VLC path either:

Added to system PATH, or

Hardcoded in player/launcher.py

Playback Flow

Select stream number to play (or Enter to skip): 1
→ VLC launches with the stream URL
Running the Project
1. Install dependencies
bash
Copy code
pip install aiohttp
2. Ensure VLC is installed
Recommended path (Windows):


C:\Program Files\VideoLAN\VLC\vlc.exe
3. (Optional) Add VLC to PATH
Or hardcode the path in player/launcher.py.

4. Run

python main.py
5. Enter channel name

asyncio.run(run("Fox News"))
```
Common Issues & Realities

❗ SSL certificate errors
Some IPTV sites use weak or broken certificates.
This is normal in the IPTV ecosystem.

❗ Regional bias
Many public IPTV sources skew:

1) Arabic

2) European

3) LATAM




"# IPTV_scraper" 
