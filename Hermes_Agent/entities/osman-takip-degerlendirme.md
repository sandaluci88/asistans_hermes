---
title: Osman — Takip Hesabi Degerlendirme
tags: [osman, takip, degerlendirme, yorum, retweet, engagement]
date: 2026-05-30
status: active
brain: A
---

# Osman — Takip Hesabi Degerlendirme 🎯

Osman'in takip ettigi hesaplari taramasi, hangilerine **yorum** yapilacagini, hangilerine **retweet** (repost) yapilacagini belirlemesi ve Ekrem'e bildirmesi sureci.

## Takip Edilen Hesaplar (12)

| # | Hesap | Alan | Oncelik | Etkilesim Tipi |
|---|-------|------|:-------:|----------------|
| 1 | @karpathy | AI lider, ex-Tesla | Yuksek | Yorum + RT |
| 2 | @NousResearch | Acik kaynak AI | Yuksek | Yorum + RT |
| 3 | @shannholmberg | Pazarlama strateji | Orta | Yorum |
| 4 | @lilyraynyc | SEO/AEO uzmani | Yuksek | Yorum + RT |
| 5 | @nateherk | AI/pazarlama | Orta | Yorum |
| 6 | @iPullRank | SEO, teknikal | Yuksek | Yorum + RT |
| 7 | @alexgroberman | AI search, GEO | Yuksek | Yorum + RT |
| 8 | @AnthropicAI | Claude, AI guvenlik | Yuksek | RT |
| 9 | @OpenAI | GPT, AI haberleri | Yuksek | RT |
| 10 | @GoogleDeepMind | Gemini, AI arastirma | Orta | RT |
| 11 | @Kevin_Indig | SEO, buyume | Yuksek | Yorum + RT |
| 12 | @ModestMitkus | AI ajans, kucuk isletme | Yuksek | Yorum + RT |

## Degerlendirme Kriterleri

Her hesabin son tweet'leri su kriterlere gore degerlendirilir:

### Yorum Yapilacak Tweet Kriterleri
1. **Dusunce uyandiran** — Bir iddia, soru veya gorus iceren tweet
2. **Sektor yorumu yapilabilir** — AI, SEO, pazarlama, GEO ile ilgili
3. **Botfusions pozisyonuna uygun** — dijital calisan, AI ajani baglantisi kurulabilir
4. **280 karakter limiti** — Kisa, oz, Turkce yorum
5. **SamanlikDegil** — Spam ya da promosyon tweet degil

### Retweet Yapilacak Tweet Kriterleri
1. **Onemli haber** — Yeni model lansmani, API degisikligi, sektor buyuklugu
2. **Veri/istatistik paylasimi** — AI pazar buyuklugu, adoption oranlari, trend verileri
3. **Ozgul bulgu** — Benchmark sonuclari, arastirma raporu, case study
4. **Topluluk onemi** — Cok fazla etkilesim alan, sektorde yanki uyandiran

### Atlanacak Tweet'ler
1. Promosyon/satis tweet'leri
2. Kisisel/paylasim tweet'leri (sektor disi)
3. Cok teknik detay (sadece uzmanlik gerektiren)
4. Zamanlari gecmis olaylar (1 gunden eski)
5. Politika/rahatsiz edici icerik

## Degerlendirme Sonuc Formatı

Her degerlendirme sonucu [[ekrem-yorum-hazir]] dosyasina yazilir:

### Yorum Formati
```
### Yorum N: @hesap — Konu basligi
**Tweet:** TWEET_ID — "Tweet ozeti (ilk 100 karakter)"
**Yorum:** [Turkce, max 280 karakter, kibar, sektor odakli]
**Durum:** Bekliyor
```

### Retweet Formati
```
### RT N: @hesap — Konu basligi
**Tweet:** TWEET_ID
**Neden RT:** [1 cumle ile neden degerli]
**Durum:** Bekliyor
```

## Pipeline Akisi

```
Osman Tarar (09:00)
  ↓
Takip hesaplarini tara (xurl search from:hesap -n 3)
  ↓
Her tweet'i degerlendir
  ├── Yorum uygun → [[ekrem-yorum-hazir]] dosyasina yaz
  ├── RT uygun → [[ekrem-yorum-hazir]] dosyasina isaretle
  └── Atla → gec
  ↓
Ekrem'e bildir
  ↓
Ekrem cron (her 2 saat) → Yorumlari gonder + RT yap
```

## Cron Entegrasyonu

| Adim | Sorumlu | Zaman | Islem |
|------|---------|-------|-------|
| 1 | Osman | 09:00 | Takip hesaplarini tara + degerlendir |
| 2 | Osman | 09:15 | Sonuclari wiki'ye yaz |
| 3 | Ekrem | Her 2 saat | Yorumlari gonder + RT yap |
| 4 | Ekrem | Her 2 saat | Yapilan islemleri isaretle |

## Yorum Yazma Kurallari

1. **Turkce olmali** — Yorumlar her zaman Turkce
2. **280 karakter** — X karakter limiti asilmamali
3. **Kibar ve yapici** — Savusturucu degil, tamamlayici ton
4. **Sektor odakli** — AI, SEO, pazarlama, GEO ile ilgili
5. **Botfugins pozisyonu** — Gerektiginde "AI ajani", "dijital calisan" teması
6. **Ozgul** — Kopya yorum degil, her tweet'e ozel
7. **Soru sorma** — Yorumlarda soru bitirmek etkilesimi artirir
8. **Emoji kullan** — 1-2 emoji yorumu canli tutar

## Ornek Degerlendirmeler

### Ornek 1: Yorum Yapilacak
> @karpathy: "AI agents will replace most SaaS workflows by 2027"
> **Degerlendirme:** Yorum yap — Botfussions pozisyonu ile dogrudan ilgili
> **Yorum:** "2027'ye kadar bekleme geregi yok. Biz su an ajanslara AI ajan kuruyoruz, 48 saatte devreye aliyoruz. SaaS'in yerine otomatik workflow geciyor. 🤖"

### Ornek 2: RT Yapilacak
> @AnthropicAI: "Claude 4.6 is now available with improved coding capabilities"
> **Degerlendirme:** RT yap — Onemli model lansmani
> **Neden RT:** Yeni model lansmani, sektorde buyuk yanki

### Ornek 3: Atlanacak
> @nateherk: "Great coffee this morning ☕"
> **Degerlendirme:** Atla — Sektor iliskisi yok

## Haftalik Degerlendirme Raporu

Her hafta Pazartesi Osman su raporu uretir:

| Metrik | Hedef | Gerceklesen |
|--------|:-----:|:-----------:|
| Taradigi hesap sayisi | 12 | - |
| Yorum yapilan tweet | 5-10 | - |
| RT yapilan tweet | 3-5 | - |
| Atlanan tweet | - | - |
| Yorumlara gelen yanit | 2+ | - |
| RT'lerin ortalama etkilesim | 50+ | - |

## Ilgili Sayfalar

- [[ekrem-x-ajani]] — Tweet uretimi ve yayinlama
- [[ekrem-x-agent-cron-workflow]] — Cron is akisi
- [[ekrem-yorum-hazir]] — Yorum taslaklari
- [[osman-arastirma]] — Osman'in arastirma sureci
- [[ekrem-tweet-havuzu]] — Tweet fikirleri
- [[botfusions-x-tweet-arsivi]] — Yayinlanan tweet kayitlari
