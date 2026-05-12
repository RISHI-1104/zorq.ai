const express = require('express');
const cors = require('cors');
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static('.'));

// ⚠️  NOTE: This is legacy Node.js code. Use server.py (Flask) instead!
// For security, API keys must NEVER be hardcoded in source code.
// Use environment variables via .env file (see .env.example)

// const GROQ_API_KEY = process.env.GROQ_API_KEY || 'gsk_YOUR_ACTUAL_API_KEY_HERE';
// Please use server.py instead - it's production-ready with proper security!

const GROQ_API_KEY = process.env.GROQ_API_KEY || 'NOT_SET';

app.post('/api/chat', async (req, res) => {
  try {
    const { messages } = req.body;
    
    if (!messages || !Array.isArray(messages)) {
      return res.status(400).json({ error: 'Invalid messages format' });
    }

    const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${GROQ_API_KEY}`
      },
      body: JSON.stringify({
        model: 'mixtral-8x7b-32768',
        messages: messages,
        max_tokens: 1024,
        temperature: 0.7
      })
    });

    const data = await response.json();
    
    if (!response.ok) {
      console.error('Groq API Error:', data);
      return res.status(response.status).json({ error: data.error?.message || 'API request failed' });
    }

    const reply = data.choices?.[0]?.message?.content || 'No response received.';
    res.json({ reply });
  } catch (error) {
    console.error('Server error:', error);
    res.status(500).json({ error: error.message || 'Internal server error' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`ZORQ server running on http://localhost:${PORT}`);
});
