---
title: Hermes İnfografik Pipeline
tags: [pipeline, infografik, otomasyon, cron]
source: raw/pipeline-kurulum.md
date: 2026-05-23
status: active
brain: A
---

# Hermes İnfografik Pipeline

## Amaç
Google Sheets'ten konu al → Ekrem araştır + tweet yaz → Ayla infografik oluştur → X'e post et → Sheets DONE işaretle.

## Çalışma Zamanı
- **Günde 2 kez:** 12:00 ve 14:00 TSİ (09:00 ve 11:00 UTC)
- **Script:** `/opt/data/scripts/hermes-infografik-pipeline.py`

## Akış

```
[1/5] Google Sheets → sıradaki TODO konuyu al
[2/5] Ekrem (DeepSeek) → araştırma + tweet metni (800-2000 karakter)
[3/5] Ayla (Gemini) → infografik görsel oluştur
[4/5] xurl → X'e post et (görsel + metin)
[5/5] Google Sheets → DONE işaretle
```

## Sheets Yapısı
- **ID:** `1w-RqIicfrQlw2tM0Z9XJtuNCtrSCY9ALbbo4PEN7-B0`
- **Sayfa:** `HERMES  X`
- **Sütun A:** Konu başlığı
- **Sütun B:** Durum (TODO / DONE)

## API Anahtarları

| Servis | Değer | Durum |
|--------|-------|-------|
| DeepSeek | `sk-da274deb322d44fb98d6f8bbe2ae0b87` | ✅ Çalışıyor |
| Google AI Studio | Kullanıcıdan bekleniyor | ❌ Geçersiz |

## Cron Job (Planlanan)

Henüz cron'a bağlanmadı — manuel test aşamasında. Cron schedule: `0 9,11 * * *` (UTC).

## Test Durumu

| Adım | Sonuç |
|------|-------|
| Sheets'ten konu al | ✅ Konu #4 alındı |
| Ekrem tweet üret | ✅ 1068 karakter üretildi |
| Ayla infografik | ❌ API key geçersiz |
| X'e post | ❌ (infografik başarısız olunca iptal) |
| Sheets güncelle | ❌ (post başarısız) |

## Bağımlılıklar

- `pip install google-genai google-auth google-api-python-client`
- `xurl` (npm global: `@xdevplatform/xurl`)
- DeepSeek API key (hardcode)
- Google AI Studio API key (hardcode)

## İlgili Sayfalar

- [[ayla-gorsel-uretim]] — Ayla'nın yetenekleri ve API key durumu
- [[ekrem-x-ajani]] — Ekrem tweet üretim ajanı
- [[ekrem-tweet-havuzu]] — Tweet konuları havuzu
