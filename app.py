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
        media_type = data.get('mediaType', 'photos')  # يمكن photos أو videos
        page = int(data.get('page', 1))

        if not query:
            return jsonify({'error': 'أدخل كلمة بحث'}), 400

        encoded_query = quote(query)
        per_page = 15
        url = f"https://api.pexels.com/v1/{media_type}?query={encoded_query}&per_page={per_page}&page={page}"
        
        res = requests.get(url, headers={'Authorization': PEXELS_API_KEY})
        res.raise_for_status()

        if media_type == "videos":
            items = [{
                'type': 'video',
                'src': v['video_files'][0]['link'],
                'original': v['url'],
                'alt': v['user']['name']
            } for v in res.json().get('videos', [])]
        else:
            items = [{
                'type': 'photo',
                'src': p['src']['medium'],
                'original': p['src']['original'],
                'alt': p['alt']
            } for p in res.json().get('photos', [])]

        return jsonify({
            'success': True,
            'results': items,
            'has_more': len(items) == per_page
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
if __name__ == '__main__':
    app.run()
