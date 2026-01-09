import json
import os
import requests
import subprocess
import re

# مسارات الملفات
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES_JSON = os.path.join(BASE_DIR, "local", "sources.json")
CHANNELS_JSON = os.path.join(BASE_DIR, "remote", "channels.json")

def get_youtube_stream_url(youtube_url):
    """استخراج رابط البث المباشر من يوتيوب باستخدام yt-dlp"""
    print(f"استخراج رابط يوتيوب: {youtube_url}")
    try:
        # -g للحصول على الرابط المباشر، --get-url
        result = subprocess.run(
            ['yt-dlp', '-g', '-f', 'best', youtube_url],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"خطأ في استخراج رابط يوتيوب: {e}")
        return None

def parse_m3u(url, default_category):
    """تحميل وتحليل ملف M3U"""
    channels = []
    print(f"تحميل قائمة M3U: {url}")
    try:
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            return []
        
        lines = response.text.splitlines()
        current_name = None
        current_category = default_category

        for line in lines:
            line = line.strip()
            if line.startswith('#EXTINF:'):
                # محاولة استخراج الاسم
                name_match = re.search(r',([^,]+)$', line)
                if name_match:
                    current_name = name_match.group(1).strip()
                
                # استخراج القسم إذا وجد group-title
                cat_match = re.search(r'group-title="([^"]+)"', line)
                if cat_match:
                    current_category = cat_match.group(1)
            elif line.startswith('http'):
                if current_name:
                    channels.append({
                        "name": current_name,
                        "url": line,
                        "category": current_category
                    })
                current_name = None
                current_category = default_category
    except Exception as e:
        print(f"خطأ في تحليل M3U: {e}")
    
    return channels

def main():
    if not os.path.exists(SOURCES_JSON):
        print("ملف المصادر غير موجود!")
        return

    with open(SOURCES_JSON, "r", encoding="utf-8") as f:
        sources_data = json.load(f)
        sources = sources_data.get("sources", [])

    all_channels_by_cat = {}

    for src in sources:
        if not src.get("enabled", True):
            continue

        src_type = src.get("type", "direct")
        src_url = src.get("url")
        src_name = src.get("name")
        src_cat = src.get("category", "General")

        channels_to_add = []

        if src_type == "m3u":
            channels_to_add = parse_m3u(src_url, src_cat)
        elif src_type == "youtube":
            stream_url = get_youtube_stream_url(src_url)
            if stream_url:
                channels_to_add = [{"name": src_name, "url": stream_url, "category": src_cat}]
        elif src_type == "direct":
            channels_to_add = [{"name": src_name, "url": src_url, "category": src_cat}]

        for ch in channels_to_add:
            cat = ch['category']
            if cat not in all_channels_by_cat:
                all_channels_by_cat[cat] = []
            all_channels_by_cat[cat].append({"name": ch['name'], "url": ch['url']})

    # تحويل البيانات للشكل النهائي
    final_data = {"categories": []}
    for cat_name, channels in all_channels_by_cat.items():
        final_data["categories"].append({
            "name": cat_name,
            "channels": channels
        })

    # حفظ النتائج
    os.makedirs(os.path.dirname(CHANNELS_JSON), exist_ok=True)
    with open(CHANNELS_JSON, "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)

    totalcount = sum(len(c['channels']) for c in final_data['categories'])
    print(f"تم التحديث! عدد الأقسام: {len(final_data['categories'])}, إجمالي القنوات: {totalcount}")

if __name__ == "__main__":
    main()
