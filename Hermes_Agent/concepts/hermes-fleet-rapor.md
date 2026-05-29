# Hermes Fleet — Kurulum ve Mimari Raporu

> Tarih: 27 Mayıs 2026
> Proje: AI Reklam Ajansı Otomasyon Sistemi
> Durum: Faz 1, 2, 2A, 3 Tamamlandı — Production'da Aktif

---

## 1. Sistem Ne Yapar?

Hermes Fleet, **birden fazla AI agent'ını koordine eden tam otomatik bir AI operasyon sistemi**dir. Tek Telegram bot'u üzerinden 5 farklı uzman agent'e erişim sağlar, görev dağıtır, çıktıları değerlendirir, insan onayı alır ve sonuçları kaydeder.

```
Kullanıcı (Telegram)
    ↓
@bilmis1_bot (Router)
    ↓ Intent Detection
    ↓
┌─────┬─────┬─────┬──────┬──────┐
│ CMO │ SEO │ OPS │ Life │ Jale │
└─────┴─────┴─────┴──────┴──────┘
    ↓ Evaluator (Jale)
    ↓ Human Approval (Telegram)
    ↓ Memory + Maestro Kayıt
    Sonuç
```

---

## 2. Fazlar ve Bileşenler

### Faz 1 — API Router (Tamamlandı)

**Ne yaptı:** Gelen mesajı otomatik olarak doğru agent'e yönlendiren API routing servisi.

| Bileşen | Dosya | İşlev |
|---------|-------|-------|
| Router API | `hermes-router/router.py` | FastAPI ana uygulama, port 8699 |
| Intent Detection | `hermes-router/intent.py` | Keyword matching + LLM fallback ile agent seçimi |
| Agent Registry | `hermes-router/agents.py` | 5 agent health check (30sn döngü), durum takibi |
| Config | `hermes-router/config.yaml` | Agent tanımları, keyword'ler, route tablosu |

**Endpoint'ler:**
- `GET /health` — Router + tüm agent sağlık durumu
- `POST /v1/route` — Intent detection (hangi agent, güven skoru)
- `POST /v1/chat/completions` — OpenAI-compatible proxy + SSE streaming

**Nasıl çalışır:**
1. Kullanıcı mesaj gönderir
2. Keyword matching ile hızlı agent tespiti (Türkçe karakter normalizasyonu)
3. Güven skoru < 0.3 ise LLM fallback (DeepSeek)
4. Belirsiz mesajlar → CMO (varsayılan)
5. Manuel seçim: `X-Hermes-Agent` header ile override

---

### Faz 2 — Kapalı İş Akışları (Tamamlandı)

**Ne yaptı:** Tekrarlanan iş akışlarını otomatikleştiren workflow engine + cron scheduler + Telegram router.

#### 2.1 Workflow Engine

| Bileşen | Dosya | İşlev |
|---------|-------|-------|
| Engine | `hermes-router/workflows/engine.py` | YAML template çalıştırıcı, adım zinciri |
| Modeller | `hermes-router/workflows/models.py` | Workflow, Step, EvaluationResult modelleri |
| Evaluator | `hermes-router/workflows/evaluator.py` | Jale kalite kontrol (PASS/REVISION/FAIL) |
| Maestro Bridge | `hermes-router/workflows/maestro_bridge.py` | Workflow → Maestro mission/task/evidence |
| Template'ler | `hermes-router/workflows/templates/` | seo-report.yaml, analytics-report.yaml, gundem-scan.yaml |

**Nasıl çalışır:**
```
Workflow başlat
  → Maestro mission oluştur
  → Step 1: Agent'e gönder (execute)
  → Step 2: Jale değerlendir (evaluate)
    → PASS: devam
    → REVISION: tekrar çalıştır (max 3 deneme)
    → FAIL: workflow durdur
  → Step 3: İnsan onayı (human_approval)
    → Telegram inline keyboard
  → Maestro ship
```

