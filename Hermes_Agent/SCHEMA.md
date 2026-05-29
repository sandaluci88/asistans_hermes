# Wiki Schema — Hermes Agent Vault

## Domain
Hermes Fleet yönetimi, AI agent orchestrasyonu, X/Twitter pazarlama, SEO/AEO, GitHub operasyonları, sistem yönetimi.

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `ekrem-x-ajani.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link between pages (minimum 2 outbound links per page)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`
- Dil: Türkçe (teknik terimler İngilizce kalabilir)

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | decision | comparison | query | synthesis
tags: [from taxonomy below]
sources: [raw/sources/source-name.md]
brain: A | B | AB
---
```

## Tag Taxonomy
- **Agent**: cron, skill, soul, container, fleet, orchestration
- **X/Twitter**: tweet, algoritma, engagement, trend, xurl, botfusions
- **Sistem**: linux, docker, vps, port, volume, healthcheck
- **AI/ML**: llm, model, api, token, fine-tune, inference
- **Pazarlama**: seo, aeo, cmo, reklam, icerik, strateji
- **GitHub**: repo, issue, pr, github-ops, botfusionss
- **Wiki**: ingest, query, lint, kaynak, ozet
- **Kisi**: user, agent, person

Rule: every tag on a page must appear in this taxonomy. If a new tag is needed,
add it here first, then use it.

## Page Thresholds
- **Create a page** when an entity/concept appears in 2+ sources OR is central to one source
- **Add to existing page** when a source mentions something already covered
- **DON'T create a page** for passing mentions
- **Split a page** when it exceeds ~200 lines
- **Archive a page** when content is fully superseded

## Update Policy
When new information conflicts with existing content:
1. Check the dates — newer sources generally supersede older ones
2. If genuinely contradictory, note both positions with dates and sources
3. Mark the contradiction in frontmatter
4. Flag for user review

## Klasor Yapisi
```
Hermes_Agent/
├── raw/sources/     → Ham kaynaklar, DOKUNULMAZ
├── raw/docs/        → Statik dokumanlar (mevcut SOUL.patch.md vs.)
├── sources/         → Her ham kaynak icin ozet sayfasi
├── entities/        → Agent'lar, servisler, kisiler
├── concepts/        → Soyut kavramlar
├── decisions/       → Kararlar (her karar = tek sayfa)
├── issues/          → Duzeltilen sorunlar
├── syntheses/       → Ust duzey genel bakis sayfalari
├── archive/         → Eskimis sayfalar
├── index.md         → Kategori bazli icerik katalogu
├── log.md           → Append-only zaman damgali olay kaydi
└── SCHEMA.md        → Bu dosya
```
