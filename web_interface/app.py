from flask import Flask, render_template
import json
import os

app = Flask(__name__)
CHANNELS_JSON = os.path.join(os.path.dirname(__file__), "../remote/channels.json")

@app.route("/")
def index():
    # قراءة بيانات القنوات
    if os.path.exists(CHANNELS_JSON):
        with open(CHANNELS_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"categories": []}

    return render_template("index.html", categories=data.get("categories", []))

if __name__ == "__main__":
    app.run(debug=True)
