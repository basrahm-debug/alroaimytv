from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = "secret123"  # ضروري للرسائل المؤقتة flash

CHANNELS_JSON_PATH = "remote/channels.json"

def load_channels():
    if os.path.exists(CHANNELS_JSON_PATH):
        with open(CHANNELS_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"categories": []}

def save_channels(data):
    with open(CHANNELS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/", methods=["GET", "POST"])
def index():
    data = load_channels()

    if request.method == "POST":
        category_name = request.form.get("category")
        channel_name = request.form.get("channel_name")
        channel_url = request.form.get("channel_url")

        if not category_name or not channel_name or not channel_url:
            flash("جميع الحقول مطلوبة", "error")
            return redirect(url_for("index"))

        # البحث عن القسم أو إضافته إذا غير موجود
        category = next((c for c in data["categories"] if c["name"] == category_name), None)
        if not category:
            category = {"name": category_name, "channels": []}
            data["categories"].append(category)

        # إضافة القناة
        category["channels"].append({"name": channel_name, "url": channel_url})
        save_channels(data)
        flash(f"تمت إضافة القناة {channel_name} بنجاح", "success")
        return redirect(url_for("index"))

    return render_template("index.html", categories=data["categories"])

if __name__ == "__main__":
    app.run(debug=True)
