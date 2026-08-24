# Exa

Semantic / neural search API built for AI applications — query by meaning instead of
keywords, with category filters, domain filters, and a `/contents` endpoint that returns
cleaned page text.

> Part of **[Free API Bazaar](../../README.md)** · [Mega AI Bazaar](https://drvivek34.github.io/Mega-AI-Bazaar/)

## Free tier (verified 2026-08-24)

| Item | Value |
|---|---|
| Signup bonus | **$20 in free credits** (≈ 2,800 searches, one-time) |
| Monthly refill | **$10 in credits every month** on the Free Tier (≈ 1,000–1,400 searches) |
| Credit card | **Not required** |
| Pay-as-you-go | From ≈ **$7 / 1,000 standard neural `/search` requests** (endpoint-dependent; `/contents` costs more) |

Sources: [exa.ai/pricing](https://exa.ai/pricing) ·
[Pricing reference](https://exa.ai/docs/reference/pricing)

Note: Exa's separate **Websets** product has its own plans and does **not** draw from these
API credits.

## How to get access

1. Sign up at [dashboard.exa.ai](https://dashboard.exa.ai/) — no card needed.
2. Create an API key on the Keys page.
3. Export it:

```bash
export EXA_API_KEY="your-exa-key"
```

## How to call it

Auth uses the `x-api-key` header:

```bash
curl -s https://api.exa.ai/search \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "research papers on LLM jailbreak defenses",
        "numResults": 5,
        "useAutoprompt": true}'
```

Response: `{"results": [{"title", "url", "publishedDate", "author", "id"}]}`
— no relevance score by default; results come back already ranked semantically.

Add page text with `/contents`:

```bash
curl -s https://api.exa.ai/contents \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ids": ["<result-id-from-search>"], "text": true}'
```

Useful `/search` options:

- `category`: `news`, `pdf`, `github`, `tweet`, `company`, `paper` — narrows result type.
- `includeDomains` / `excludeDomains`: domain allow/block lists.
- `startPublishedDate` / `endPublishedDate`: freshness windows (`2026-01-01` style).
- `useAutoprompt: true` — rewrites your query into a better neural query (costs more per call).

Python quickstart:

```python
import os, requests

def exa_search(query: str, n: int = 5, category: str | None = None):
    payload = {"query": query, "numResults": n}
    if category:
        payload["category"] = category
    r = requests.post("https://api.exa.ai/search",
                      headers={"x-api-key": os.environ["EXA_API_KEY"]},
                      json=payload, timeout=30)
    r.raise_for_status()
    return [{"title": x["title"], "url": x["url"], "published": x.get("publishedDate")}
            for x in r.json()["results"]]
```

## Using it in an agent

- Best pick when the query is *conceptual* ("approaches to X", "papers like Y") rather than
  keyword-shaped.
- `category: "news"` + a `startPublishedDate` gives a cheap freshness filter without burning
  extra calls on retries.
- The monthly $10 refill is the real free tier — budget ≈ 35–45 searches/day to stay inside it.

## Pitfalls

- No relevance score in responses — don't compare "score" fields across providers.
- `useAutoprompt`, `/contents`, and `findSimilar` each have different credit costs; check the
  pricing table before wiring them into hot loops.
- Websets usage never touches API credits — confusion here makes people think credits vanished.
- Unused monthly credits don't accumulate.

## Links

- Dashboard / signup: <https://dashboard.exa.ai/>
- Docs: <https://docs.exa.ai/>
- Pricing reference: <https://exa.ai/docs/reference/pricing>
