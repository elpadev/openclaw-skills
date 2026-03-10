#!/usr/bin/env python3
import argparse
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from typing import Dict, List

DDG_HTML_URL = "https://html.duckduckgo.com/html/"


def strip_tags(value: str) -> str:
    value = re.sub(r"<!--.*?-->", " ", value, flags=re.S)
    value = re.sub(r"<(script|style|noscript|svg|form|nav|header|footer)[^>]*>.*?</\1>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def resolve_ddg_link(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc.endswith("duckduckgo.com") and parsed.path.startswith("/l/"):
        qs = urllib.parse.parse_qs(parsed.query)
        uddg = qs.get("uddg", [None])[0]
        if uddg:
            return urllib.parse.unquote(uddg)
    return url


def fetch_html(query: str, timeout: int = 20) -> str:
    params = urllib.parse.urlencode({"q": query})
    url = f"{DDG_HTML_URL}?{params}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_results(raw_html: str, limit: int) -> List[Dict[str, str]]:
    # Extract each result block first for safer parsing
    blocks = re.findall(r"<div[^>]+class=\"[^\"]*result[^\"]*\"[^>]*>(.*?)</div>\s*</div>", raw_html, flags=re.I | re.S)
    if not blocks:
        # Fallback: parse links directly
        blocks = re.findall(r"<a[^>]+class=\"[^\"]*result__a[^\"]*\"[^>]*>.*?</a>", raw_html, flags=re.I | re.S)

    items: List[Dict[str, str]] = []

    for block in blocks:
        a_match = re.search(r"<a[^>]+class=\"[^\"]*result__a[^\"]*\"[^>]*href=\"([^\"]+)\"[^>]*>(.*?)</a>", block, flags=re.I | re.S)
        if not a_match:
            continue

        href = html.unescape(a_match.group(1).strip())
        title_html = a_match.group(2)
        title = strip_tags(title_html)
        url = resolve_ddg_link(href)

        sn_match = re.search(r"<a[^>]+class=\"[^\"]*result__snippet[^\"]*\"[^>]*>(.*?)</a>|<div[^>]+class=\"[^\"]*result__snippet[^\"]*\"[^>]*>(.*?)</div>", block, flags=re.I | re.S)
        snippet = ""
        if sn_match:
            snippet = strip_tags(sn_match.group(1) or sn_match.group(2) or "")

        if title and url:
            items.append({"title": title, "url": url, "snippet": snippet})
        if len(items) >= limit:
            break

    # De-duplicate by URL
    dedup: List[Dict[str, str]] = []
    seen = set()
    for item in items:
        if item["url"] in seen:
            continue
        seen.add(item["url"])
        dedup.append(item)
    return dedup[:limit]


def main() -> int:
    p = argparse.ArgumentParser(description="DuckDuckGo HTML search parser")
    p.add_argument("--query", required=True, help="Search query")
    p.add_argument("--limit", type=int, default=5, help="Max results")
    p.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    args = p.parse_args()

    if args.limit < 1 or args.limit > 20:
        print("ERROR: --limit must be between 1 and 20", file=sys.stderr)
        return 2

    try:
        raw = fetch_html(args.query)
        results = parse_results(raw, args.limit)
        out = {
            "query": args.query,
            "provider": "duckduckgo-html",
            "count": len(results),
            "results": results,
        }
        if args.pretty:
            print(json.dumps(out, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(out, ensure_ascii=False))
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
