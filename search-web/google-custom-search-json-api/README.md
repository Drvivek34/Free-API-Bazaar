# Google Custom Search JSON API

Google's official programmatic search API. Searches either the entire web (via a configured
Custom Search Engine) or specific sites. Stable, well-documented, genuinely free — but
daily-capped.

> Part of **[Free API Bazaar](../../README.md)** · [Mega AI Bazaar](https://drvivek34.github.io/Mega-AI-Bazaar/)

## Free tier (verified 2026-08-24)

| Item | Value |
|---|---|
| Free quota | **100 queries / day** (≈ 3,000/month) |
| Paid scale-up | $5 per additional 1,000 queries/day, up to 10k/day |
| Credit card | Needed only for paid quota |
| Auth | API key **+** Custom Search Engine ID (`cx`) — both required |

Source: [Official overview](https://developers.google.com/custom-search/v1/overview)

## How to get access (two artifacts, not one)

1. Create a Custom Search Engine at [programmablesearchengine.google.com](https://programmablesearchengine.google.com/)
   — enable **"Search the entire web"**, note the engine ID (`cx`).
2. Create an API key in [Google Cloud Console](https://console.cloud.google.com/) →
   APIs & Services → Credentials (enable "Custom Search API" first).
3. Export both:

```bash
export GCS_API_KEY="AIza..."
export GCS_CX="0123456789abcdef:xyz"
```

## How to call it

Simple GET — easiest API of the bunch:

```bash
curl -s "https://www.googleapis.com/customsearch/v1" \
  --data-urlencode "key=$GCS_API_KEY" \
  --data-urlencode "cx=$GCS_CX" \
  --data-urlencode "q=open source llm inference servers" \
  --data-urlencode "num=5"
```

Response: `{"items": [{"title", "link", "snippet"}], "searchInformation": {...}}`
— supports `dateRestrict` (e.g. `q=d30` style freshness), `siteSearch` filters, country /
language params, and pagination via `start` (max 100 results total per query window).

Python quickstart:

```python
import os, requests

def gcs_search(q: str, n: int = 5):
    r = requests.get("https://www.googleapis.com/customsearch/v1", params={
        "key": os.environ["GCS_API_KEY"],
        "cx": os.environ["GCS_CX"],
        "q": q, "num": min(n, 10),
    }, timeout=20)
    r.raise_for_status()
    return [{"title": i["title"], "url": i["link"], "snippet": i["snippet"]}
            for i in r.json().get("items", [])]
```

## Using it in an agent

- Rock-solid zero-cost baseline for low-volume agents: schedule around the 100/day cap
  (cache aggressively, dedupe queries before they hit the API).
- Ideal for *site-scoped* monitoring (one `cx` per target site = precise change detection).
- Pair with a bigger-quota provider for interactive traffic; let GCS handle scheduled checks.

## Pitfalls

- Forgetting the `cx` param is the classic failure — key alone returns 400.
- `num` maxes at 10 per request despite docs hinting larger values.
- Daily quota resets at midnight PT, not IST — align cron jobs accordingly.
- 403 `quotaExceeded` mid-loop means the day's cap is gone; switch providers until tomorrow.

## Links

- Overview & quotas: <https://developers.google.com/custom-search/v1/overview>
- Programmable Search Engine console: <https://programmablesearchengine.google.com/>
- API reference: <https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list>
