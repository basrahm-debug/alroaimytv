import json
import os

# مسار ملف القنوات
CHANNELS_JSON = os.path.join(os.path.dirname(__file__), "../remote/channels.json")

def main():
    # مثال على القنوات الافتراضية، يمكن تعديلها لاحقًا
    data = {
        "categories": [
            {
                "name": "Quran",
                "channels": [
                    {"name": "القرآن الكريم", "url": "https://example.com/quran.m3u"}
                ]
            },
            {
                "name": "News",
                "channels": [
                    {"name": "Al Jazeera", "url": "https://example.com/aljazeera.m3u"}
                ]
            }
        ]
    }

    # كتابة البيانات إلى channels.json
    with open(CHANNELS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"تم تحديث القنوات بنجاح، عدد القنوات: {sum(len(c['channels']) for c in data['categories'])}")

if __name__ == "__main__":
    main()
