# Serper.dev

Google SERP-as-a-service: real Google search results (organic, news, images, places,
scholar) delivered as fast JSON, purpose-built for LLM agents. Simplest auth model of the
paid-quality providers.

> Part of **[Free API Bazaar](../../README.md)** · [Mega AI Bazaar](https://drvivek34.github.io/Mega-AI-Bazaar/)

## Free tier (verified 2026-08-24)

| Item | Value |
|---|---|
| Signup bonus | **2,500 free credits** (one-time, no expiry reported) |
| After bonus | Prepaid credit packs from **$50**; effective ≈ **$0.30–$1.00 per 1,000 queries** |
| Credit card | Not stated at signup — account works immediately on free credits |
| Cost class | Cheapest paid SERP tier among major providers (≈ $1 / 1k vs SerpApi's $9–25 / 1k) |

Sources: [Serper pricing overview](https://coldiq.com/blog/serper-pricing) ·
[SERP pricing comparison](https://apiserpent.com/blog/serp-api-pricing-comparison)

## How to get access

1. Sign up at [serper.dev](https://serper.dev/) — dashboard shows your key right away.
2. Export it:

```bash
export SERPER_API_KEY="your-serper-key"
```

## How to call it

POST-based, key in a header:

```bash
curl -s https://google.serper.dev/search \
  -H "X-API-KEY: $SERPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "gpu prices delhi market", "num": 5}'
```

Response: `{"organic": [{"title", "link", "snippet", "position"}], "news": [...],
"knowledgeGraph": {...}, "answerBox": {...}}` — includes Google answer boxes and the
knowledge panel when present, which most competitors omit.

Other endpoints: `/news`, `/images`, `/places`, `/scholar`, `/maps`.

Python quickstart:

```python
import os, requests

def serper_search(q: str, n: int = 5):
    r = requests.post("https://google.serper.dev/search",
                      headers={"X-API-KEY": os.environ["SERPER_API_KEY"]},
                      json={"q": q, "num": n}, timeout=20)
    r.raise_for_status()
    return [{"title": x["title"], "url": x["link"], "snippet": x["snippet"]}
            for x in r.json().get("organic", [])[:n]]
```

## Using it in an agent

- Default choice when you want **actual Google results** cheaply — 2,500 free credits is
  enough to prototype a full RAG loop before paying anything.
- `answerBox` / `knowledgeGraph` fields often remove the need for a follow-up scrape.
- Track remaining balance via the dashboard; the API doesn't push quota warnings.

## Pitfalls

- One-time credits, not monthly — unlike Tavily/Exa refills, the 2,500 don't renew.
- Header name is `X-API-KEY` (capital KEY); 401s usually mean a typo there.
- Heavy parallel bursts can trip rate limits — batch queries through a small queue.

## Links

- Signup / dashboard: <https://serper.dev/>
- Playground/docs: <https://serper.dev/playground>
