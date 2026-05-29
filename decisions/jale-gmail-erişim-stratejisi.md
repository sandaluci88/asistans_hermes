---
title: Jale Gmail Erişim Strateji Değerlendirmesi
tags: [jale, gmail, email, gws-botfusionss, strateji, decision]
date: 2026-05-27
status: active
brain: B
---

# Jale Gmail Erişimi — Strateji Değerlendirmesi ve Karar Noktaları

## 1. Mevcut Durum Özeti

| Bileşen | Durum |
|---------|-------|
| **Güngör (GitHub Ops Agent)** | botfusionss@gmail.com Gmail API erişimi var. `gws-botfusionss` Python aracı + OAuth JSON token. Sadece `from:github.com` maillerini okur, değerlendirme yapmaz. |
| **Jale (Sistem Yönetici Asistanı)** | Mail erişimi **yok**. IMAP-based `jale-email-monitor.py` mevcut ama IMAP bilgileri `.env`'de boş/yorumda. Çalışmaz durumda. |
| **Mevcut OAuth** | `~/.config/email-hermes/gcp-oauth-botfusionss.json` — Güngör'e ait. |
| **Mevcut Mail Aracı** | `gws-botfusionss` — Google Workspace CLI wrapper, Python tabanlı. Aynı anda tek OAuth token ile çalışır. |
| **Jale'nin Mevcut Yetenekleri** | Dreaming (DeepSeek analiz, RSS tarama), Haftalık fleet durum raporu (cron: `jale-fleet-durum-raporu`), X pipeline koordinasyonu. |

## 2. Değerlendirme: Neden Jale'nin Mail Erişimi Olmalı?

| Kazanım | Açıklama | Öncelik |
|---------|----------|---------|
| **Gelen Kutusu Triage** | Önemli/önemsiz ayırma, etiketleme, kategorizasyon. Güngör sadece GitHub maillerine bakar, geri kalan her şey (bültenler, bildirimler, müşteri mailleri) okunmaz. | Yüksek |
| **Günlük Brifing Mail Özeti** | Jale'nin dreaming/sabah raporuna mail özeti entegrasyonu. | Yüksek |
| **Hatırlatıcı & Takvim** | Mail üzerinden gelen toplantı davetleri, deadline bildirimleri. | Orta |
| **Aksiyon Maddeleri** | Mail içinde "şunu yap" taleplerini tespit edip göreve dönüştürme. | Orta |
| **Güvenlik & Uyarılar** | Hesap güvenlik bildirimleri, şifre değişikliği, yeni cihaz girişleri. | Yüksek |

## 3. Mimari Seçenekler

### SEÇENEK A: Güngör ile Aynı OAuth Token'ı Paylaşma

**Nasıl çalışır:** Jale, Güngör'ün mevcut `gcp-oauth-botfusionss.json` token'ını kullanır. İkisi de `gws-botfusionss` aracı üzerinden botfusionss@gmail.com'a erişir.

| Artılar | Eksiler |
|---------|---------|
| + Sıfır yeni GCP projesi/kurulum | − Token sadece tek bir scope ile yetkilendirilmiş olabilir (Güngör sadece `from:github.com` okur) |
| + Hemen çalışmaya başlar | − Token paylaşımı: biri refresh yaparsa diğerini kırma riski |
| + Tek OAuth yönetimi | − Denetim/günlük: "kim ne yaptı" takibi zor |
| | − İkisi aynı anda okuma/yazma yaparsa yarış koşulu |

**Risk: YÜKSEK.** Aynı anda iki agent aynı token ile farklı sorgular yaparsa Google API rate limiting veya token refresh çakışması yaşanabilir. Ayrıca Güngör'ün scope'u (sadece `from:github.com` okuma) Jale'nin tüm gelen kutusuna erişmesi için yeterli olmayabilir.

### SEÇENEK B: Aynı Gmail Hesabı, Ayrı OAuth Token (Önerilen)

**Nasıl çalışır:** Jale için ayrı bir GCP OAuth token'ı oluşturulur, aynı botfusionss@gmail.com hesabına erişir. İkinci bir `gws-jale` adında tool instance'ı veya alias.

| Artılar | Eksiler |
|---------|---------|
| + İzole token yönetimi | − İkinci bir GCP OAuth setup gerektirir (manuel adım) |
| + Her agent kendi scope'u ile çalışır | − Aynı mailbox'a iki farklı token ile bağlanmak Google rate limit'e takılabilir |
| + Denetim: hangi token ne yaptı belli | |
| + Biri kırılırsa diğeri çalışmaya devam eder | |

**Risk: DÜŞÜK.** Gmail API rate limit'leri 250 quota units/saniye. İki API çağrısı aynı anda yapılmazsa sorun olmaz. Jale'nin cron job'ları (günde 1-2 kez) ile Güngör'ün saatlik kontrolleri çakışmaz.

### SEÇENEK C: IMAP ile Doğrudan Erişim

**Nasıl çalışır:** Mevcut `jale-email-monitor.py` canlandırılır. Gmail App Password ile IMAP erişimi.

| Artılar | Eksiler |
|---------|---------|
| + GCP projesi gerektirmez | − Gmail App Passwords artık sadece 2FA + özel uygulama şifreleri ile çalışır |
| + Hızlı setup | − IMAP modern Gmail özelliklerini (etiketler, filtreler) desteklemez |
| + Basit kod | − Güvenlik: App Password düz metin, OAuth kadar güvenli değil |
| | − Google, IMAP erişimini 2024'ten itibaren kısıtlıyor |

**Risk: ORTA.** IMAP basit bir çözüm ama uzun vadede sürdürülebilir değil. Google OAuth'u zorunlu kılmaya doğru gidiyor.

