# Brave Search API

Enterprise-grade Web Search API over Brave's independent 40B+ page index, with news,
images, and AI-snippet endpoints. Clean JSON, generous result metadata, strong
recent-content coverage.

> Part of **[Free API Bazaar](../../README.md)** · [Mega AI Bazaar](https://drvivek34.github.io/Mega-AI-Bazaar/)

## ⚠️ Free tier changed (verified 2026-08-24)

The old permanent free plan (**2,000 queries/month**, later 5,000 under the Aug 2025 AI
Grounding update) was **retired**. Current model:

| Item | Value |
|---|---|
| Current free allowance | **$5 in FREE prepaid credits every month**, auto-applied |
| ≈ Query volume | ~1,000–1,600 Web Search queries/month (AI snippet / Grounding calls cost more) |
| Credit card | **Yes — required at signup** (metered billing above the monthly credits) |
| Per-query cost | ≈ $0.003–$0.005 for standard Web Search |

Sources: [Brave API pricing](https://api-dashboard.search.brave.com/documentation/pricing) ·
[Coverage of the change](https://www.implicator.ai/brave-drops-free-search-api-tier-puts-all-developers-on-metered-billing/)

If you created a subscription before Aug 2025 and still see "Free" in old docs — check the
dashboard; legacy plans were migrated to metered billing.

## How to get access

1. Register at [api-dashboard.search.brave.com](https://api-dashboard.search.brave.com/)
   — card required (you stay inside the free $5 unless you exceed it).
2. Create a subscription and copy the API key.
3. Export it:

```bash
export BRAVE_SEARCH_API_KEY="BSA-your-key"
```

Variable-name gotcha: most integrations (including common MCP servers and router scripts)
expect exactly **`BRAVE_SEARCH_API_KEY`**, not `BRAVE_API_KEY`.

## How to call it

Auth uses the `X-Subscription-Token` header:

```bash
curl -s "https://api.search.brave.com/res/v1/web/search?q=hermes+agent+framework&count=5" \
  -H "X-Subscription-Token: $BRAVE_SEARCH_API_KEY" \
  -H "Accept: application/json"
```

Response: `{"web": {"results": [{"title", "url", "description", "age"}]}, "news": {...}}`

Other endpoints: `/res/v1/news/search`, `/res/v1/images/search`,
`/res/v1/summarizer/search` (AI snippets — higher credit cost), plus Grounding endpoints
for LLM tool use.

Python quickstart:

```python
import os, requests

def brave_search(q: str, n: int = 5):
    r = requests.get(
        "https://api.search.brave.com/res/v1/web/search",
        headers={"X-Subscription-Token": os.environ["BRAVE_SEARCH_API_KEY"],
                  "Accept": "application/json"},
        params={"q": q, "count": n},
        timeout=30,
    )
    r.raise_for_status()
    return [{"title": x["title"], "url": x["url"], "snippet": x["description"],
              "age": x.get("age")}
            for x in r.json()["web"]["results"]]
```

## Using it in an agent

- Strongest free-ish option for **freshness**: the `age` field ("2 hours ago") is reliable
  and great for recency ranking in agent pipelines.
- Pair with a keyword-capable provider (Serper/GCS) for full coverage — indexes differ.
- At ~$0.004/query, the monthly $5 covers roughly 1,250 plain searches; every summarizer or
  grounding call eats that budget several times faster.

## Pitfalls

- Card required now — trials that promise "no card" Brave access are outdated.
- Wrong env var name (`BRAVE_API_KEY`) is the #1 integration failure — use
  `BRAVE_SEARCH_API_KEY`.
- Only HTTP 200 calls should count against your local quota tracker; log 429s separately.
- Summarizer/Grounding endpoints bill differently from plain Web Search — isolate them behind
  a feature flag in cost-sensitive apps.

## Links

- Signup / dashboard: <https://api-dashboard.search.brave.com/>
- Product page: <https://brave.com/search/api/>
- Pricing: <https://api-dashboard.search.brave.com/documentation/pricing>
