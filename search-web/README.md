# Search & Web

Free or free-credit web search, crawling, and extraction APIs — the "give my agent eyes on
the web" shelf.

> Part of **[Free API Bazaar](../README.md)** · Browse all bazaars at the **[Mega AI Bazaar](https://drvivek34.github.io/Mega-AI-Bazaar/)**.

## How entries are stored
Each provider lives in **its own sub-folder** inside this category, named in `kebab-case`:

```
search-web/
└── <provider-name>/
    └── README.md     # free-tier limits, access steps, API examples, pitfalls
```

## Add to this category
- Open a PR following the [contribution guide](../CONTRIBUTING.md), **or**
- Submit via the [submission form](https://github.com/Drvivek34/Free-API-Bazaar/issues/new/choose).

## Quick comparison (verified 2026-08-24)

| Provider | Free allowance | Card needed? | Best for |
|---|---|---|---|
| [Tavily](tavily/) | 1,000 credits/month (recurring) | No | LLM-native search + extract, easiest default |
| [Exa](exa/) | $10 credits/month (+$20 signup) | No | Semantic / neural search, papers, news |
| [Firecrawl](firecrawl/) | 1,000 credits/month | No | Search → scrape → clean markdown pipeline |
| [Brave Search API](brave-search-api/) | $5 credits/month (~1k queries) ⚠️ model changed Aug 2025 | Yes | Freshness (`age` field), independent index |
| [Serper.dev](serper-dev/) | 2,500 one-time credits | Not stated | Real Google SERP JSON, cheapest paid tier |
| [Google Custom Search](google-custom-search-json-api/) | 100 queries/day | Only for paid quota | Official Google results, site-scoped monitoring |
| [SearXNG](searxng/) | Unlimited (self-hosted) | No | Dev/testing, keyless metasearch |
| [Parallel Web Systems](parallel/) | PAYG ≈ $0.005/search; free local MCP server | See entry | Task-oriented parallel web research API |

## Picking one (cheat sheet)

- **Default agent search** → Tavily (recurring monthly quota, no card).
- **Conceptual / research queries** → Exa.
- **Need full page content, not snippets** → Firecrawl.
- **Freshness-sensitive lookups** → Brave (check its changed free tier first).
- **Exact Google results / answer boxes** → Serper or Google Custom Search.
- **Unlimited testing budget** → self-host SearXNG.

Quotas change often — every entry page carries a *verified* date; re-check the linked
official pricing page before relying on an offer.

## Entries

| Entry | Description |
|---|---|
| [Tavily](tavily/) | AI-native search engine for LLMs. 1,000 free credits/month, no card. |
| [Exa](exa/) | Neural/semantic search API. $20 signup + $10/month free credits. |
| [Firecrawl](firecrawl/) | Search + scrape + crawl to clean markdown. 1,000 free credits/month. |
| [Brave Search API](brave-search-api/) | Independent web index; $5/month free credits (card required). |
| [Serper.dev](serper-dev/) | Google SERP JSON API; 2,500 one-time free credits. |
| [Google Custom Search JSON API](google-custom-search-json-api/) | Official Google search; 100 free queries/day. |
| [Parallel Web Systems](parallel/) | Parallel task-oriented web research API. |
| [SearXNG](searxng/) | Self-hosted metasearch aggregator; unlimited & keyless. |
