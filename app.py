import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def clean_query(query):
    # إزالة الرموز غير المرغوب فيها مثل النقاط والفواصل
    return ''.join(e for e in query if e.isalnum() or e.isspace())

def search_pexels_with_type(media_type):
    query = request.args.get("query", "").strip()
    page = int(request.args.get("page", 1))

    if not query:
        return jsonify({"error": "Missing query"}), 400
    
    # تنظيف الاستعلام
    query = clean_query(query)

    url = f"https://api.pexels.com/v1/{'videos/' if media_type == 'videos' else ''}search?query={query}&per_page={5 if media_type == 'videos' else 10}&page={page}"
    headers = {"Authorization": PEXELS_API_KEY}
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        return jsonify({"error": "Failed to fetch from Pexels"}), 500
    
    return jsonify(res.json())

@app.route("/api/photos", methods=["GET"])
def search_photos():
    return search_pexels_with_type("photos")

@app.route("/api/videos", methods=["GET"])
def search_videos():
    return search_pexels_with_type("videos")

if __name__ == "__main__":
    app.run(debug=True)
