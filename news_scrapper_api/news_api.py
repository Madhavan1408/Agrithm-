"""
news_api.py
-----------
Farmer News Scraper - Core Module

Inputs  : city (village/city of farmer), crop (crop name), state (optional), limit (optional)
Output  : List of ranked, deduplicated news articles relevant to the farmer

Sources : Google News RSS (free, no API key required)
Strategy: Multi-query approach — hyperlocal, state-level, and national agri news
"""

import feedparser
from urllib.parse import quote
from datetime import datetime
from typing import Optional


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def _build_rss_url(query: str, lang: str = "en-IN", country: str = "IN") -> str:
    """Construct a Google News RSS URL for the given search query."""
    encoded = quote(query)
    return f"https://news.google.com/rss/search?q={encoded}&hl={lang}&gl={country}&ceid={country}:{lang.split('-')[0]}"


def _parse_published(entry) -> str:
    """Extract and format published date from a feed entry."""
    try:
        t = entry.get("published_parsed") or entry.get("updated_parsed")
        if t:
            return datetime(*t[:6]).strftime("%Y-%m-%d %H:%M")
    except Exception:
        pass
    return entry.get("published", "Unknown date")


def _score_article(title: str, summary: str, city: str, crop: str, state: str) -> int:
    """
    Relevance score: higher = more relevant to this farmer.
    Checks how many of the key terms appear in the title/summary.
    """
    text = (title + " " + summary).lower()
    keywords = [
        city.lower(),
        crop.lower(),
    ]
    if state:
        keywords.append(state.lower())

    # agricultural anchor words — boost if present
    agri_words = [
        "farmer", "farming", "agriculture", "crop", "rain", "drought",
        "msp", "price", "yield", "harvest", "kisan", "sowing", "irrigation",
        "pest", "fertilizer", "paddy", "wheat", "dal", "mandi", "produce"
    ]

    score = 0
    for kw in keywords:
        if kw in text:
            score += 3          # strong signal — exact place/crop match
    for aw in agri_words:
        if aw in text:
            score += 1          # weak signal — general agri relevance

    return score


def _fetch_news(query: str, max_results: int = 15) -> list[dict]:
    """Fetch and parse news articles from Google News RSS for a query."""
    url = _build_rss_url(query)
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries[:max_results]:
        articles.append({
            "title": entry.get("title", "No title").strip(),
            "url": entry.get("link", ""),
            "source": entry.get("source", {}).get("title", "Google News"),
            "published": _parse_published(entry),
            "summary": entry.get("summary", "")[:300],
            "score": 0,   # filled in later
        })
    return articles


# ─────────────────────────────────────────────
# MAIN FUNCTION
# ─────────────────────────────────────────────

def get_farmer_news(
    city: str,
    crop: str,
    state: Optional[str] = None,
    limit: int = 10,
    lang: str = "en-IN",
) -> list[dict]:
    """
    Fetch and rank agricultural news articles relevant to a specific farmer.

    Args:
        city  : Farmer's city or village (e.g. "Ongole", "Nashik")
        crop  : Farmer's crop (e.g. "rice", "cotton", "grapes")
        state : State name for broader coverage (e.g. "Andhra Pradesh")
        limit : Max number of articles to return (default 10)
        lang  : Language code for Google News (default "en-IN")

    Returns:
        List of dicts, each with keys:
        { title, url, source, published, summary, score }
        Sorted by relevance score (highest first).
    """
    if not city or not crop:
        raise ValueError("Both 'city' and 'crop' are required.")

    state_str = state or "India"

    # ── Query 1: Hyper-local — city + crop (most specific)
    q1 = f'"{crop}" farming "{city}"'

    # ── Query 2: State/national level crop news
    q2 = f'"{crop}" agriculture {state_str}'

    # ── Query 3: Local general agri news (broadest)
    q3 = f'agriculture farming "{city}" OR "{state_str}"'

    # ── Query 4: Crop-specific news India-wide (fallback for obscure cities)
    q4 = f'{crop} crop news India farmer'

    all_articles: list[dict] = []
    seen_urls: set[str] = set()

    for query in [q1, q2, q3, q4]:
        fetched = _fetch_news(query, max_results=15)
        for article in fetched:
            url = article["url"]
            if url and url not in seen_urls:
                seen_urls.add(url)
                # Score against farmer's context
                article["score"] = _score_article(
                    article["title"],
                    article["summary"],
                    city,
                    crop,
                    state_str,
                )
                all_articles.append(article)

    # Sort by relevance score (highest first), then by recency (fallback)
    all_articles.sort(key=lambda x: x["score"], reverse=True)

    # Return top N, always at least include some articles
    result = all_articles[:limit]

    # Strip internal summary field from output (it was only used for scoring)
    for article in result:
        del article["summary"]

    return result
