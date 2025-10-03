const express = require('express');
const Anthropic = require('@anthropic-ai/sdk');
const config = require('./src/config/config');

// API anahtarının varlığını kontrol et
if (!config.anthropicApiKey) {
  console.error('ANTHROPIC_API_KEY bulunamadı. Lütfen .env dosyanızı kontrol edin.');
  process.exit(1);
}

const anthropic = new Anthropic({
  apiKey: config.anthropicApiKey,
});

const app = express();

app.use(express.json());

// Test endpoint'i
app.get('/', (req, res) => {
  res.json({ message: 'API çalışıyor' });
});

// Anthropic API endpoint'i
app.post('/api/chat', async (req, res) => {
  try {
    const message = await anthropic.messages.create({
      model: "claude-3-opus-20240229",
      max_tokens: 1000,
      messages: [
        {
          role: "user",
          content: req.body.message || "Merhaba!"
        }
      ]
    });
    
    res.json(message);
  } catch (error) {
    console.error('Anthropic API Hatası:', error);
    res.status(500).json({ error: 'Bir hata oluştu' });
  }
});

app.listen(config.port, () => {
  console.log(`Server ${config.port} portunda çalışıyor`);
});
