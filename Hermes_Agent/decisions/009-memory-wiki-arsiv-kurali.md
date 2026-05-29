---
title: Memory → Wiki Arşiv Kuralı
tags: [memory, arşiv, kural]
date: 2026-05-26
status: active
brain: A
---

# Memory → Wiki Arşiv Kuralı

## Kural

**Yerel memory %80 dolduğunda:**

1. Mevcut tüm memory içeriğini `concepts/hermes-memory-arsivi.md` sayfasına append et
2. `zep_add_fact` ile Zep'e logla
3. Yerel memory'den sadece oturum için gerekli minimumu tut, gerisini sil
4. `index.md`'yi güncelle
5. `log.md`'ye **brain-arsiv** etiketiyle kayıt düş

## Bellek Hiyerarşisi

| Katman | Amaç | Süre |
|--------|------|------|
| **Zep Cloud** | Kalıcı cross-session bağlam, kararlar, tercihler | Kalıcı |
| **Wiki** | Öğrenme deposu, yapılandırılmış bilgi, arşiv, ajan dokümantasyonu | Kalıcı |
| **Yerel Memory** | Sadece bu oturumda hızlı erişim gereken bilgiler | Oturum, %80'de taşınır |

## Neden

- Zep'teki bilgiler dağınık, sadece ilişkisel grafik
- Wiki'deki bilgiler yapılandırılmış, insan ve LLM'in öğrenmesi için düzenli
- "Öğrenim için önemli" olan wiki'de olmalı
- Yerel memory şişince performans düşer, temiz tutmak gerek

## İlgili

- [[hermes-memory-arsivi]]
