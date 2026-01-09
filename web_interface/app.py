from flask import Flask, render_template
import json
from pathlib import Path

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent.parent
CHANNELS_JSON = BASE_DIR / "remote" / "channels.json"

@app.route("/")
def index():
    if CHANNELS_JSON.exists():
        with open(CHANNELS_JSON, "r", encoding="utf-8") as f:
            data = {"categories": json.load(f)}
    else:
        data = {"categories": []}
    return render_template("index.html", categories=data["categories"])

if __name__ == "__main__":
    app.run(debug=True)