## 4. Önerilen Strateji: Seçenek B (Ayrı Token)

### Adımlar

1. **Yeni GCP OAuth Token'ı Oluştur**
   - Mevcut GCP projesinde (`botfusionss`) yeni bir OAuth 2.0 Client ID oluştur
   - Scope: `https://www.googleapis.com/auth/gmail.readonly` (Jale sadece okuyacak, yazmayacak)
   - Token'ı `~/.config/email-hermes/gcp-oauth-jale.json` olarak kaydet
   - İlk yetkilendirme için hermes konsolundan manuel URL açılması gerekebilir

2. **Jale İçin `gws-jale` Alias / Instance**
   - Mevcut `gws-botfusionss` tool'unu kopyala veya alias oluştur
   - Jale'nin SOUL'una `gws-jale` tool'u olarak tanımla
   - Tool, sadece `gmail.users.messages.list` ve `gmail.users.messages.get` yetkisine sahip olmalı (read-only)

3. **SOUL Kuralları**
   - Jale'nin mail okuma kuralları (aşağıda detaylandırılmıştır)
   - Hangi tür mailleri okuyacağı, hangilerini atlayacağı
   - Gizlilik: Jale asla mail içeriğini raw olarak Telegram'a forward etmez, sadece özet geçer

4. **Cron Job Düzenlemesi**
   - Mevcut `jale-fleet-durum-raporu` cron'una mail özeti entegre et
   - Yeni bir `jale-email-brifing` cron'u (sabah 08:00 TSİ)
   - Güngör'ün `gungor-jules-check` (her saat) ile çakışma kontrolü

5. **İzleme ve Loglama**
   - Jale her mail sorgusunda kaç mail okuduğunu loglasın
   - Token refresh hatalarını Jale'nin kendi kendine rapor edeceği bir mekanizma

## 5. Karar Verilmesi Gereken Noktalar

### 🔴 Karar 1: Token Türü
- **A** — Güngör ile aynı token'ı paylaş (riskli, hızlı)
- **B** — Ayrı OAuth token oluştur (güvenli, 1 saat setup)
- **C** — IMAP App Password (basit, geçici)

### 🔴 Karar 2: Erişim Scope'u
- **Read-only**: `gmail.readonly` — Jale sadece okur, asla silmez/göndermez (önerilen)
- **Read-write**: `gmail.modify` — Silme, okundu işaretleme, etiketleme
- **Full access**: `gmail.send` dahil — Mail gönderme yetkisi (en riskli)

**Öneri: Read-only ile başla, ihtiyaç halinde kademeli artır.**

### 🔴 Karar 3: Hangi Mailler?
Jale hangi mailleri okuyacak?

| Kategori | Oku? | Açıklama |
|----------|------|----------|
| `from:github.com` | Hayır | Güngör'ün sorumluluğu |
| `from:jules+bots@google.com` | Hayır | Güngör kontrol ediyor |
| `category:primary` (insan mailleri) | Evet | Müşteri, iş ortağı, yönetici |
| `category:social` | Şartlı | Sadece önemli keyword varsa |
| `category:promotions` | Şartlı | Sadece önemli keyword varsa |
| `is:unread` genel tarama | Evet | Günde 1 kez |
| Güvenlik bildirimleri | Evet | Google hesap güvenliği, şifre değişikliği |
| Bültenler | Hayır | Kaynak israfı |

### 🔴 Karar 4: Tool İsmi ve Konfigürasyon
- `gws-jale` adıyla mı yoksa parametrik olarak mı (`--account jale`)?
- SOUL'a tool tanımı nasıl entegre edilecek?
- Jale'nin SOUL'u nerede duracak? (Mevcut: `/opt/data/wiki/` altında jale ile ilgili dosyalar var ama SOUL yok)

### 🔴 Karar 5: Güvenlik Politikası
- Jale mail içeriğini raw olarak gönderebilir mi?
- Mail → Telegram forward kuralları?
- Hassas veri (parola, API key) içeren mailler nasıl filtrelenecek?

## 6. Jale'nin SOUL'una Eklenecek Mail Kuralları

```markdown
- `gws-jale` tool'unu SOUL'da tanımla: `gws-jale gmail users messages list --params '{"userId":"me","q":"{query}","maxResults":10}'`
- Günde 3 kez okuma limiti: sabah 08:00, öğlen 12:00, akşam 18:00 TSİ
- Asla gmail.users.messages.modify veya delete kullanma
- Raw mail içeriğini Telegram'a forward etme — sadece özet (subject + from + 1 cümle)
- Hassas keyword içeren mailleri (parola, şifre, API key, token) özette belirtme — sadece "Hassas içerikli mail" olarak işaretle
- Güngör'ün sorguladığı mailleri tekrar sorgulama (from:github.com, from:jules+bots)
```

## 7. Özet ve Öncelikli Aksiyonlar

| # | Aksiyon | Öncelik | Süre |
|---|---------|---------|------|
| 1 | **Karar ver**: Hangi token stratejisi (B önerilir) | Yüksek | Hemen |
| 2 | **Karar ver**: Read-only vs read-write | Yüksek | Hemen |
| 3 | Yeni OAuth token oluştur (GCP Console) | Yüksek | ~30 dk |
| 4 | Jale SOUL'una gws-jale tool tanımını ekle | Yüksek | ~15 dk |
| 5 | Cron job'ları düzenle / yeni cron ekle | Orta | ~30 dk |
| 6 | Test: ilk mail sorgusu + Telegram raporu | Orta | ~15 dk |
| 7 | Güvenlik filtresi ve hassas veri politikasını kodla | Orta | ~45 dk |

## 8. Related

- [[gungor-github-ops]]
- [[jale-dreaming]]
- [[jale-x-pipeline]]
- [[email-architecture]]
