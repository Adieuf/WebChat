const express = require('express');
const axios = require('axios');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());

const DIRECT_LINE_SECRET = process.env.DIRECT_LINE_SECRET;
const DIRECT_LINE_URL = 'https://directline.botframework.com/v3/directline/tokens/generate';

app.get('/api/token', async (req, res) => {
  if (!DIRECT_LINE_SECRET) {
    return res.status(500).json({ error: 'DIRECT_LINE_SECRET not configured' });
  }
  try {
    const response = await axios.post(
      DIRECT_LINE_URL,
      {},
      { headers: { Authorization: `Bearer ${DIRECT_LINE_SECRET}` } }
    );
    res.json({ token: response.data.token });
  } catch (err) {
    const status = err.response?.status || 500;
    res.status(status).send(err.response?.data || err.message);
  }
});

const PORT = process.env.PORT || 3978;
const HOST = process.env.HOST || '0.0.0.0';

app.listen(PORT, HOST, () => {
  console.log(`Server listening on http://${HOST}:${PORT}`);
});
