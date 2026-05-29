---
title: Hermes Router
tags: [router, orkestrasyon, api, faz-1]
date: 2026-05-26
status: active
brain: A
---

# Hermes Router

Faz 1 orkestrasyon servisi. Tek API giris noktasindan gelen mesaji intent detection ile dogru agent'a route eder. Agent health check loop ve SSE streaming destekler.

## Port

8699

## Endpoint'ler

- `POST /v1/route` — Intent detection (hangi agent'a gidecek?)
- `POST /v1/chat/completions` — Proxy mode (dogru agent'a forward + SSE streaming)
- `GET /health` — Router + tum agent'larin health durumu
- `X-Hermes-Agent` header — Manuel agent secimi

## Mimari

```
Kullanici -> Router (8699) -> Intent Detection -> Agent API -> Response
                    |
                    +-> Health Check Loop (30sn)
```

## Intent Detection

1. Keyword matching (hizli) — turkce karakter normalizasyonu
2. LLM fallback (OpenRouter/DeepSeek) — confidence < 0.3 oldugunda
3. Default: CMO (belirsiz mesajlar)

## Health Check Loop

Registry her 30 saniyede bir tum agent'larin `/health` endpoint'ini kontrol eder. Saglikli agent'lar arasinda secim yapar. Unhealthy agent otomatik olarak atlanir.

## Konfigürasyon

`config.yaml` uzerinden agent tanimlari (url, role, keywords), router ayarlari (port, health_check_interval, intent_confidence_threshold), LLM ayarlari.

## Deployment

- Docker konteyner (docker-compose.vps.yml)
- Traefik: router.turklawai.com
- Network: agency-net + coolify
- Environment: OPENROUTER_API_KEY (LLM fallback), HERMES_API_KEY (agent authentication)

## Related

- [[hermes-orchestrator-gelisim-plani]]
- [[hermes-agent]]
- [[hermes-api]]
