const express = require('express');
const axios = require('axios');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());

const PORT = process.env.PORT || 3000;
const API_KEY = process.env.PEXELS_API_KEY;

if (!API_KEY) {
  console.error("PEXELS_API_KEY غير موجود في متغيرات البيئة.");
  process.exit(1);
}

app.get('/search', async (req, res) => {
  const query = req.query.query;
  const type = req.query.type || 'photos';

  if (!query) {
    return res.status(400).json({ error: 'يرجى تحديد كلمة البحث' });
  }

  const endpoint = type === 'videos'
    ? 'https://api.pexels.com/videos/search'
    : 'https://api.pexels.com/v1/search';

  try {
    const response = await axios.get(endpoint, {
      headers: { Authorization: API_KEY },
      params: { query, per_page: 10 }
    });

    res.json(response.data);
  } catch (error) {
    console.error('خطأ في استدعاء Pexels:', error.message);
    res.status(500).json({ error: 'فشل في استدعاء خدمة Pexels' });
  }
});

app.listen(PORT, () => {
  console.log(`الخادم يعمل على http://localhost:${PORT}`);
});
