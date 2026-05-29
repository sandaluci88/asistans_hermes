---
title: X API Ban Koruması ve Entegrasyon Planı
tags: [x, twitter, api, ban, rate-limit, guvenlik]
date: 2026-05-23
status: active
brain: A
---

# X API Ban Koruması ve Entegrasyon Planı

## 1. Ban Sebepleri ve Önlemler

### Sebep 1: Rate Limit Aşımı
**Sorun:** X API'nin rate limit'i aşılırsa geçici/ kalıcı ban.

**Çözümler:**
- Günlük post limiti (max 5 tweet/gün)
- Cron job'lar arası minimum 2 saat
- `x-url-usage-limit-remaining` header'ını oku, %10 altına düşünce dur
- 429 hatası alınca 15dk bekle (Retry-After header'ı)

### Sebep 2: Duplikasyon
**Sorun:** Aynı içeriğin tekrar tekrar atılması spam olarak algılanır.

**Çözümler:**
- Tweet metninin SHA256 hash'ini kaydet
- Son 50 tweet'in hash'ini kontrol et
- %80 benzerlik → atma
- Son 24 saatte aynı konu → atma

### Sebep 3: Görsel Spam
**Sorun:** Aynı görselin tekrar kullanımı.

**Çözümler:**
- Görselin perceptual hash'ini (pHash) hesapla
- Son 20 görselin hash'ini kontrol et
- Eşik: Hamming distance < 10 → atma

### Sebep 4: Suspicious Behavior (Şüpheli Davranış)
**Sorun:** Bot gibi davranma (çok hızlı, sürekli aynı pattern).

**Çözümler:**
- Random bekleme (1-3sn arası)
- Her tweet farklı uzunlukta (800-2000 random)
- Post saatleri rastgele 5-10dk kaydır
- Haftada 1 gün tatil (Pazar)

### Sebep 5: API Abuse
**Sorun:** Aynı endpoint'e art arda çok fazla istek.

**Çözümler:**
- Döngüsel tweet atma (her işlem arası 1-3sn)
- Bulk işlem yapma, tek tek işle
- Error handling: her hata için exponential backoff

---

## 2. Kill Switch Mekanizması

```python
KILL_SWITCH = {
    "enabled": True,
    "daily_limit": 5,          # Günde max 5 tweet
    "min_interval": 120,       # İki tweet arası min 2 saat (dakika)
    "max_retries": 3,          # API hatasında max deneme
    "cooldown_on_error": 900,  # Hata sonrası bekleme (15dk)
    "similarity_threshold": 0.8, # %80 benzerlik = atma
    "state_file": "/tmp/x-kill-switch.json"
}
```

### State Dosyası Yapısı
```json
{
    "date": "2026-05-23",
    "tweets_today": 2,
    "last_tweet_at": "2026-05-23T12:00:00",
    "tweet_history": [
        {
            "id": "2058168049719509301",
            "text_hash": "sha256...",
            "topic": "E-E-A-T++",
            "posted_at": "2026-05-23T12:00:00"
        }
    ],
    "image_hashes": ["phash1", "phash2"],
    "rate_limit_remaining": 100,
    "rate_limit_reset": "2026-05-23T13:00:00"
}
```

---

## 3. Twitter API Client (OAuth 1.0a + v1.1 uploadMedia)

### Neden OAuth 1.0a?
- Medya yükleme (v1.1) OAuth 1.0a gerektirir
- xurl OAuth 1.0a kullanıyor (consumer_key/secret + token/secret)
- `client.v1.uploadMedia()` → media ID döner
- Sonra v2 API ile tweet at (`media_ids` ile)

### Python ile Direkt Kullanım

```python
import requests
from requests_oauthlib import OAuth1

# OAuth 1.0a credentials (xurl ~/.xurl dosyasındakiler)
auth = OAuth1(
    client_key="VYlbK2jHX9Mi7Qs01DtiqnOFC",
    client_secret="zivkEGNJgeMuc6i08E26acVHyMTh62eahmGc90GjTmkOcsjXW7",
    resource_owner_key="1980994616674426880-5psVswVPUfsgHAd0UBWIQF1sZVtSKR",
    resource_owner_secret="YHzYelMsKGjZsHA6GVQs8xpAWfDyh5RDy8exT848usRKo"
)

# 1. Medya yükle (v1.1)
url_upload = "https://upload.twitter.com/1.1/media/upload.json"
with open(image_path, "rb") as f:
    files = {"media": f}
    resp = requests.post(url_upload, auth=auth, files=files)
    media_id = resp.json()["media_id"]

# 2. Tweet at (v2)
url_tweet = "https://api.twitter.com/2/tweets"
body = {
    "text": tweet_text,
    "media": {"media_ids": [str(media_id)]}
}
resp = requests.post(url_tweet, auth=auth, json=body)
```

---

## 4. Pipeline'a Entegrasyon

```python
def should_post(kill_switch_state):
    """Kill switch kontrolü — tweet atılabilir mi?"""
    now = datetime.now()
    
    # Günlük limit kontrolü
    if kill_switch_state["tweets_today"] >= KILL_SWITCH["daily_limit"]:
        return False, "Gunluk limit doldu"
    
    # Son tweet'ten 2 saat geçmiş mi?
    last = kill_switch_state.get("last_tweet_at")
    if last:
        elapsed = (now - datetime.fromisoformat(last)).total_seconds() / 60
        if elapsed < KILL_SWITCH["min_interval"]:
            return False, f"Cok erken ({elapsed:.0f}dk gecti, {KILL_SWITCH['min_interval']}dk gerekli)"
    
    return True, "OK"


def check_duplicate(text, history):
    """Tweet metninin duplicate olup olmadığını kontrol et"""
    import hashlib
    new_hash = hashlib.sha256(text.encode()).hexdigest()
    
    for tweet in history:
        if tweet["text_hash"] == new_hash:
            return True  # Aynı metin
        # %80 benzerlik kontrolü
        if similarity(text, tweet["topic"]) > KILL_SWITCH["similarity_threshold"]:
            return True  # Çok benzer
    
    return False


def save_state(state):
    """Kill switch state'ini kaydet"""
    with open(KILL_SWITCH["state_file"], "w") as f:
        json.dump(state, f, indent=2)
```

---

## 5. Pipeline'da Implementasyon

```
hermes-infografik-pipeline.py

Giriş:
→ kill switch kontrolü (günlük limit, interval, duplicate)
→ Eğer blocked: "Bugünlük limit doldu, devam etme" → raporla + çık

Normal akış:
→ Sheets'ten konu al
→ Ekrem tweet üret
→ Ayla infografik oluştur
→ Kill switch'e kaydet (metin hash'i)
→ uploadMedia (v1.1)
→ Tweet at (v2, media_ids ile)
→ Kill switch state güncelle
→ Sheets DONE
```

---

## İlgili Sayfalar
- [[hermes-infografik-pipeline]] — Ana pipeline
- [[007-pipeline-hata-cozumleri]] — Daha önceki hatalar
- [[ekrem-x-ajani]] — Ekrem tweet üretim ajanı
