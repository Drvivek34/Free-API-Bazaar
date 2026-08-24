# Tavily

AI-native search engine built specifically for LLMs and RAG agents. Returns clean,
LLM-ready results with relevance scores, plus Extract and Crawl endpoints for pulling
full-page content.

> Part of **[Free API Bazaar](../../README.md)** · [Mega AI Bazaar](https://drvivek34.github.io/Mega-AI-Bazaar/)

## Free tier (verified 2026-08-24)

| Item | Value |
|---|---|
| Plan name | **Researcher** (free) |
| Monthly quota | **1,000 API credits / month** |
| Reset | Monthly |
| Credit card | **Not required** |
| Credit cost | Basic Search = 1 · Advanced Search = 2 · Extract = 1 credit / 5 URLs |
| Paid upgrade | Project plan $30/mo for 4,000 credits; overage ≈ $0.008/credit |

Sources: [Credits & Pricing docs](https://docs.tavily.com/documentation/api-credits) ·
[Pricing page](https://www.tavily.com/pricing)

## How to get access

1. Sign up at [app.tavily.com](https://app.tavily.com/) — email or GitHub login, no card.
2. Copy your API key (`tvly-...`) from the dashboard home.
3. Export it:

```bash
export TAVILY_API_KEY="tvly-your-key-here"
```

## How to call it

Auth goes **in the JSON body**, not a header (common gotcha):

```bash
curl -s https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -d '{"api_key": "$TAVILY_API_KEY",
        "query": "best free LLM APIs 2026",
        "search_depth": "basic",
        "max_results": 5}'
```

Response shape: `{"results": [{"title", "url", "content", "score"}], "response_time"}`
— `score` is Tavily's own relevance score (0–1).

Python quickstart:

```python
import requests

def tavily_search(query: str, n: int = 5, depth: str = "basic"):
    r = requests.post("https://api.tavily.com/search", json={
        "api_key": __import__("os").environ["TAVILY_API_KEY"],
        "query": query,
        "search_depth": depth,      # basic=1cr, advanced=2cr
        "max_results": n,
    }, timeout=30)
    r.raise_for_status()
    return [{"title": x["title"], "url": x["url"],
              "snippet": x["content"], "score": x.get("score")}
            for x in r.json()["results"]]
```

Other endpoints:

- **Extract** — POST `/extract` with `"urls": [...]` pulls raw page content (1 credit / 5 URLs).
- **Crawl** — POST `/crawl` walks a site from a base URL (1 credit / 10 pages extracted).

## Using it in an agent / Hermes

- Point any OpenAI-style tool-calling loop at the function above; feed `title + url + snippet`
  into context.
- Budget rule of thumb: a Basic Search per user turn keeps you under ~33 searches/day on
  the free tier. Reserve Advanced Search (2 credits) for vague or multi-hop queries.
- Combine with Extract only on the top 2–3 hits, never all results, to stretch credits.

## Pitfalls

- Sending the key as an `Authorization` header does nothing — Tavily wants `api_key` in the body.
- `advanced` depth silently doubles credit burn; set it deliberately.
- 432 status = quota exhausted / key problem — check the dashboard before retrying.
- Credits reset on the 1st, they do **not** roll over.

## Links

- Dashboard / signup: <https://app.tavily.com/>
- Docs: <https://docs.tavily.com/>
- Credits & pricing: <https://docs.tavily.com/documentation/api-credits>
