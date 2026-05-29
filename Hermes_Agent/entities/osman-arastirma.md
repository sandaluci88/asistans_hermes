---
title: Osman — Araştırma Ajanı
tags: [osman, arastirma, web-search, trend, rapor]
date: 2026-05-23
status: active
brain: A
---

# Osman — Araştırma Ajanı 🔍

Osman, Botfusions AI Reklam Ajansı'nın internet araştırma ve raporlama ajanıdır.

## Görevi

- İnternette ve X'te (site:x.com ile) güncel trendleri, sektör haberlerini tarar
- DeepSeek Flash ile hızlı analiz yapar
- DeepSeek v4 Pro ile derinlemesine rapor yazar
- Ekrem'in tweet havuzunu doldurur
- Yayınlanan tweet'leri arşive kaydeder

## Rapor Formatı

Her rapor `reports/osman/YYYY-AA-GG-SSmm-tur.md` şeklinde kaydedilir.

- **gundem** — hızlı tarama, 5-7 başlık, tweet fikirleri
- **analiz** — derinlemesine, veri/istatistik ağırlıklı

## Tweet Fikirleri

Osman'ın ürettiği tweet fikirleri [[ekrem-tweet-havuzu]] sayfasına eklenir. Her fikir şunları içerir:
- Konu başlığı
- Kısa açıklama
- Potansiyel puanı (Yüksek/Orta)
- Öncelik (⭐ ile)

## Arşiv

Yayınlanan tweet'ler [[botfusions-x-tweet-arsivi]] sayfasına otomatik kaydedilir.

## Kullandığı Teknolojiler

- **web_search** — Hermes tool, internette gezinme
- **DeepSeek Flash** (`deepseek-chat`) — hızlı analiz
- **DeepSeek v4 Pro** (`deepseek-chat`) — derin raporlama

## İlgili Sayfalar

- [[ekrem-x-ajani]]
- [[ekrem-tweet-havuzu]]
- [[botfusions-x-tweet-arsivi]]
- Skill: `scripts/skills/osman-arastirma.md`
