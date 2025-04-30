import os
from flask import Flask, render_template, request, jsonify
import requests
from urllib.parse import quote  # المكتبة القياسية لبايثون
from dotenv import load_dotenv

# تأكد من عدم وجود أي استيراد لـ werkzeug هنا

load_dotenv()

app = Flask(__name__)

PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        query = request.json.get('query', '').strip()
        if not query:
            return jsonify({'error': 'أدخل كلمة بحث'}), 400
            
        # الترميز الآمن مع urllib
        encoded_query = quote(query)
        url = f"https://api.pexels.com/v1/search?query={encoded_query}&per_page=15"
        
        res = requests.get(url, headers={'Authorization': PEXELS_API_KEY})
        res.raise_for_status()
        
        photos = [{
            'src': p['src']['medium'],
            'original': p['src']['original']
        } for p in res.json().get('photos', [])]
        
        return jsonify({'photos': photos})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
