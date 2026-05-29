---
title: 3 Günlük Hafıza Özeti
tags: [hafiza, ozet, 2026, mayis]
date: 2026-05-23
status: active
brain: AB
---

# 🧠 3 Günlük Hafıza Özeti — 21-23 Mayıs 2026

Bu belge, Botfusions AI Reklam Ajansı Hermes Agent'in 21-23 Mayıs 2026 tarihleri arasındaki tüm konuşmalarının, kararlarının ve teknik detaylarının özetidir.

---

## 📊 Genel Durum

| Alan | Durum | Not |
|------|-------|-----|
| 🤖 Ekrem X Ajanı | ✅ Çalışıyor | Günde 3 tarama, havuzdan seç, 80+ skorla tweet |
| 🎨 Ayla (Görsel) | ⚠️ API key sorunu | Yeni Google AI Studio key lazım |
| 📋 Google Sheets | ✅ Bağlantı hazır | 97 TODO konu, pipeline test edildi |
| 🚀 İnfografik Pipeline | ⚠️ Ayla key bekliyor | 12:00/14:00 TSİ'de çalışacak |
| 💰 X API Kredisi | ✅ Yüklendi | Son 3 gün: 2 kez bitmiş, şimdi tekrar geldi |
| 📚 Wiki | ✅ 25+ sayfa | Günlükler, entity'ler, kararlar, hata analizleri |
| 🐶 Musti | ❌ İptal | Groq API internete erişemiyor |

---

## 🔑 API Anahtarları

| Servis | Değer | Yerde |
|--------|-------|-------|
| **DeepSeek** | `sk-da274deb322d44fb98d6f8bbe2ae0b87` | Pipeline'da hardcode |
| **Google AI Studio** | ❌ Geçersiz (yenisi lazım) | Skill'de frontmatter |
| **Google Sheets** | Refresh token ile çalışıyor | `.env` dosyasında |
| **X API (xurl)** | OAuth 1.0a + OAuth2 | `~/.xurl` dosyasında |
| **OpenRouter** | Maskelenmiş placeholder | `config.yaml`'da |

---

## 🤖 Ekrem X Ajanı — Yapılandırma

**Kimlik:** @botfusionss hesabından tweet atan self-improving AI ajanı
**Cron Job ID:** `061335902907`
**Schedule:** `0 3,10,15 * * *` (06:00/13:00/18:00 TSİ)
**Model:** DeepSeek deepseek-chat
**Skill:** `/opt/data/scripts/skills/ekrem-x-ajani.md` (v4.0)

**Çalışma Döngüsü:**
1. `xurl search` ile gündem tara (1 search yeter)
2. Tweet Havuzu'na ekle (`entities/ekrem-tweet-havuzu.md`)
3. Havuzdan seç + yorum kat
4. 0-100 skorla
5. 80+ ise `xurl post` ile at
6. `xurl read` ile metrik takip
7. Öğren + strateji güncelle

**Öğrenilmiş Dersler (Tekrarlama!):**
1. API key hardcode edilmeli (env maskelenmiş geçer)
2. xurl Node.js wrapper — subprocess'te PATH'e `/usr/bin` ekle
3. Media upload'da media_id `data.id`'de
4. Sheets 1-indexed (`i+1` unutma)
5. Gemini infografik 60sn sürer (timeout 120sn)
6. Pipeline adımlarını ayrı ayrı test et

---

## 🎨 Ayla — Yapılandırma

**Model:** Gemini 3.1 Flash Image Preview
**Skill:** `/opt/data/scripts/skills/ayla-gorsel-ajani.md` (v2)
**Wiki:** `entities/ayla-gorsel-uretim.md`

**Yapabilecekleri:**
- Görsel analiz (Telegram'dan gelen resimleri analiz)
- İnfografik üretimi (1200×675px, koyu tema)
- Pipeline entegrasyonu (Ekrem tweet + Ayla infografik → X)

**Blocker:** ❌ Google AI Studio API key geçersiz — yeni key lazım

---

## 📋 Google Sheets

**ID:** `1w-RqIicfrQlw2tM0Z9XJtuNCtrSCY9ALbbo4PEN7-B0`
**Sayfa:** `HERMES  X`
**İçerik:** 97 satır TODO konu (çoğu AI/SEO/dijital pazarlama)
**Kimlik Doğrulama:** OAuth 2.0 (refresh token ile)
**Refresh Token:** `.env` dosyasında

**Pipeline Kullanımı:**
1. Sheets'ten sıradaki TODO konuyu al
2. Ekrem araştır + tweet yaz (800-2000 karakter)
3. Ayla infografik oluştur
4. xurl ile X'e post et
5. Sheets'te DONE işaretle

---

## 🚀 Infografik Pipeline

**Script:** `/opt/data/scripts/hermes-infografik-pipeline.py`
**Planlanan Schedule:** `0 9,11 * * *` (12:00/14:00 TSİ)
**Durum:** Test edildi, Ayla key gelince çalışır

**Test Sonucu:**
- ✅ Sheets'ten konu al
- ✅ Ekrem tweet üret (1068 karakter)
- ❌ Ayla infografik (API key geçersiz)
- ❌ X'e post (infografik başarısız olunca iptal)

---

## 💰 X API Kredi Geçmişi

| Tarih | Post | Read | Media | Toplam |
|-------|------|------|-------|--------|
| 21 Mayıs | 3 | **656** 🚨 | 0 | ~660 |
| 22 Mayıs | 19 | **416** 🚨 | 6 | ~441 |
| 23 Mayıs | 6 | 67 | 0 | ~73 |

**Suçlu:** `botfusions-x-tara` cron job'u (her saat 26 read request × ~12 run/gün)
**Çözüm:** Cron duraklatıldı ✅, şimdi sadece Ekrem kendi search ile tarıyor

---

## 🗂️ Wiki Sayfaları

| Kategori | Sayfalar |
|----------|----------|
| **Günlükler** | 2026-05-21, 2026-05-22, 2026-05-23 |
| **Entity'ler** | ekrem-x-ajani, ayla-gorsel-uretim, ayla-analizleri, ekrem-tweet-havuzu, hermes-infografik-pipeline, botfusions-tweet-arsivi |
| **Kararlar** | 001-007 (telegram, windows, deployment, self-improvement, dashboard, hci, pipeline-hata) |
| **Sorunlar** | 002-windows-cli-encoding |
| **Sentezler** | sprint-context, teknik-mimari, entegrasyon-akisi |
| **Kavramlar** | ajan-ogrenme-dongusu |

---

## ❌ İptal Edilenler

1. **Musti (Groq API ajanı)** — Groq internete erişemiyor
2. **botfusions-x-tara cron job'u** — X API kredisini bitiriyordu

---

## ⏳ Bekleyen İşler

| İş | Blocker |
|----|---------|
| Google AI Studio API key yenileme | Kullanıcıdan bekleniyor |
| İnfografik pipeline cron'a bağlama | Ayla key gelince |
| Ekrem tweet arşivi wiki sayfası doldurma | Zamanla |
| 97 TODO konunun tamamını pipeline'dan geçirme | Sürekli süreç |

---

## 🔗 İlgili Sayfalar

- [[2026-05-21]]
- [[2026-05-22]]
- [[2026-05-23]]
- [[ekrem-x-ajani]]
- [[ayla-gorsel-uretim]]
- [[hermes-infografik-pipeline]]
- [[ekrem-tweet-havuzu]]
- [[007-pipeline-hata-cozumleri]]