**Template formatı:**
```yaml
name: seo-report
params: [topic, keywords]
steps:
  - agent: seo
    type: execute
    prompt: "{{topic}} için anahtar kelime araştırması yap"

  - agent: jale
    type: evaluate
    criteria: [accuracy, completeness, hallucination]
    min_confidence: 0.7

  - type: human_approval
    message: "Rapor hazır. Onaylıyor musunuz?"
```

#### 2.2 Cron Scheduler

| Bileşen | Dosya | İşlev |
|---------|-------|-------|
| Parser | `hermes-router/scheduler/parser.py` | Türkçe zaman ifadesi → cron |
| Manager | `hermes-router/scheduler/manager.py` | APScheduler, İstanbul timezone |
| Routes | `hermes-router/scheduler/routes.py` | `/v1/schedule/*` endpoint'leri |

**Desteklenen Türkçe ifadeler:**

| İfade | Cron | Anlam |
|-------|------|-------|
| Her sabah 7'de | `0 7 * * *` | Günlük |
| Her pazar 10'da | `0 10 * * 0` | Haftalık |
| Her ayın 1'inde | `0 0 1 * *` | Aylık |
| Her 30 dakikada bir | `*/30 * * * *` | Interval |
| Hafta içi 9'da | `0 9 * * 1-5` | İş günü |
| Her gün 12 ve 18'de | `0 12,18 * * *` | Çoklu saat |

#### 2.3 Telegram Router

| Bileşen | Dosya | İşlev |
|---------|-------|-------|
| Bot | `hermes-router/telegram_bot.py` | @bilmis1_bot, polling mode |
| Approval | `hermes-router/approval.py` | İnsan onay yönetimi |

**Bot komutları:**
- `/start`, `/help` — Bilgi
- `/cmo`, `/seo`, `/ops`, `/life`, `/jale` — Manuel agent seçimi (kalıcı)
- `/reset` — Varsayılan agent'a dön
- Normal mesaj → Otomatik intent detection

**Onay mekanizması:**
```
Workflow çıktısı → Telegram mesajı
  [✅ Onayla]  [🔄 Düzelt]  [❌ Reddet]
Onayla → workflow devam eder
Düzelt → agent'e geri gönderilir
Reddet → workflow durdurulur
```

---

### Faz 2A — Uzman Tavsiyeleri (Tamamlandı)

**Ne yaptı:** Dışarıdan alınan uzman tavsiyeleri doğrultusunda temel eksiklikler giderildi.

#### 2A.1 Memory Altyapısı

| Bileşen | Dosya | İşlev |
|---------|-------|-------|
| Modeller | `hermes-router/memory/models.py` | Lesson, Failure, WorkflowState |
| Storage | `hermes-router/memory/store.py` | File-based JSON CRUD |
| Routes | `hermes-router/memory/routes.py` | `/v1/memory/*` endpoint'leri |

**Nasıl çalışır:**
```
lesson.json  → Öğrenilmiş deneyimler (problem → çözüm → bir dahaki sefere)
failures.json → Hata kayıtları (agent, hata tipi, mesaj, çözüm)
state/{workflow}.json → Workflow durum takibi (hangi adımda, ne çıktı)
```

**Endpoint'ler:**
- `GET/POST /v1/memory/lessons` — Öğrenilen dersler
- `GET/POST /v1/memory/failures` — Hata kayıtları
- `GET/PUT /v1/memory/state/{workflow}` — Workflow durumu

#### 2A.2 Evaluator Katmanı

| Bileşen | Dosya | İşlev |
|---------|-------|-------|
| Evaluator | `hermes-router/workflows/evaluator.py` | Jale'ye gönderir, kalite kontrol |
| Models güncelleme | `hermes-router/workflows/models.py` | EvaluationResult modeli |

**Değerlendirme kriterleri:**
1. **Doğruluk (Accuracy):** Bilgiler doğru mu?
2. **Tamlık (Completeness):** Görev tamamlanmış mı?
3. **Tutarlılık (Consistency):** Çıktı tutarlı mı?
4. **Halüsinasyon kontrolü:** Uydurma bilgi var mı?

