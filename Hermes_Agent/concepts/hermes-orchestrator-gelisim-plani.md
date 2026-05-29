---
title: Hermes Orchestrator Gelistirme Plani
tags: [mimari, orkestrasyon, fleet, gelisim-plani, master-plan]
date: 2026-05-26
status: active
brain: B
---

# Hermes Orchestrator — Gelistirme Plani (Master)

## Vizyon

Hermes bir orkestrator olarak calisir. Kullanici tek bir noktadan talimat verir, Hermes dogru uzmana route eder, uzman calisir, Hermes raporlar.

```
Sen → Hermes → Route → Specialist → Execute → Rapor
```

## Iki Tur Specialist Agent

### Open Specialists (Dinamik)
Esnek, etkilesimli agent'lar. Back-and-forth, yon degistirme:
- Coding Agent (Claude Code / Codex)
- Research Agent
- Creative Agent
- Content Agent

### Closed Specialists (End-to-End, Tekrarlanabilir)
Repeatable workflow'lar. Her seferinde ayni isi ayni sekilde yaparlar:
- SEO makale workflow
- Haftalik rakip arastirma raporu
- Landing page QA
- Aylik analytics ozeti
- Content repurposing pipeline
- Lead list enrichment
- PR review / bug-fix workflow

### Graduation Kurali
> Open specialist'ler zamanla closed'a graduation yapar.
> Bir surece dinamik calisirsin, shape'i bulursun, sonra repeatable agent olarak kilitlersin.

---

## Mevcut Fleet Envantteri

| Agent | Port | Tur | Model | Durum |
|---|---|---|---|---|
| hermes-cmo | 8642 | Open | deepseek-v4-pro | Aktif |
| hermes-seo | 8643 | Open | deepseek-v4-pro | Aktif |
| hermes-ops | 8644 | Open | deepseek-v4-pro | Aktif |
| hermes-life | 8645 | Open | deepseek-v4-pro | Aktif (karar bekle) |
| jale | 8646 | Open | deepseek-v4-pro | Aktif |
| hermes-ads | 8648 | — | — | SOUL hazir, konteyner yok |

## Mevcut Guclu Yonler

- Container izolasyonu (her agent ayri)
- Her agent ayri SOUL.md
- VPS deployment 7/24
- Dashboard + API server
- Wiki (ikinci beyin) + 2 yonlu GitHub sync
- Telegram entegrasyonu (CMO + Jale)
- Maestro (lokal kurulu)
- Browser Use (zaten var)
- Firecrawl (Osman raporlarinda kullanimda)

---

## GELISIM YOL HARITASI

### FAZ 1 — Temel Routing (1-2 hafta)
**Hedef**: Kullanici "fix the landing page" dediginde dogru agent'a gitsin

| Gorev | Aciklama | Oncelik |
|---|---|---|
| Orkestrator API endpoint | `/v1/route` — intent detection ile agent secimi | Yuksek |
| Intent detection mekanizmasi | Kullanici mesajindan tur olusturma (coding/seo/ops/creative/research) | Yuksek |
| Telegram router | Tek bot → cok agent routing | Yuksek |
| Route tablosu | Mesaj turu → agent eslestirme matrisi | Orta |

### FAZ 2 — Closed Workflows (2-3 hafta)
**Hedef**: Repeatable pipeline'lar, cron ile otomatik calisan isler

