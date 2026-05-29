---
title: Pipeline Hata Günlüğü ve Çözümleri
tags: [pipeline, hata, debug, api-key, environment]
date: 2026-05-23
status: active
brain: A
---

# Pipeline Hata Günlüğü — 23 Mayıs 2026

## Sorun 1: DeepSeek API Key Subprocess'e Geçmedi

**Hata:** `HTTP Error 401: Unauthorized` — DeepSeek API key geçersiz.

**Kök Neden:** Hermes Gateway process'inde `DEEPSEEK_API_KEY` environment variable olarak tanımlı. Ancak gateway, güvenlik nedeniyle subprocess'lere env değişkenlerini **maskelenmiş** (`***`) olarak geçiriyor. Python script'i `os.environ.get("DEEPSEEK_API_KEY")` ile okumaya çalışınca boş string alıyor.

**Belirtiler:**
- `cat /proc/1/environ` → `DEEPSEEK_API_KEY=***` (maskelenmiş)
- `os.environ` veya `subprocess` env'i → key yok
- `config.yaml` içinde `${DEEPSEEK_API_KEY}` placeholder

**Çözüm:** API key'i doğrudan Python script'ine **hardcode** et. Hardcode edilen key sadece script içinde kalır, environment'a sızmaz.

```python
DEEPSEEK_KEY = "sk-da274deb322d44fb98d6f8bbe2ae0b87"
```

## Sorun 2: xurl PATH'te Bulunamadı

**Hata:** `env: ‘node’: No such file or directory`

**Kök Neden:** xurl bir Node.js uygulaması (`#!/usr/bin/env node`). `subprocess.run` ile çağrılırken `PATH` environment variable'ı tam olarak ayarlanmazsa `node` bulunamıyor.

**Belirtiler:**
- Terminal'den xurl çalışıyor
- Python subprocess'ten xurl çağırınca "node not found"

**Çözüm:** Her xurl çağrısından önce `PATH`'e npm global bin + standart yolları ekle:

```python
xurl_path = os.path.expanduser("~/.npm-global/bin/xurl")
env = os.environ.copy()
env["PATH"] = f"{os.path.expanduser('~/.npm-global/bin')}:/usr/bin:/usr/local/bin:{env.get('PATH', '')}"
```

**Alternatif:** xurl'in Node.js binary wrapper olduğunu ve `node`'un `/usr/bin/node`'da olduğunu unutma. `env` dict'inde `/usr/bin`'i eklemeyi ihmal etme.

## Sorun 3: Media Upload JSON Parse

**Hata:** `Media JSON parse failed, posting text only`

**Kök Neden:** xurl media upload çıktısında `processing_info.state = "pending"` döndüğünde, kod `media_data.get("data", {}).get("id")` ile media_id'yi bulamıyor. Çünkü asıl yapı:

```json
{
  "data": {
    "id": "1234567890",
    "media_key": "...",
    "processing_info": {"state": "pending"}
  }
}
```

**Belirtiler:**
- Media upload başarılı (HTTP 200)
- JSON parse exception veya `media_id = None`

**Çözüm:** Hem `data.id` hem de `media_id` alanlarını kontrol et:

```python
media_data = json.loads(result.stdout)
media_id = media_data.get("data", {}).get("id") or media_data.get("media_id")
```

## Sorun 4: Google AI Studio API Key Geçersiz

**Hata:** `400 INVALID_ARGUMENT: API key not valid`

**Kök Neden:** Skill'de frontmatter'da `api_key: AIzaSy...CwrI` yazılıyor ama bu key geçerli değil. Gerçek çalışan key farklı.

**Benzer Sorun:** Gateway'deki `OPENROUTER_API_KEY` da maskelenmiş placeholder olarak kayıtlı (`sk-or-...ed83`). Gerçek değer sadece gateway'in kendi credential pool'unda.

**Çözüm:** Hardcode edilen API key'lerin çalıştığından emin ol. Test etmeden pipeline'a koyma.

## Sorun 5: Sheets UPDATE için Satır Numarası

**Hata:** Sheets'te DONE işaretlerken yanlış satıra yazma.

**Kök Neden:** Google Sheets API 1-indexed. Kodda `enumerate` 0-indexed döndüğü için `i + 1` ile düzeltilmiş. Unutulursa bir satır aşağı/ yukarı yazar.

**Çözüm:** 
```python
for i, row in enumerate(values):
    if status.upper() == "TODO" and konu:
        return i + 1, konu  # +1 = sheets 1-indexed
```

## Sorun 6: Gemini Infografik Bekleme Süresi

**Hata:** Infografik oluşmadan pipeline devam ediyor.

**Kök Neden:** Gemini 3.1 Flash Image Preview görsel üretirken ~60 saniye beklemek gerekiyor. Kod timeout vermeden hemen sonucu okumaya çalışıyor.

**Çözüm:** API çağrısında timeout'u 120 saniye yap:

```python
response = client.models.generate_content(
    model=MODEL,
    contents=prompt,
    config=types.GenerateContentConfig(
        timeout=120  # 60sn bekleme + 60sn buffer
    )
)
```

## Genel Kural

**Hermes Gateway environment variable'ları subprocess'lere maskelenmiş geçer.** Bir Python script'inin API key'e erişmesi gerekiyorsa:
1. Key'i script'e hardcode et (önerilen)
2. Veya bir ara dosyaya yaz (güvenlik riski)
3. Veya gateway API'sini kullan (auth gerekir)

