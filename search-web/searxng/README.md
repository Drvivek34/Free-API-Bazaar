# SearXNG

Open-source metasearch engine: aggregates Google, Bing, DuckDuckGo, Brave, Startpage and
others into one JSON API — with **no API key, no quota, and no cost**, because you host it.

> Part of **[Free API Bazaar](../../README.md)** · [Mega AI Bazaar](https://drvivek34.github.io/Mega-AI-Bazaar/)

## Free tier (verified 2026-08-24)

| Item | Value |
|---|---|
| Cost | **Free forever** — self-hosted open source (AGPLv3) |
| Quota | None imposed by SearXNG itself; upstream engines may throttle abusive IPs |
| Auth | None (disable the JSON formatter at your peril — see pitfalls) |

Source: [searxng/searxng on GitHub](https://github.com/searxng/searxng)

## How to get access (self-host)

Docker, the standard route:

```bash
docker run -d --name searxng -p 8888:8080 \
  -v "$PWD/searxng:/etc/searxng" \
  searxng/searxng:latest
```

Enable the JSON output API by editing `searxng/settings.yml`:

```yaml
search:
  formats:
    - html
    - json
```

Then restart the container. Test:

```bash
curl -s "http://localhost:8888/search?q=free+tts+apis&format=json&language=en"
```

Response: `{"results": [{"url", "title", "content", "engine", "score"}]}` — each result
carries the upstream `engine` and a merged `score`; dedupe happens automatically.

Python quickstart:

```python
import requests

def searx_search(q: str, n: int = 5, base="http://localhost:8888"):
    r = requests.get(f"{base}/search", params={"q": q, "format": "json"},
                     timeout=30)
    r.raise_for_status()
    return [{"title": x["title"], "url": x["url"], "snippet": x["content"],
              "engines": x.get("engines")}
            for x in r.json()["results"][:n]]
```

## Using it in an agent

- Unlimited dev/testing backend: hammer it during development, save paid credits for prod.
- `engines` field reveals which upstreams agree about a result — cheap multi-engine voting.
- Public instances exist (see searx.space) but most block the JSON API to prevent abuse —
  self-hosting is the supported path.

## Pitfalls

- JSON formatter is **disabled by default** — a missing `format=json` capability is config,
  not breakage.
- Running unauthenticated JSON APIs publicly gets your instance abused within days; put auth
  or a firewall in front.
- Upstream engines rotate anti-bot measures; keep the image updated or engines start failing
  silently.
- Result quality ≠ Google's; treat as breadth, not authority.

## Links

- Source: <https://github.com/searxng/searxng>
- Docs: <https://docs.searxng.org/>
- Public instance list: <https://searx.space/>
