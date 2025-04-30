import os
from flask import Flask, render_template, request, jsonify
import requests
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        media_type = data.get('mediaType', 'photos').strip()
        page = int(data.get('page', 1))

        if not query:
            return jsonify({'success': False, 'error': 'أدخل كلمة بحث'}), 400

        encoded_query = quote(query)
        url = f"https://api.pexels.com/v1/{media_type}?query={encoded_query}&per_page=15&page={page}"

        response = requests.get(url, headers={"Authorization": PEXELS_API_KEY})
        response.raise_for_status()
        data = response.json()

        results = []
        if media_type == "photos":
            for item in data.get('photos', []):
                results.append({
                    'type': 'photo',
                    'src': item['src']['medium'],
                    'original': item['src']['original'],
                    'alt': item.get('alt', '')
                })
        elif media_type == "videos":
            for item in data.get('videos', []):
                video_url = item['video_files'][0]['link'] if item['video_files'] else ''
                results.append({
                    'type': 'video',
                    'src': video_url,
                    'original': item['url']
                })

        return jsonify({
            'success': True,
            'results': results,
            'has_more': data.get('next_page') is not None
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
