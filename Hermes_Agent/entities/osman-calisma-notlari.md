# Osman Calisma Notlari

## 29 Mayis 2026 — Ogrenilen Dersler

### API Key Eksikligi
- XAI_API_KEY ve BRAVE_API_KEY environment variable'lari tanimli degil.
- x_search_helper.py ve Brave Search API calismaz.
- Cozum: Browser ile doğrudan haber sitelerine git.

### Bot Detection
- Google Search ve Bing doğrudan sorgu bot detection'a takilir.
- Cozum: Haber sitelerine direkt navigasyon (TechCrunch, The Verge, SEL, MarTech, Webrazzi).

### Calisan Kaynaklar (Browser ile)
- TechCrunch AI: https://techcrunch.com/category/artificial-intelligence/
- The Verge AI: https://www.theverge.com/ai-artificial-intelligence
- Search Engine Land: https://searchengineland.com/
- MarTech: https://martech.org/
- Webrazzi: https://webrazzi.com/
- Google Haberler: https://news.google.com/search?q=...&hl=tr&gl=TR&ceid=TR:tr

### Dosya Yollari
- Gundem raporlari: /opt/data/wiki/Hermes_Agent/reports/osman/YYYY-MM-DD-HHmm-gundem.md
- Tweet havuzu: /opt/data/wiki/Hermes_Agent/entities/ekrem-tweet-havuzu.md
- Wiki repo: /opt/data/wiki/Hermes_Agent/ (git push origin master)

### Skill Yazma
- /opt/data/skills read-only mount edildigi icin skill create islemi basarisiz olur.
- Skill yazmak icin farkli filesystem yolu veya mount duzeltmesi gerekli.

### web_search Araci
- Bu ortamda `web_search` araci mevcut degil. Browser veya curl kullanilmali.