**Sonuçlar:**
- PASS → Sonraki adıma geç
- REVISION → Agent'e geri gönder (max 3 deneme)
- FAIL → Workflow'u durdur

#### 2A.3 Retrieval Pipeline

| Bileşen | Dosya | İşlev |
|---------|-------|-------|
| Pipeline | `hermes-router/retrieval.py` | 5 kademeli öncelikli bilgi erişimi |

**Öncelik sırası:**
```
1. state.json       → Aktif workflow durumu (en hızlı)
2. short.md         → Hızlı bağlam notları
3. lessons.json     → Öğrenilmiş deneyimler (benzer durum arama)
4. Zep Cloud        → Uzun dönem hafıza (semantik search)
5. Autosearch       → Web araması (son çare, en pahalı)
```

#### 2A.4 Agent Sorumluluk Ayrımı

Her agent'ın net tanımlanmış yetkinlikleri:

| Agent | Rol | Capabilities |
|-------|-----|-------------|
| CMO | Araştırma + Strateji | research, strategy, analytics, campaign, budget |
| SEO | SEO Uzmanı | keyword, backlink, technical_seo, content_seo |
| OPS | DevOps + Altyapı | deploy, monitor, security, docker, backup |
| Life | Yaşam Koçu | health, wellness, motivation, habit, balance |
| Jale | Koordinatör + Evaluator | coordinate, evaluate, approve, memory, quality_control |

---

### Faz 3 — Orkestrasyon (Tamamlandı)

**Ne yaptı:** Tam otomatik orkestrasyon sistemi — Maestro entegrasyonu, güvenlik katmanı, agent-arası iletişim, fleet kontrol paneli.

#### 3.1 Maestro Bridge

| Bileşen | Dosya | İşlev |
|---------|-------|-------|
| Bridge | `hermes-router/workflows/maestro_bridge.py` | Maestro lifecycle yönetimi |

**Nasıl çalışır:**
```
Her workflow çalıştığında:
1. Maestro mission oluştur (pln-xxx)
2. Her adım için Maestro task oluştur (tsk-xxx)
3. Task durumları: draft → claimed → doing → shipped
4. Her adımdan sonra evidence kaydet (evd-xxx)
5. Evaluation sonucu → verifier evidence
6. Workflow tamamlandığında → mission ship
```

**Evidence türleri:** command, verifier, plan-check, review-ack, runtime-signal

#### 3.2 CaMeL Guard (Güvenlik)

| Bileşen | Dosya | İşlev |
|---------|-------|-------|
| Guard | `hermes-router/camel.py` | Trust boundaries, access matrix |

**3 güven seviyesi:**
```
FULL      → CMO, Jale (tüm agent'lere erişim)
STANDARD  → SEO, OPS (sınırlı erişim)
RESTRICTED → Life (sadece Jale'ye erişim)
```

**Access matrix (hangi agent nereye erişebilir):**
```
CMO  → SEO, OPS, Jale
SEO  → CMO, Jale
OPS  → CMO, Jale, SEO
Jale → CMO, SEO, OPS, Life (koordinatör = herkese)
Life → Jale (sadece koordinatör)
```

**Kontrol noktaları:**
- `check_permission()` → Agent erişim izni
- `validate_delegation()` → Görev delegasyonu doğrulama
- `sanitize_output()` → API key, token vb. filtreleme

#### 3.3 Agent-Arası İletişim (Delegation)

| Bileşen | Dosya | İşlev |
|---------|-------|-------|
| Manager | `hermes-router/delegation.py` | Görev delegasyonu + broadcast |

**Nasıl çalışır:**
```
Agent A, Agent B'ye görev devreder:
1. CamelGuard ile izin kontrolü
2. Hedef agent'e HTTP POST (120sn timeout)
3. Sonuç kaydedilir (başarı/başarısızlık)
4. Response döndürülür
```

