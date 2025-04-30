import os
from flask import Flask, render_template, request, jsonify
import requests
from werkzeug.utils import quote as url_quote
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Pexels API key from environment variables
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        media_type = data.get('mediaType', 'photos')
        query = data.get('query', '').strip()
        page = data.get('page', 1)
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Build API URL
        if media_type == 'photos':
            api_url = f"https://api.pexels.com/v1/search?query={url_quote(query)}&per_page=12&page={page}"
        else:
            api_url = f"https://api.pexels.com/videos/search?query={url_quote(query)}&per_page=6&page={page}"
        
        # Make request to Pexels API
        response = requests.get(api_url, headers={'Authorization': PEXELS_API_KEY})
        response.raise_for_status()
        data = response.json()
        
        # Format results
        results = []
        if media_type == "photos":
            results = [{
                'type': 'photo',
                'src': photo['src']['medium'],
                'original': photo['src']['original'],
                'alt': photo.get('alt', 'صورة')
            } for photo in data.get('photos', [])]
        else:
            results = [{
                'type': 'video',
                'src': next(
                    (f['link'] for f in video['video_files'] 
                    if f['quality'] == 'sd' and f['file_type'] == 'video/mp4'),
                    video['video_files'][0]['link']
                )
            } for video in data.get('videos', [])]
        
        return jsonify({
            'success': True,
            'results': results,
            'has_more': len(results) > 0
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
