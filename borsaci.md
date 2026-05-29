# Borsacı — Türk Finans Piyasaları AI Agent

## Genel Bilgi
- **Repo:** https://github.com/saidsurucu/borsaci.git
- **Konum:** `/opt/data/workspace/borsaci/`
- **Lisans:** MIT
- **Dil:** Python (PydanticAI)
- **LLM:** Google Gemini 3 Series (Pro + Flash) veya OpenRouter

## Kapsam
| Alan | Detay |
|------|-------|
| **BIST** | 758 şirket, finansal tablolar, teknik göstergeler (RSI, MACD, Bollinger), analist tavsiyeleri |
| **TEFAS** | 800+ yatırım fonu, kategori bazlı arama, portföy analizi |
| **Kripto** | BtcTurk (295+ TRY parite), Coinbase (500+ USD/EUR parite), orderbook |
| **Döviz** | 28+ parite |
| **Emtia** | Altın, petrol, gümüş |
| **Makro** | TCMB enflasyon (TÜFE, ÜFE), ekonomik takvim (30+ ülke) |

## Çalıştırma
```bash
# Docker ile
cd /opt/data/workspace/borsaci
docker-compose run --rm borsaci

# .env gerekiyor: OPENROUTER_API_KEY=***
```

## MCP Sunucu
Varsayılan: `https://borsamcp.fastmcp.app/mcp`
Özelleştirmek için: `BORSA_MCP_URL` env değişkeni

## Kullanım (Haberci ve Diğer Agent'lar)
Borsacı projesi MCP sunucusu üzerinden finans verisi sağlar. Agent'lar bu MCP araçlarını kullanarak:
- BIST hisse senedi fiyatları ve grafikleri
- TEFAS fon performansları
- Kripto para fiyatları
- Döviz kurları
- Ekonomik takvim verileri
- Teknik analiz göstergeleri

çekebilir ve yorumlayabilir.

## Notlar
- Eğitim ve araştırma amaçlıdır, yatırım tavsiyesi değildir
- OpenRouter API key veya Google Gemini OAuth ile çalışır
- Docker üzerinden izole çalıştırılması önerilir
