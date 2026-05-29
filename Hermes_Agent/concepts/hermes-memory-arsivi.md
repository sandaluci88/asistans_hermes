---
title: Hermes Memory Arşivi
tags: [memory, arşiv, sistem-bilgisi]
date: 2026-05-29
status: active
brain: AB
---

# Hermes Memory Arşivi

Agent'in yerel memory'sinden wiki'ye taşınan kalıcı bilgiler.

## Memory Yönetim Kuralı (TAŞA KAZINMIŞ)

Memory %80 dolduğunda (1,760/2,200 chars), en az kullanılan/kritik olmayan bilgiler bu wiki sayfasına arşivlenir. Memory %95'i geçerse (2,090 chars) **acil arşiv** tetiklenir.

Oturum içi gerekli minimum bilgi memory'de tutulur, gerisi wiki'ye aktarılır.

## Model Sıralaması

| Sıra | Sağlayıcı | Model | Kullanım |
|------|-----------|-------|----------|
| 1. | DeepSeek | deepseek-v4-pro | **Default** — tüm işlemler |
| 2. | OpenRouter | google/gemini-3.5-flash | **Fallback** — DeepSeek düşerse |
| 3. | KIE.AI | claude-opus-4-7 | **Emergency** — sadece özel durumda |

**Not:** Vision/görsel okuma — DeepSeek desteklemez. Görsel analizi için OpenRouter üzerinden `google/gemini-3.5-flash` kullanılır.

## X/Twitter Hesabı

- **Hesap:** @botfusionss — Botfusions AI Reklam Ajansı
- **Plan:** X Premium+ (25.000 karakter limiti)
- **Kural:** KISA TWEET ATMA. 800-2000 karakter. Thread atma, show more = dwell time.
- **Auth:** xurl OAuth 1.0a ile VPS'te yapılandırıldı
- **Kullanıcı:** Ömer Cenk Tokgöz, @botfusionss

## Ajanlar

### Ekrem — Canlı X Ajanı
- **Görev:** Tweet at, like yap, retweet/RT yap, quote yap.
- **xurl yetenekleri:**
  - `xurl tweet "..."` — tweet at ✅
  - `xurl like <id>` — like at ✅
  - `xurl repost <id>` — retweet/RT ✅
  - `xurl quote <id> "..."` — quote yap ✅
  - `xurl reply <id> "..."` — ⚠️ mention'suz 403 verir (X API limiti)
- **Cron:** `0 3,6,9,12,15,18 * * *` (06:00-21:00 TSİ, 6 sefer)
- **Yorum formatı:** Türkçe yorum + altına İngilizce çeviri
- **Yorum havuzu:** Osman raporu + pipeline'dan gelen tweet'lere yorum yapar

### Ayla — Görsel Analiz + Oluşturma
- Model: `gemini-3.1-flash-image-preview` (Google AI Studio, genai SDK)
- Pipeline kendi Gemini API key'ini kullanır

### Osman — Araştırma Ajanı
- Cron: `0 3,10 * * *` (06:00/13:00 TSİ)
- Araçlar: Brave Search (ayda 2000 ücretsiz sorgu) + X Search (xAI/Grok 4.3) ile @shannholmberg, @swyx taraması
- Analiz: `moonshot-v1-auto` (BYOK) — Kimi K2.6 timeout sorunu nedeniyle değiştirildi
- Maliyet: ~$0.06/rapor
- Script: `/opt/data/scripts/osman_cron_runner.py`

## Pipeline Kuralları

| Durum | Yapılacak |
|-------|-----------|
| DeepSeek invalid → | template fallback |
| Gemini invalid → | FAL.ai fallback |
| timezone hatası → | fix |
| FLUX/FAL Türkçe metin → | Python Pillow ile elle çiz (okuyamaz) |
| Baoyu da | yasak |

## Saat Dilimi
Tüm zamanlar **TSİ** (Türkiye Saati, UTC+3). Asla UTC değil. Cron işlerinde TSİ → UTC dönüşümü otomatik yapılır.

## Kullanıcı Bilgisi
- **İsim:** Ömer Cenk Tokgöz
- **Email:** cenk.tokgoz@gmail.com
- **Tercih:** Türkçe iletişim, emir kipi değil işbirlikçi ton
- **Prensip:** "Her şey kendi içinde bir sistem"

## Related

- [[ekrem-x-ajani]]
- [[osman-arastirma-ajani]]
- [[ayla-gorsel-ajani]]

## Sources

- Hermes Agent Persona (sistem prompt'u)
- Oturum memory dump (29 May 2026)
