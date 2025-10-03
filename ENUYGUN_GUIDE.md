# 🛫 Enuygun MCP Kullanım Rehberi

Bu rehber, AI Agent'ınızla Enuygun MCP servisini kullanarak seyahat aramaları yapmanızı gösterir.

## 🎯 Neler Yapabilirsiniz?

Enuygun MCP servisi ile şunları yapabilirsiniz:
- ✈️ **Uçak bileti arama**
- 🏨 **Otel arama**
- 🚌 **Otobüs bileti arama**
- 🚗 **Araba kiralama**
- 🌤️ **Hava durumu tahminleri**

## 🚀 Başlangıç

### 1. Agent'ı Çalıştırın
```powershell
python main.py
```

### 2. Enuygun Araçlarını Kontrol Edin
```
Siz: tools
```

Şu araçları göreceksiniz:
- `enuygun.flight_search` - Uçak bileti arama
- `enuygun.hotel_search` - Otel arama
- `enuygun.bus_search` - Otobüs bileti arama
- `enuygun.car_search` - Araba kiralama arama
- `enuygun.flight_weather_forecast` - Uçuş için hava durumu
- `enuygun.hotel_weather_forecast` - Otel konumu için hava durumu
- `enuygun.car_weather_forecast` - Araba kiralama için hava durumu
- `enuygun.bus_weather_forecast` - Otobüs seyahati için hava durumu

## 📖 Kullanım Örnekleri

### ✈️ Uçak Bileti Arama

```
Siz: İstanbul'dan İzmir'e 15 Kasım'da 2 yetişkin için uçak bileti ara

Agent: [Enuygun'da uçuş araması yapar ve seçenekleri gösterir]
```

**Daha detaylı arama:**
```
Siz: İstanbul'dan Antalya'ya 25 Aralık'ta gidiş, 30 Aralık'ta dönüş, 
     2 yetişkin 1 çocuk, business class, sadece direkt uçuşlar
```

### 🏨 Otel Arama

```
Siz: İstanbul'da 20-25 Kasım tarihleri arası 2 kişilik otel ara

Agent: [Otel seçeneklerini listeler]
```

**Çocuklu arama:**
```
Siz: Antalya'da 1 Haziran - 10 Haziran arası, 2 yetişkin ve 
     8 ve 12 yaşında 2 çocuk için otel ara
```

### 🚌 Otobüs Bileti Arama

```
Siz: Ankara'dan İzmir'e 18 Kasım'da 1 kişi için otobüs bileti bul

Agent: [Otobüs seferlerini gösterir]
```

**Gidiş-dönüş:**
```
Siz: İstanbul'dan Ankara'ya 20 Kasım gidiş, 22 Kasım dönüş, 
     2 yetişkin için otobüs bileti ara
```

### 🚗 Araba Kiralama

```
Siz: İstanbul'da 15 Kasım saat 10:00'da al, 20 Kasım saat 18:00'de 
     bırak, 25 yaşında sürücü için araba kirala

Agent: [Araba kiralama seçeneklerini gösterir]
```

**Farklı lokasyonlarda teslim:**
```
Siz: İstanbul'da 1 Aralık saat 09:00'da al, Antalya'da 10 Aralık 
     saat 20:00'de bırak, 30 yaşında sürücü
```

### 🌤️ Hava Durumu Sorguları

```
Siz: İstanbul'da 15-20 Kasım arası hava durumu nasıl olacak?

Agent: [Hava durumu tahminini gösterir]
```

```
Siz: Antalya'da yarın uçuş yapmak için hava uygun mu?

Agent: [Hava durumunu kontrol eder ve bilgi verir]
```

## 💡 Gelişmiş Kullanım

### Karşılaştırma Yapma

```
Siz: İstanbul-İzmir arası hem uçak hem otobüs seçeneklerini göster 
     ve karşılaştır

Agent: 
[Her iki arama sonucunu gösterir]
[Fiyat, süre ve konfor açısından karşılaştırır]
```

### Tatil Planı Oluşturma

```
Siz: Antalya'ya 3 günlük tatil planla. 
     - 25 Aralık gidiş, 28 Aralık dönüş
     - 2 kişilik uçak bileti
     - Otel rezervasyonu
     - Araba kiralama
     - Hava durumu kontrolü

Agent: 
[Kapsamlı bir tatil planı hazırlar]
[Tüm seçenekleri sırayla arar ve önerir]
```

### Bütçe Analizi

```
Siz: İstanbul'dan Bodrum'a 1 haftalık tatil için toplam maliyet nedir?
     Uçak, otel ve araba dahil. 2 yetişkin için.

Agent:
[Tüm seçenekleri arar]
[Toplam maliyeti hesaplar]
[Farklı bütçe seçenekleri sunar]
```

## 📅 Tarih Formatları

Agent doğal dil ile tarihleri anlayabilir:
- ✅ "15 Kasım", "15 Kasım 2024"
- ✅ "Yarın", "Gelecek hafta"
- ✅ "15.11.2024"
- ✅ "2024-11-15"

## 🎯 İpuçları

1. **Açık ve Detaylı Olun**: Ne kadar detay verirseniz, o kadar iyi sonuç alırsınız
2. **Esneklik Belirtin**: "±2 gün esnek" gibi esnekliklerinizi belirtin
3. **Öncelikleri Paylaşın**: "En ucuz seçenekleri göster" veya "Konfor öncelikli"
4. **Çoklu Arama**: Farklı seçenekleri karşılaştırmak için birden fazla arama yapın

## ⚠️ Önemli Notlar

- Fiyatlar anlık olarak değişebilir
- Son rezervasyon için Enuygun web sitesini ziyaret edin
- Vize ve pasaport gereksinimlerini kontrol etmeyi unutmayın
- Bagaj kurallarını ve ek ücretleri gözden geçirin

## 🔍 Sorun Giderme

### "Sonuç Bulunamadı"
- Tarihleri kontrol edin (geçmiş tarihler olabilir)
- Daha esnek tarihler deneyin
- Farklı şehir isimleri kullanmayı deneyin (örn: "İstanbul" yerine "IST")

### "Hata Oluştu"
- İnternet bağlantınızı kontrol edin
- Daha sonra tekrar deneyin
- Agent'ı yeniden başlatın: `clear` komutu kullanın

## 📞 Yardım

Daha fazla yardım için:
```
Siz: help
```

veya

```
Siz: Enuygun ile neler yapabilirim?
```

---

**İyi seyahatler! ✈️🏨🚌🚗**