**Endpoint'ler:**
- `POST /v1/delegate` — Agent-arası görev gönderimi
- `POST /v1/broadcast` — Birden fazla agent'e aynı görev
- `GET /v1/agents/{name}/status` — Tek agent durum sorgulama

#### 3.4 HCI Dashboard

| Bileşen | Dosya | İşlev |
|---------|-------|-------|
| API | `hermes-router/hci.py` | Fleet kontrol paneli endpoint'leri |

**Endpoint'ler:**
```
GET /v1/fleet/status     → Genel durum (kaç agent, kaç healthy, kaç onay bekliyor)
GET /v1/fleet/agents     → Agent listesi + capabilities + trust level
GET /v1/fleet/workflows  → Aktif workflow'lar + adım durumu
GET /v1/fleet/approvals  → Bekleyen insan onayları
GET /v1/fleet/lessons    → Son öğrenilen dersler
GET /v1/fleet/metrics    → Sistem metrikleri
```

---

## 3. Teknik Mimari

### 3.1 Altyapı

| Bileşen | Detay |
|---------|-------|
| **VPS** | 5.182.33.26, Ubuntu 22.04 LTS |
| **Orkestrasyon** | Coolify + Docker Compose |
| **Domain** | turklawai.com + alt domain'ler (Traefik, SSL) |
| **Ağ** | agency-net (internal) + coolify (external) |

### 3.2 Docker Servisleri (11 konteyner)

| Servis | Port | İşlev |
|--------|------|-------|
| hermes-router | 8699 | API router, workflow engine, tüm endpoint'ler |
| hermes (CMO) | 8642 | Marketing strateji agent |
| hermes-seo | 8643 | SEO uzman agent |
| hermes-ops | 8644 | DevOps agent |
| hermes-life | 8645 | Yaşam koçu agent |
| jale | 8646 | Koordinatör + evaluator agent |
| hermes-dashboard | 9119 | Web yönetim paneli |
| paperclip | 3100 | Organizasyon yönetimi |
| bridge | 8766 | Hermes ↔ Paperclip entegrasyonu |
| postgres | 5432 | Veritabanı |
| cmo-dashboard | 8765 | CMO operasyon paneli |

### 3.3 Model Politikası

| Agent | Model | Sağlayıcı |
|-------|-------|-----------|
| CMO | deepseek-v4-pro | DeepSeek |
| CMO (Ayla) | gemini-3.1-flash-image-preview | Google |
| Jale/SEO/OPS/Life | deepseek-v4-pro | DeepSeek |

**Kural:** Anthropic (Opus/Sonnet) kullanıcı söylemedikçe YASAK.

### 3.4 Veri Saklama

| Veri | Konum | Format |
|------|-------|--------|
| Agent skills | `/opt/data/skills/` | Markdown |
| Wiki / Vault | `/opt/data/wiki/` | Markdown |
| Memory | `/opt/data/wiki/memory/` | JSON |
| Maestro missions | `/opt/data/.maestro/missions/` | JSON |
| Maestro tasks | `/opt/data/.maestro/tasks/` | JSON |
| Maestro evidence | `/opt/data/.maestro/evidence/` | JSON |
| Agent data | Docker volumes | Persistent |

---

## 4. Tam Endpoint Listesi

### Router
| Method | Endpoint | İşlev |
|--------|----------|-------|
| GET | `/health` | Router + agent sağlık durumu |
| POST | `/v1/route` | Intent detection |
| POST | `/v1/chat/completions` | OpenAI-compatible chat proxy |

### Workflow
| Method | Endpoint | İşlev |
|--------|----------|-------|
| GET | `/v1/workflows` | Workflow listesi |
| POST | `/v1/workflows/{name}/run` | Workflow çalıştır |
| GET | `/v1/workflows/{name}/status` | Workflow durumu |

