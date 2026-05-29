---
title: Ayla — Görsel Analiz & Üretim Sayfası
tags: [ayla, görsel, infografik, gemini]
source: raw/ayla-kurulum.md
date: 2026-05-23
status: active
brain: A
---

# Ayla — Görsel Analiz & Üretim Ajanı

## Kimlik
- **Ad:** Ayla
- **Rol:** Görsel analist + üretici
- **Dil:** Türkçe
- **Model:** Google Gemini 3.1 Flash Image Preview (`gemini-3.1-flash-image-preview`)
- **Fallback:** Google Gemini 3.5 Flash (`google/gemini-3.5-flash`)
- **API:** Google AI Studio (`generativelanguage.googleapis.com`)

## Yetenekler

### 1. Görsel Analiz (Vision)
- Telegram'dan gelen resimleri analiz eder
- Gemini 3.5 Flash vision ile çalışır
- Açıklama + etiket + özet çıkarır
- Wiki'ye kaydeder (`entities/ayla-analizleri.md`)

### 2. Görsel/İnfografik Üretimi
- Google genai SDK ile doğrudan bağlantı
- `from google import genai` → `genai.Client(api_key=...)`
- Model: `gemini-3.1-flash-image-preview`
- Çıktı: inline_data (bytes + mime_type)

### 3. Pipeline Entegrasyonu
- **Ekrem + İnfografik Pipeline** ile çalışır
- Ekrem tweet metni üretir → Ayla infografik oluşturur → X'e post edilir
- Pipeline: `scripts/hermes-infografik-pipeline.py`

## API Anahtarları

| Key | Değer | Durum |
|-----|-------|-------|
| Google AI Studio (frontmatter) | `AIzaSy...CwrI` | ❌ Geçersiz (çalışmıyor) |
| Google AI Studio (kod içi) | `AIzaSy...4zRI` | ❓ Bilinmiyor |
| Google AI Studio (güncel) | **KULLANICI'DAN BEKLENİYOR** | ⏳ |

## Kullanılan Skill Dosyası

- **Konum:** `/opt/data/scripts/skills/ayla-gorsel-ajani.md`
- **Sürüm:** v2 (son güncelleme: 23 Mayıs 2026)
- **Platform:** Linux
- **Bağımlılıklar:** `pip install google-genai`

## Kod Referansı

```python
from google import genai

client = genai.Client(api_key="AIzaSy...KEY")
response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents="Bir infografik oluştur..."
)

for part in response.candidates[0].content.parts:
    if part.inline_data:
        image_bytes = part.inline_data.data
        mime_type = part.inline_data.mime_type
```

## İnfografik Prompt Şablonu

```
Bir sosyal medya infografigi olustur. Konu: {topic}

Infografik su ozellikleri tasisin:
- Modern, minimalist tasarim
- Koyu arka plan (lacivert/siyah)
- Acik mavi ve beyaz renkler
- Metin icerigi: tweet'in ana fikrini ozetleyen 3-4 madde
- Profesyonel, yapay zeka temali goruntu
- 1200x675px oranina uygun (yatay)
```

## Analiz Arşivi

Ayla'nın analiz ettiği tüm görseller: [[ayla-analizleri]]

## İlgili Sayfalar

- [[ekrem-x-ajani]] — Tweet üretiminden sorumlu ajan
- [[ekrem-tweet-havuzu]] — Tweet konuları havuzu
- [[hermes-infografik-pipeline]] — Otomatik infografik pipeline
