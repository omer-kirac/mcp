# ⚡ Hızlı Başlangıç - Enuygun MCP Agent

Sadece 3 adımda başlayın!

## 1️⃣ Bağımlılıkları Yükleyin

```powershell
pip install -r requirements.txt
```

## 2️⃣ API Anahtarınızı Ayarlayın

`.env` dosyası oluşturun ve düzenleyin:

```powershell
# .env dosyası oluştur
python setup_env.py
```

Sonra `.env` dosyasını bir metin editöründe açın ve şunu ekleyin:
```
ANTHROPIC_API_KEY=sk-ant-api03-xxx...
```

💡 **API Anahtarı nereden alınır?**
- https://console.anthropic.com/ adresine gidin
- Hesap oluşturun veya giriş yapın
- "API Keys" bölümünden yeni bir anahtar oluşturun

## 3️⃣ Agent'ı Başlatın

```powershell
python main.py
```

## ✅ İlk Denemeler

Agent başladığında şunları deneyin:

### 🔍 Mevcut Araçları Görün
```
tools
```

### 🛫 Uçak Bileti Arayın
```
İstanbul'dan Ankara'ya yarın 1 kişilik uçak bileti ara
```

### 🏨 Otel Arayın
```
İstanbul'da önümüzdeki hafta 2 kişilik otel ara
```

### 🌤️ Hava Durumu Sorun
```
Antalya'da bu hafta sonu hava nasıl olacak?
```

### 🚌 Otobüs Bileti Bulun
```
Ankara'dan İzmir'e gelecek hafta 2 kişilik otobüs bileti bul
```

## 🎯 Daha Fazlası İçin

- 📖 Detaylı örnekler: [ENUYGUN_GUIDE.md](ENUYGUN_GUIDE.md)
- 📚 Tam dokümantasyon: [README.md](README.md)
- 💡 Kullanım örnekleri: [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)

## ⚠️ Sorun mu Yaşıyorsunuz?

### "API Key Hatası"
✅ `.env` dosyanızın olduğundan emin olun
✅ ANTHROPIC_API_KEY'in doğru olduğunu kontrol edin

### "MCP Bağlantı Hatası"
✅ İnternet bağlantınızı kontrol edin
✅ Node.js yüklü olduğundan emin olun: `node --version`

### "Import Error"
✅ Bağımlılıkları yeniden yükleyin: `pip install -r requirements.txt`
✅ Sanal ortamı aktif edin: `venv\Scripts\activate`

## 🚀 Hazırsınız!

Artık Enuygun MCP agent'ınız hazır. İyi kullanımlar!

---

**İpucu:** `help` yazarak yardım menüsünü görebilirsiniz.


