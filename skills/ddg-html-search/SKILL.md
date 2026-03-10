---
name: ddg-html-search
description: Search the web via DuckDuckGo HTML endpoint (https://html.duckduckgo.com/html/?q=...) and return cleaned, model-friendly results. Use when web_search returns weak/no results, when the user asks for DuckDuckGo-based search, or when you need deterministic non-JS HTML search output with top links/snippets.
---

# DuckDuckGo HTML Search

Use this skill for fallback web search with parseable HTML-only output.

## Run

```bash
python3 skills/ddg-html-search/scripts/ddg_html_search.py --query "salamtoman" --limit 5
```

## Behavior

- Fetch from `https://html.duckduckgo.com/html/?q=<query>`.
- Remove noisy HTML (`script`, `style`, `form`, `nav`, `header`, `footer`, comments, extra whitespace).
- Extract top results (title, url, snippet).
- Resolve DuckDuckGo redirect links (`/l/?uddg=...`) to canonical target URLs.
- Return compact JSON for clean model context.

## Recommended flow

1. Run the script with the exact user query.
2. If results are empty, retry with quote/no-quote variants.
3. Return top `N` entries with title + URL + snippet.
4. Clearly mark when results are best-effort from HTML parsing.

## Example

```bash
python3 skills/ddg-html-search/scripts/ddg_html_search.py \
  --query "openclaw skills" \
  --limit 5 \
  --pretty
```
