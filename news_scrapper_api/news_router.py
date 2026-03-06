"""
news_router.py
--------------
FastAPI Router for the Farmer News Scraper API.

Endpoint:
    GET /news

Query Parameters:
    city   (required) : Farmer's city or village
    crop   (required) : Crop grown by the farmer
    state  (optional) : Farmer's state (improves regional relevance)
    limit  (optional) : Number of articles to return (default: 10, max: 30)
    lang   (optional) : Language code for Google News (default: "en-IN")

Response:
    {
      "query": { city, crop, state },
      "count": <int>,
      "articles": [
        { "title": "...", "url": "...", "source": "...", "published": "...", "score": <int> },
        ...
      ]
    }
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from news_api import get_farmer_news

router = APIRouter(prefix="/news", tags=["Farmer News"])


@router.get("/", summary="Get local & national agri-news for a farmer")
def fetch_news(
    city: str = Query(..., description="Farmer's city or village name", example="Ongole"),
    crop: str = Query(..., description="Crop the farmer is growing", example="rice"),
    state: Optional[str] = Query(None, description="State name for broader regional news", example="Andhra Pradesh"),
    limit: int = Query(10, ge=1, le=30, description="Max number of articles to return"),
    lang: str = Query("en-IN", description="Language code for Google News"),
):
    """
    Fetch agricultural news articles relevant to a specific farmer.

    - Combines **hyperlocal** (city + crop), **state-level**, and **national** news
    - Deduplicates articles across all sources
    - Ranks articles by relevance to the farmer's city and crop
    - Returns articles sorted from most to least relevant
    """
    try:
        articles = get_farmer_news(
            city=city.strip(),
            crop=crop.strip(),
            state=state.strip() if state else None,
            limit=limit,
            lang=lang,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"News fetch failed: {str(e)}")

    return {
        "query": {
            "city": city,
            "crop": crop,
            "state": state or "India (national)",
        },
        "count": len(articles),
        "articles": articles,
    }