| Gorev | Aciklama | Oncelik |
|---|---|---|
| Workflow sablon formati | YAML-based workflow tanimi (trigger, steps, done_criteria) | Yuksek |
| Ilk closed workflow: SEO raporu | Keyword ara → rakip analiz → rapor olustur → wiki'ye kaydet | Yuksek |
| Ikinci workflow: Analytics ozeti | Haftalik metrik toplama → ozet → Telegram bildirim | Orta |
| Ucuncu workflow: Gundem raporu | Firecrawl + DeepSeek ile gundem tarama (Osman zaten yapiyor, closed'a cevir) | Orta |
| Dogal dil cron scheduler | "Her sabah 7'de X yap" formatinda zamanlama | Orta |
| Maestro VPS aktivasyonu | Cron + task tracking aktif et | Yuksek |

### FAZ 3 — Orkestrasyon (3-4 hafta)
**Hedef**: Agent-arasi iletisim, graduation, guvenlik

| Gorev | Aciklama | Oncelik |
|---|---|---|
| Agent-arasi iletisim | `delegate_task` — API uzerinden gorev delegasyonu | Yuksek |
| Subagent spawn | Paralel gorev execution | Orta |
| Graduation mekanizmasi | Open → closed gecis algilama + otomasyon | Orta |
| Agent Camel guvenlik | CaMeL guard, trust boundaries | Dusuk |
| HCI dashboard | Tamamlayici yonetim paneli | Dusuk |

### FAZ 4 — Otonomi (4-6 hafta)
**Hedef**: Self-improving, skill evolution, otomatik ogrenme

| Gorev | Aciklama | Oncelik |
|---|---|---|
| Self-improvement dongusu | Agent'lar kendi hatalarindan ogrenme | Yuksek |
| Skill Factory (VPS) | Tekrarlanan pattern'lerden otomatik skill olusturma | Yuksek |
| Honcho user modeling | Otomatik pattern recognition + persistent user model | Orta |
| agentskills.io entegrasyonu | Skill hub'dan cekme + paylasma | Orta |
| Otomatik graduation algilama | Dinamik → repeatable gecisi otomatik tespit | Dusuk |
| Performance tracking | Agent performans metrikleri + optimizasyon | Dusuk |

### FAZ 5 — Kanal Genisleme (6-8 hafta)
**Hedef**: Coklu kanal, voice, mobil erisim

| Gorev | Aciklama | Oncelik |
|---|---|---|
| Discord entegrasyonu | Messaging gateway genisleme | Orta |
| Slack entegrasyonu | Messaging gateway genisleme | Orta |
| WhatsApp entegrasyonu | Messaging gateway genisleme | Dusuk |
| Voice note destegi | Telefon → agent → islem | Dusuk |
| Email entegrasyonu | E-posta uzerinden agent erisimi | Dusuk |

---

## ARASTARMA KAYNAKLARI

### Kaynak 1: Kullanici Tanimi — "Open/Closed Specialist Agents"
- **Tarih**: 2026-05-26
- **Bulgular**: Open vs Closed agent ayrimi. Graduation kavrami. Orkestrator mental modeli.
- **Etki**: Faz 1-3 tamamini sekillendirdi

### Kaynak 2: Akshay Pachaar Masterclass (X Thread)
- **Tarih**: 2026-05-23
- **Bulgular**: 3-katmanli bellek, Skill Hub (687 skill), Curator, delegate_task, GEPA optimizasyonu
- **Etki**: Faz 4 skill hub + self-improvement

### Kaynak 3: Nainsi Dwivedi — "The AI Agent That Learns From You" (X Article)
- **Tarih**: 2026-05-26
- **URL**: https://x.com/NainsiDwiv50980/status/2059191739815281042
- **Bulgular**: Honcho dialectic user modeling, agentskills.io, dogal dil cron, subagent spawn, 10+ model provider, 40+ built-in tools, 3-katmanli bellek
- **Etki**: Faz 2 cron, Faz 3 subagent, Faz 4 Honcho + agentskills.io, Faz 5 kanal

### Kaynak 4: KanikaBK — "Obsidian Vault Goldmine" (X Tweet)
- **Tarih**: 2026-05-26
- **URL**: https://x.com/KanikaBK/status/2059196910448320670
- **Bulgular**: Obsidian + LM Studio + Local LLM. Smart Connections (semantic search), BMO Chatbot, Mini-RAG. Gizlilik argumani hakli.
- **Etki**: Dusuk oncelik — semantic search ve local fallback ileride degerlendirilecek

### Kaynak 5: Web Scraping Araclari Degerlendirmesi
- **Tarih**: 2026-05-26
- **Eklenen araclar**:
  - **Crawl4AI** — LLM-native crawler, Markdown cikti, wiki INGEST icin. `pip install crawl4ai`. Faz 2'ye eklendi.
  - **Scrapegraph AI** — LLM + graph-based scraping, rakip analizi + SEO verisi icin. Faz 3'e eklendi.
- **Zaten var olanlar**: Firecrawl (Osman), Browser Use (Hermes built-in), Playwright (agent-browser)
- **Atlananlar**: Scrapy (low-level), Crawlee (Node.js), Katana (guvenlik), Maxun (degerlendir)

---

## ARASTIRMA BEKLEYEN KONULAR

> Bunlar arastirilip plana eklenecek:

1. **Intent Detection Yontemleri** — Kullanici niyetini anlamanin en iyi yolu
2. **Workflow Engine Secenekleri** — Closed workflow'lar icin motor/format
3. **Multi-Agent Communication** — Agent-arasi gorev delegasyonu protokolleri
4. **Graduation Patterns** — Open → closed gecis mekanizmasi ornekleri
5. **Honcho Dialectic User Modeling** — Otomatik kullanici modeli olusturma
6. **agentskills.io Protocol** — Skill paylasim standardi
7. **Crawl4AI Hermes Entegrasyonu** — Web → Markdown → Wiki INGEST pipeline
8. **Scrapegraph AI SEO Kullanimi** — Rakip analizi otomasyonu

---

## Related

- [[project-fleet-specialists]]
- [[project-control-room]]
- [[project-orchestration-tools]]
- [[project-yapilacaklar]]
