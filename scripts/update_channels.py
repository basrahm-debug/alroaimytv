import json
import requests
from pathlib import Path
import subprocess

# مسارات الملفات
BASE_DIR = Path(__file__).resolve().parent.parent
SOURCES_FILE = BASE_DIR / "local" / "sources.json"
CHANNELS_JSON = BASE_DIR / "remote" / "channels.json"

def parse_m3u(url):
    """تحميل M3U وفصل القنوات"""
    channels = []
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        lines = r.text.splitlines()
        name = ""
        for line in lines:
            line = line.strip()
            if line.startswith("#EXTINF:"):
                parts = line.split(",", 1)
                if len(parts) > 1:
                    name = parts[1].strip()
            elif line and not line.startswith("#"):
                channels.append({
                    "name": name if name else "Unknown",
                    "url": line,
                    "enabled": True
                })
                name = ""
    except Exception as e:
        print(f"فشل تحميل M3U من {url}: {e}")
    return channels

def get_youtube_live(url):
    """استخراج رابط البث المباشر أو آخر فيديو باستخدام yt-dlp"""
    try:
        result = subprocess.run(
            ["yt-dlp", "-g", "-f", "best", url],
            capture_output=True,
            text=True,
            check=True
        )
        link = result.stdout.strip().splitlines()[0]
        return link
    except Exception as e:
        print(f"فشل الحصول على رابط YouTube من {url}: {e}")
        return None

def main():
    if SOURCES_FILE.exists():
        with open(SOURCES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"sources": []}

    all_categories = []

    for src in data.get("sources", []):
        category_name = src.get("category", "عام")
        src_type = src.get("type")
        channels_list = []

        if src_type == "m3u" and src.get("url"):
            channels_list = parse_m3u(src["url"])

        elif src_type == "direct" and src.get("url"):
            channels_list = [{
                "name": src.get("name", "Unknown"),
                "url": src.get("url"),
                "enabled": src.get("enabled", True)
            }]

        elif src_type == "youtube" and src.get("url"):
            live_url = get_youtube_live(src["url"])
            if live_url:
                channels_list = [{
                    "name": src.get("name", "YouTube Live"),
                    "url": live_url,
                    "enabled": src.get("enabled", True)
                }]

        if channels_list:
            all_categories.append({
                "name": category_name,
                "channels": channels_list
            })

    # دمج القنوات حسب القسم لتجنب تكرار الأقسام
    merged = {}
    for cat in all_categories:
        name = cat["name"]
        if name not in merged:
            merged[name] = []
        merged[name].extend(cat["channels"])

    final_data = [{"name": k, "channels": v} for k, v in merged.items()]
    CHANNELS_JSON.parent.mkdir(exist_ok=True, parents=True)
    with open(CHANNELS_JSON, "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

    total_channels = sum(len(c["channels"]) for c in final_data)
    print(f"تم تحديث {total_channels} قناة في المجموع.")

if __name__ == "__main__":
    main()
