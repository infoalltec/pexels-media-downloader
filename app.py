import os
from flask import Flask, render_template, request, jsonify
import requests
from urllib.parse import quote  # بديل آمن ومضمون
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# تكوين Pexels API
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        if not query:
            return jsonify({'error': 'يجب إدخال كلمة بحث'}), 400

        # بناء الرابط باستخدام urllib
        api_url = f"https://api.pexels.com/v1/search?query={quote(query)}&per_page=15"
        
        response = requests.get(api_url, headers={'Authorization': PEXELS_API_KEY})
        response.raise_for_status()
        
        return jsonify({
            'results': [{
                'src': photo['src']['medium'],
                'original': photo['src']['original']
            } for photo in response.json().get('photos', [])]
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