### Scheduler
| Method | Endpoint | İşlev |
|--------|----------|-------|
| POST | `/v1/schedule` | Türkçe NLP ile cron oluştur |
| GET | `/v1/schedule` | Tüm cron job'lar |
| GET/DELETE | `/v1/schedule/{id}` | Tekil job işlemleri |
| POST | `/v1/schedule/{id}/pause` | Duraklat |
| POST | `/v1/schedule/{id}/resume` | Devam ettir |

### Memory
| Method | Endpoint | İşlev |
|--------|----------|-------|
| GET/POST | `/v1/memory/lessons` | Öğrenilen dersler |
| GET/POST | `/v1/memory/failures` | Hata kayıtları |
| GET/PUT | `/v1/memory/state/{workflow}` | Workflow durumu |

### Delegation
| Method | Endpoint | İşlev |
|--------|----------|-------|
| POST | `/v1/delegate` | Agent-arası görev |
| POST | `/v1/broadcast` | Multi-agent broadcast |
| GET | `/v1/agents/{name}/status` | Agent durum sorgula |

### Fleet Dashboard
| Method | Endpoint | İşlev |
|--------|----------|-------|
| GET | `/v1/fleet/status` | Genel fleet durumu |
| GET | `/v1/fleet/agents` | Agent listesi + detaylar |
| GET | `/v1/fleet/workflows` | Aktif workflow'lar |
| GET | `/v1/fleet/approvals` | Bekleyen onaylar |
| GET | `/v1/fleet/lessons` | Son dersler |
| GET | `/v1/fleet/metrics` | Sistem metrikleri |

---

## 5. Yeni Müşteri Kurulum Rehberi

### 5.1 Gereksinimler

```bash
# VPS minimum
Ubuntu 22.04 LTS
4GB RAM
50GB SSD
Docker + Docker Compose

# API Anahtarları
OPENROUTER_API_KEY=sk-or-...     # LLM erişimi
TELEGRAM_BOT_TOKEN=...           # Telegram bot
JWT_SECRET=$(openssl rand -hex 32)
POSTGRES_PASSWORD=...
```

### 5.2 Kurulum Adımları

```bash
# 1. Repo'yu klonla
git clone <repo-url> /data/coolify/services/<musteri>
cd /data/coolify/services/<musteri>

# 2. Submodule'leri yükle
git submodule update --init --recursive

# 3. .env dosyası oluştur
cp .env.example .env
# API anahtarlarını gir

# 4. Docker'ı başlat
docker compose -f docker-compose.vps.yml up -d

# 5. Sağlık kontrolü
docker exec hermes-router python3 -c \
  "import urllib.request; print(urllib.request.urlopen('http://localhost:8699/health').read().decode())"
```

### 5.3 Müşteri Özelleştirme

**Yeni agent eklemek için:**

1. `hermes-router/config.yaml`'a yeni agent ekle:
```yaml
agents:
  yeni-agent:
    url: "http://yeni-agent:8650"
    role: "Açıklama"
    capabilities: ["cap1", "cap2"]
    keywords: ["anahtar", "kelimeler"]
```

2. `docker-compose.vps.yml`'e yeni servis ekle:
```yaml
  yeni-agent:
    build: ./agency
    environment:
      - PORT=8650
      - SOUL_PATH=/opt/data/souls/yeni-agent.md
```

3. `camel.py`'de access matrix'e ekle
4. Build + recreate: `docker compose build && docker compose up -d`

**Yeni workflow template'i:**

`hermes-router/workflows/templates/yeni-is.yaml` oluştur:
```yaml
name: yeni-is
description: "Açıklama"
params: [param1, param2]
steps:
  - agent: cmo
    type: execute
    prompt: "{{param1}} hakkında araştırma yap"
    output_key: arastirma

  - agent: jale
    type: evaluate
    criteria: [accuracy, completeness]

  - type: human_approval
    message: "Sonuç hazır. Onaylıyor musunuz?"
```

### 5.4 Traefik Domain Eşleştirme

Her agent için alt domain:
```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.yeni-agent.rule=Host(`yeni-agent.musteri.com`)"
  - "traefik.http.services.yeni-agent.loadbalancer.server.port=8650"
```

