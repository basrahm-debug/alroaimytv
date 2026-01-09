from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
import subprocess

app = Flask(__name__)
app.secret_key = "alroaimy_secret_key"

# مسارات الملفات (مسارات مطلقة لضمان العمل الصحيح)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES_JSON_PATH = os.path.join(BASE_DIR, "local", "sources.json")
UPDATE_SCRIPT_PATH = os.path.join(BASE_DIR, "scripts", "update_channels.py")

def load_sources():
    if os.path.exists(SOURCES_JSON_PATH):
        try:
            with open(SOURCES_JSON_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"sources": []}

def save_sources(data):
    os.makedirs(os.path.dirname(SOURCES_JSON_PATH), exist_ok=True)
    with open(SOURCES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/", methods=["GET", "POST"])
def index():
    data = load_sources()

    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "add":
            name = request.form.get("name")
            url = request.form.get("url")
            type_ = request.form.get("type")
            category = request.form.get("category")

            if not name or not url:
                flash("الاسم والرابط مطلوبان", "error")
            else:
                data["sources"].append({
                    "name": name,
                    "url": url,
                    "type": type_,
                    "category": category,
                    "enabled": True
                })
                save_sources(data)
                flash(f"تمت إضافة {name} بنجاح", "success")
        
        elif action == "delete":
            index = int(request.form.get("index"))
            if 0 <= index < len(data["sources"]):
                removed = data["sources"].pop(index)
                save_sources(data)
                flash(f"تم حذف {removed['name']}", "success")

        return redirect(url_for("index"))

    return render_template("index.html", sources=data["sources"])

@app.route("/update")
def run_update():
    try:
        # تشغيل سكربت التحديث في الخلفية
        subprocess.run(["python", UPDATE_SCRIPT_PATH], check=True)
        flash("تم تحديث القنوات من المصادر بنجاح!", "success")
    except Exception as e:
        flash(f"فشل التحديث: {str(e)}", "error")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
