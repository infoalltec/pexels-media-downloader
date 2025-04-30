import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def translate_to_english(text):
    try:
        url = f"https://api.mymemory.translated.net/get?q={text}&langpair=ar|en"
        res = requests.get(url).json()
        return res.get("responseData", {}).get("translatedText", text)
    except:
        return text

@app.route("/api/search", methods=["GET"])
def search_pexels():
    query = request.args.get("query", "").strip()
    media_type = request.args.get("media_type", "photos")
    page = int(request.args.get("page", 1))

    if not query or media_type not in ["photos", "videos"]:
        return jsonify({"error": "Invalid parameters"}), 400

    translated_query = translate_to_english(query)
    url = f"https://api.pexels.com/v1/{'videos/' if media_type == 'videos' else ''}search?query={translated_query}&per_page={5 if media_type == 'videos' else 10}&page={page}"

    headers = {"Authorization": PEXELS_API_KEY}
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        return jsonify({"error": "Failed to fetch from Pexels"}), 500

    return jsonify(res.json())

if __name__ == "__main__":
    app.run(debug=True)
