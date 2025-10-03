# 📖 Kullanım Örnekleri

Bu dosya, MCP AI Agent'ın çeşitli kullanım senaryolarını ve örneklerini içerir.

## 🗂️ Dosya Sistemi İşlemleri

### Dosya Listeleme
```
Siz: Belgeler klasöründeki tüm dosyaları listele
Agent: [filesystem araçlarını kullanarak dosyaları listeler]

Siz: Python dosyalarını bul
Agent: [.py uzantılı dosyaları bulur ve listeler]
```

### Dosya Okuma ve Analiz
```
Siz: README.md dosyasını oku ve özetle
Agent: [dosyayı okur ve içeriğini özetler]

Siz: Tüm Python dosyalarında "TODO" yorumlarını bul
Agent: [dosyaları tarar ve TODO yorumlarını listeler]
```

## 💾 Veritabanı İşlemleri

### PostgreSQL Sorguları
```
Siz: users tablosundaki toplam kullanıcı sayısını göster
Agent: SELECT COUNT(*) FROM users; [sorguyu çalıştırır]

Siz: Son 10 siparişi getir
Agent: SELECT * FROM orders ORDER BY created_at DESC LIMIT 10;
```

### SQLite İşlemleri
```
Siz: database.db içindeki tüm tabloları listele
Agent: [veritabanı şemasını gösterir]
```

## 🌐 Web İşlemleri

### Web Scraping (Puppeteer)
```
Siz: example.com sitesinin başlığını al
Agent: [siteyi ziyaret eder ve başlığı döndürür]

Siz: Bu web sayfasındaki tüm bağlantıları listele
Agent: [sayfadaki tüm linkleri bulur ve listeler]
```

### Web Arama (Brave Search)
```
Siz: Python asenkron programlama hakkında arama yap
Agent: [web'de arama yapar ve sonuçları özetler]

Siz: En son AI haberlerini bul
Agent: [güncel haberleri arar ve özetler]
```

## 🐙 GitHub İşlemleri

### Repository Bilgileri
```
Siz: microsoft/vscode repository'sinin son commit'lerini göster
Agent: [son commit'leri getirir ve gösterir]

Siz: Bu repository'deki açık issue'ları listele
Agent: [açık issue'ları listeler]
```

### Kod Analizi
```
Siz: Bu repository'de en çok değişen dosyaları bul
Agent: [commit geçmişini analiz eder]
```

## 🧠 Hafıza (Memory) İşlemleri

### Bilgi Saklama
```
Siz: Şunu hatırla: Benim en sevdiğim renk mavi
Agent: Anladım, bu bilgiyi kaydettim.

Siz: En sevdiğim renk neydi?
Agent: En sevdiğin renk mavi.
```

## 🔄 Karmaşık İş Akışları

### Proje Analizi
```
Siz: Bu Python projesini analiz et. Dosya yapısını, bağımlılıkları ve 
     potansiyel iyileştirme noktalarını belirle.

Agent: 
1. Dosya yapısını tarar
2. requirements.txt'i okur
3. Kod kalitesini değerlendirir
4. Öneriler sunar
```

### Veri İşleme
```
Siz: CSV dosyasını oku, veriyi analiz et ve özet istatistikler çıkar

Agent:
1. Dosyayı okur
2. Veriyi parse eder
3. İstatistikleri hesaplar
4. Sonuçları sunar
```

### Otomatik Dokümantasyon
```
Siz: src/ klasöründeki tüm Python fonksiyonlarını bul ve 
     dokümantasyon eksikliklerini belirle

Agent:
1. Tüm .py dosyalarını tarar
2. Fonksiyonları bulur
3. Docstring'leri kontrol eder
4. Eksiklikleri raporlar
```

## 🎯 İpuçları ve En İyi Uygulamalar

### Açık ve Spesifik Talimatlar
❌ Kötü: "dosyaları bul"
✅ İyi: "src/ klasöründeki son 7 gün içinde değiştirilmiş Python dosyalarını bul"

### Adım Adım İşlemler
```
Siz: Şu adımları takip et:
1. config.json dosyasını oku
2. database_url değerini bul
3. Bu veritabanına bağlan
4. users tablosundaki kayıt sayısını göster

Agent: [her adımı sırayla gerçekleştirir]
```

### Bağlam Sağlama
```
Siz: Geçen hafta bahsettiğim proje için bir README hazırla

Agent: Üzgünüm, önceki konuşmalardan bilgi bulunmuyor. 
       Proje hakkında daha fazla detay verebilir misiniz?

[Daha iyi:]
Siz: Python web scraper projem için bir README hazırla. 
     Proje Beautiful Soup ve Selenium kullanıyor.

Agent: [detaylı README oluşturur]
```

### Hata Ayıklama
```
Siz: Son çalıştırdığın koddaki hatayı açıkla

Agent: [son tool çağrısını analiz eder ve hatayı açıklar]
```

## 🔐 Güvenlik Notları

### Hassas Veriler
- API anahtarlarını ve şifreleri asla agent'a vermeyin
- Agent'ın erişim izinlerini dikkatle yapılandırın
- Sadece güvenli dizinlere erişim verin

### İzinler
```python
# İyi: Sınırlı erişim
"filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", 
             "C:/Users/YourUser/Projects/CurrentProject"]
}

# Kötü: Geniş erişim
"filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:/"]
}
```

## 📊 Performans İpuçları

### Büyük Dosyalarla Çalışma
```
Siz: 10MB'lık log dosyasının son 100 satırını göster
[Tüm dosyayı okumak yerine]

Siz: Bu dizindeki dosyaları boyutlarına göre sırala ama içeriklerini okuma
[Sadece metadata kullan]
```

### Toplu İşlemler
```
Siz: src/ klasöründeki tüm dosyalarda "old_function" 
     kelimesini "new_function" ile değiştir

Agent: [toplu değiştirme işlemi yapar]
```

## 🎨 Yaratıcı Kullanımlar

### Kod İncelemesi
```
Siz: app.py dosyasını incele ve kod kalitesi, güvenlik ve 
     performans açısından öneriler sun
```

### Proje Yapılandırma
```
Siz: Bu proje için .gitignore, .editorconfig ve 
     yapılandırma dosyaları oluştur
```

### Test Yazma
```
Siz: calculator.py dosyasındaki tüm fonksiyonlar için 
     unit testler yaz
```

---

**Daha fazla örnek ve yardım için README.md dosyasına bakın!**


