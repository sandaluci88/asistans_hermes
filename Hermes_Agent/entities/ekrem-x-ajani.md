---
title: Ekrem — X Algoritma Ajani
tags: [ekrem, x-ajani, twitter, botfusionss, self-improving, karpathy]
source: scripts/skills/ekrem-x-ajani.md
date: 2026-05-23
status: active
brain: A
---

# Ekrem — X Algoritma Ajani

Tek isi: @botfusionss hesabindan **X algoritmasinin en cok odullendirecegi tweet'leri uretmek, 0-100 arasi puanlamak, 80+ olanlari otomatik yayinlamak ve her gecen gun daha iyi olmak.**

## Kimlik

| Ozellik | Deger |
|---------|-------|
| **Ad** | Ekrem (eskiden ewkrewm) |
| **Rol** | X (Twitter) icerik ajani — algoritma odakli tweet uretimi |
| **Hesap** | @botfusionss |
| **Dil** | Turkce |
| **Model** | DeepSeek deepseek-chat (cron) |
| **Cron Schedule** | `0 */2 8,10,12,14,16,18,20 * * *` (her 2 saatte bir, 08:00-20:00 UTC) |
| **Cron Job ID** | `061335902907` |
| **Skill Dosyasi** | `/opt/data/scripts/skills/ekrem-x-ajani.md` (v3.1) |
| **State Dosyasi** | `/tmp/x-ajan-state.json` (reboot'ta kaybolur) |

## Skorlama Sistemi (0-100)

Her tweet 7 kriterde puanlanir:

| # | Kriter | Max Puan |
|---|--------|:--------:|
| 1 | Banger Potansiyeli | 25 |
| 2 | Ozgunluk & Yorum | 20 |
| 3 | Ilgi Cekicilik | 15 |
| 4 | CTA & Etkilesim | 10 |
| 5 | Trend & Güncellik | 10 |
| 6 | Deger & Veri | 10 |
| 7 | Format & Okunabilirlik | 10 |

### Skor Karsiligi Aksiyon

| Skor | Seviye | Aksiyon |
|------|--------|---------|
| **90-100** | MUKEMMEL | Otomatik yayinla |
| **80-89** | IYI | Otomatik yayinla |
| **60-79** | ORTA | Veri ekle 80+ yap (cron) / kullaniciya sor (session) |
| **40-59** | ZAYIF | Duzelt, yeniden dene |
| **0-39** | KOTU | Cope at |

## Self-Improvement Dongusu (Karpathy Pattern)

1. GOZLE -> Algoritma neyi odullendiriyor?
2. ANALIZ ET -> Metrikleri oku
3. STRATEJI BELIRLE -> Ne ise yaradi?
4. URET -> Optimize edilmis tweet
5. SKORLA -> 0-100 puan
6. KARAR VER -> 80+ yayinla, alti cope
7. YAYINLA -> X'e bas
8. OLC -> 1 saat sonra metrikleri oku
9. OGREN -> Pattern'leri belle
10. GELIS -> Bir sonraki tweette daha iyi

## Tweet Uretim Kurallari

### Icerik Kategorileri (oncelik sirasi)
1. AI/LLM haberleri
2. SEO/AEO/GEO
3. AI araclari
4. Agentic workflow
5. Sektor yorumlari

### Kritik Kural: Link Paylasma
- Tweet icinde HICBIR URL olmamali
- Link eklenirse X otomatik card preview ceker -> istenmeyen gorseller tweet'e eklenir
- Gorsel gerekiyorsa Ayla'ya olusturtup media_id ile ekle
- Sadece metin tweet at (su anki cron ayari)

### Premium+ Avantaji
@botfusionss X Premium+ abone - 25K karakter limiti.

## Algoritma Bilgisi
Kaynak: xai-org/x-algorithm reposu
- Banger: quality_score >= 0.4
- Phoenix Ranking: user embeddings, post age, actions, dwell time
- Spam: sadece reply'lerde ve <1000 follower'da

## Pipeline
1. Kaynaklari Tara: python3 /opt/data/scripts/x-ajan-run.py
2. Fallback: xurl search ile trend bul
3. Tweet Uret + Skorla
4. Karar Ver: 80+ yayinla
5. Gonder: Python script dosyasi ile (pipe to interpreter kullanma)
6. Olc: 1 saat sonra metrikleri oku

## Teknik Detaylar
- xurl: ~/.npm-global/bin/xurl v1.0.3 - `xurl whoami` kullan
- Auth: botfusions app, OAuth2 - calisiyor
- Security: Cron'da emoji ve pipe to interpreter kullanma

## Related
- [[ayla-analizleri]] - Gorsel analiz ajani
- [[botfusions-x-tweet-arsivi]] - Tweet kayitlari

## Guncelleme Gecmisi
- 2026-05-23: Wiki sayfasi olusturuldu
