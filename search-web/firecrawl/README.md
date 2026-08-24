# Firecrawl

Web data stack for AI agents: `/search` (web search), `/scrape` (single URL → clean
markdown), `/crawl` (multi-page walks), `/map` (site link maps), and structured
`/extract`. Search results can be scraped in the same call via `scrapeOptions`.

> Part of **[Free API Bazaar](../../README.md)** · [Mega AI Bazaar](https://drvivek34.github.io/Mega-AI-Bazaar/)

## Free tier (verified 2026-08-24)

| Item | Value |
|---|---|
| Monthly quota | **1,000 credits / month** (refreshed monthly) |
| What 1 credit buys | ≈ 1 page scraped; search/crawl/map draw credits per page processed |
| Rate limit | ≈ 10 requests / min |
| Credit card | **Not required** |
| Paid upgrade | Hobby tier available once the monthly refresh runs out |

Sources: [firecrawl.dev/pricing](https://www.firecrawl.dev/pricing) (FAQ: "Firecrawl is free
for 1,000 pages every month")

Note: older third-party write-ups still cite a 500-credit free plan — the official pricing
page now states 1,000/month.

## How to get access

1. Sign up at [firecrawl.dev](https://www.firecrawl.dev/) — no card for the free plan.
2. Grab the API key from the dashboard.
3. Export it:

```bash
export FIRECRAWL_API_KEY="fc-your-key"
```

## How to call it

Auth uses `Authorization: Bearer`:

```bash
# Web search with cleaned content
curl -s https://api.firecrawl.dev/v2/search \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "site reliability engineer salary india 2026",
        "limit": 5,
        "scrapeOptions": {"formats": ["markdown"]}}'
```

Single-URL scrape (the workhorse):

```bash
curl -s https://api.firecrawl.dev/v2/scrape \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/blog/post", "formats": ["markdown"]}'
```

Response: `{"data": {"markdown": "...", "metadata": {...}, "links": [...]}}` —
markdown arrives heading-preserving and boilerplate-stripped, ready for LLM context.

Long jobs (`/crawl`, bulk `/extract`) are async: the first response carries a job ID you poll
at `/v2/crawl/{id}` until `status: "completed"`.

Python quickstart:

```python
import os, requests

HDRS = {"Authorization": f"Bearer {os.environ['FIRECRAWL_API_KEY']}"}

def fc_search(query: str, limit: int = 5):
    r = requests.post("https://api.firecrawl.dev/v2/search", headers=HDRS,
                      json={"query": query, "limit": limit}, timeout=60)
    r.raise_for_status()
    out = []
    for w in r.json().get("data", {}).get("web", []):
        out.append({"title": w.get("title"), "url": w.get("url"),
                     "snippet": (w.get("description") or "")[:300],
                     "markdown": ((w.get("markdown") or "")[:2000])})
    return out
```

## Using it in an agent

- Choose Firecrawl when the task needs **page content**, not just snippets: docs ingestion,
  price/product extraction, changelog diffs.
- `/map` first, then targeted `/scrape`s of the mapped URLs beats blind `/crawl` for credit
  economy on big sites.
- Cache scraped markdown by URL hash — repeat reads shouldn't double-bill.

## Pitfalls

- Async endpoints return 202 + job ID, not results — forgetting the poll step looks like an
  empty response.
- AI `/extract` burns multiple credits per call; reserve it for schema'd fields you actually need.
- JS-heavy sites may need the `waitFor` option or return skeleton HTML.
- Rate limit (~10 req/min) trips fast in parallel loops — back off on 429.

## Links

- Dashboard / signup: <https://www.firecrawl.dev/>
- Docs: <https://docs.firecrawl.dev/>
- Billing: <https://docs.firecrawl.dev/billing>
