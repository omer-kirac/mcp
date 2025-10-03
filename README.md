# MCP AI Agent

AI Agent entegre edilmiş Model Context Protocol (MCP) ile seyahat arama ve rezervasyon işlemleri yapabilen akıllı asistan.

## 🚀 Özellikler

- ✈️ Uçuş arama ve rezervasyon (Enuygun API)
- 🏨 Otel arama
- 🚌 Otobüs bileti arama
- 🚗 Araç kiralama
- 🌤️ Hava durumu tahminleri
- 🤖 Claude AI ile akıllı konuşma

## 📋 Gereksinimler

- Python 3.11+
- Node.js (npx için)
- Anthropic API Key

## 🔧 Kurulum

1. Repoyu klonlayın:
```bash
git clone https://github.com/abdullahozbay780/yeni-proje.git
cd yeni-proje
```

2. Python bağımlılıklarını yükleyin:
```bash
pip install anthropic mcp rich python-dotenv
```

3. `.env` dosyası oluşturun:
```env
ANTHROPIC_API_KEY=your_api_key_here
MODEL_NAME=claude-3-5-sonnet-20241022
MAX_TOKENS=4096
TEMPERATURE=0.7
```

## 🎯 Kullanım

Agent'i başlatın:
```bash
python main.py
```

Örnek komutlar:
- "İstanbul'dan İzmir'e yarın uçuş ara"
- "Antalya'da otel bul, giriş 10.10.2025"
- "Ankara'nın hava durumu nasıl?"

## 📁 Proje Yapısı

```
yeni-proje/
├── main.py           # Ana giriş noktası
├── agent.py          # MCP Agent sınıfı
├── mcp_client.py     # MCP Client
├── config.py         # Yapılandırma
├── .env              # Ortam değişkenleri (git'e eklenmez)
└── ENUYGUN_GUIDE.md  # Enuygun API rehberi
```

## 🔐 Güvenlik

- `.env` dosyasını asla commit etmeyin
- API key'lerinizi güvenli tutun

## 📄 Lisans

MIT License