---

## 6. Operasyonel Runbook

### Servis Yeniden Başlatma
```bash
cd /data/coolify/services/<musteri>
docker compose -f docker-compose.vps.yml restart hermes-router
```

### Log Kontrolü
```bash
docker logs hermes-cmo-hermes-router-1 --tail 50
docker logs hermes-cmo-hermes-1 --tail 50
```

### Yeni Deploy
```bash
docker compose -f docker-compose.vps.yml build hermes-router
docker compose -f docker-compose.vps.yml up -d hermes-router
```

### Veritabanı Yedekleme
```bash
docker exec postgres pg_dump -U paperclip > backup_$(date +%Y%m%d).sql
```

### Hata Ayıklama
```bash
# Sağlık kontrolü
docker exec hermes-router python3 -c \
  "import urllib.request; print(urllib.request.urlopen('http://localhost:8699/health').read().decode())"

# Fleet durumu
docker exec hermes-router python3 -c \
  "import urllib.request; print(urllib.request.urlopen('http://localhost:8699/v1/fleet/status').read().decode())"

# Bekleyen onaylar
docker exec hermes-router python3 -c \
  "import urllib.request; print(urllib.request.urlopen('http://localhost:8699/v1/fleet/approvals').read().decode())"
```

---

## 7. Dosya Haritası

```
hermes-router/
├── router.py                    # FastAPI ana uygulama (tüm endpoint'ler)
├── config.yaml                  # Agent tanımları, keyword'ler, capabilities
├── agents.py                    # Agent registry + health check loop
├── intent.py                    # Intent detection (keyword + LLM fallback)
├── telegram_bot.py              # @bilmis1_bot, polling, approval keyboard
├── approval.py                  # ApprovalManager, onay bekleme mekanizması
├── camel.py                     # CaMeL Guard, güvenlik katmanı
├── delegation.py                # Agent-arası görev delegasyonu
├── retrieval.py                 # 5 kademeli bilgi erişim pipeline
├── hci.py                       # Fleet dashboard API endpoint'leri
├── Dockerfile                   # Container yapılandırması
├── requirements.txt             # Python bağımlılıkları
├── memory/
│   ├── models.py                # Lesson, Failure, WorkflowState modelleri
│   ├── store.py                 # File-based JSON CRUD storage
│   └── routes.py                # /v1/memory/* endpoint'leri
├── workflows/
│   ├── engine.py                # Workflow çalıştırıcı + Maestro + Camel entegrasyonu
│   ├── models.py                # Workflow, Step, EvaluationResult modelleri
│   ├── evaluator.py             # Jale kalite kontrol katmanı
│   ├── maestro_bridge.py        # Maestro lifecycle bridge
│   └── templates/
│       ├── seo-report.yaml      # SEO raporu pipeline
│       ├── analytics-report.yaml # Analitik raporu pipeline
│       └── gundem-scan.yaml     # Gündem tarama pipeline
└── scheduler/
    ├── parser.py                # Türkçe → cron expression parser
    ├── manager.py               # APScheduler yönetimi
    ├── models.py                # Schedule modelleri
    └── routes.py                # /v1/schedule/* endpoint'leri
```

---

## 8. Metrikler ve Başarı Kriterleri

| Metrik | Hedef | Mevcut |
|--------|-------|--------|
| Agent uptime | %99.9 | %100 (5/5 healthy) |
| Intent detection doğruluğu | %90 | %100 (10/10 test) |
| API response time | < 500ms | Çalışıyor |
| Evaluator coverage | Tüm workflow'lar | Aktif |
| Human approval | Yayınlama öncesi | Aktif (Telegram) |
| Memory kayıt | Her execution | Aktif (lesson + failure) |
| Maestro tracking | Her workflow | Aktif (mission/task/evidence) |

---

*Bu doküman, Hermes Fleet sisteminin tamamını belgeler. Yeni müşteri kurulumunda referans olarak kullanılabilir.*
