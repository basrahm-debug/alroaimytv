import json
import requests
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCES_FILE = BASE_DIR / "local" / "sources.json"
OUTPUT_FILE = BASE_DIR / "remote" / "channels.json"

IPTV_ORG_CHANNELS = "https://iptv-org.github.io/iptv/channels.json"
IPTV_ORG_STREAMS = "https://iptv-org.github.io/iptv/streams.json"


def load_sources():
    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)["sources"]


def fetch_iptv_org():
    channels = requests.get(IPTV_ORG_CHANNELS, timeout=20).json()
    streams = requests.get(IPTV_ORG_STREAMS, timeout=20).json()

    stream_map = {}
    for s in streams:
        channel_id = s.get("channel")
        if channel_id:
            stream_map.setdefault(channel_id, []).append(s.get("url"))

    results = []
    for c in channels:
        cid = c.get("id")
        urls = stream_map.get(cid)
        if not urls:
            continue

        results.append({
            "name": c.get("name"),
            "logo": c.get("logo"),
            "country": c.get("country"),
            "category": "iptv-org",
            "url": urls[0]
        })

    return results


def fetch_manual_m3u(url, category):
    # حالياً placeholder
    return [{
        "name": "Manual Channel",
        "url": url,
        "category": category,
        "logo": None
    }]


def main():
    sources = load_sources()
    categories = {}

    for source in sources:
        if not source.get("enabled"):
            continue

        if source["type"] == "iptv-org":
            channels = fetch_iptv_org()
        elif source["type"] == "m3u":
            channels = fetch_manual_m3u(
                source["url"],
                source["category"]
            )
        else:
            continue

        for ch in channels:
            cat = ch["category"]
            categories.setdefault(cat, []).append(ch)

    output = {
        "updated_at": datetime.utcnow().isoformat(),
        "categories": [
            {
                "id": k,
                "channels": v
            } for k, v in categories.items()
        ]
    }

    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("تم تحديث channels.json بنجاح")


if __name__ == "__main__":
    main()
