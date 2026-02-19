"""
YouTube Data API v3 — fetching real Shorts by topic.

Quota cost per topic refresh:
  search.list  → 100 units
  videos.list  → 1 unit × ceil(results/50)
  ≈ 101 units per topic, ~808 units for all 8 topics.
Daily free quota: 10 000 units.
"""
import os
import re
import time
import logging

import httpx

from models import ContentItem

logger = logging.getLogger(__name__)

YT_BASE = "https://www.googleapis.com/youtube/v3"

# Search queries per topic (English gives the broadest Shorts catalogue)
TOPIC_QUERIES: dict[str, str] = {
    "programming":  "programming coding tutorial",
    "economics":    "economics explained",
    "investing":    "investing finance stocks",
    "psychology":   "psychology mind brain",
    "productivity": "productivity study tips",
    "science":      "science facts",
    "languages":    "language learning",
    "fitness":      "fitness workout",
}

# Simple in-memory cache {topic_id: (fetched_at, items)}
_cache: dict[str, tuple[float, list[ContentItem]]] = {}
CACHE_TTL = 6 * 3600   # 6 hours — well within daily quota budget


def _parse_duration(iso: str) -> int:
    """Convert ISO 8601 duration (PT1M30S) → seconds."""
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m:
        return 60
    return int(m.group(1) or 0) * 3600 + int(m.group(2) or 0) * 60 + int(m.group(3) or 0)


async def fetch_shorts(topic_id: str, max_results: int = 20) -> list[ContentItem]:
    """Fetch YouTube Shorts for *topic_id*. Returns cached data if fresh."""
    api_key = os.getenv("YOUTUBE_API_KEY", "")
    if not api_key:
        logger.warning("YOUTUBE_API_KEY not set — skipping YouTube fetch for '%s'", topic_id)
        return []

    # Return cached result if still fresh
    if topic_id in _cache:
        fetched_at, cached_items = _cache[topic_id]
        if time.time() - fetched_at < CACHE_TTL:
            logger.debug("Cache hit for topic '%s' (%d items)", topic_id, len(cached_items))
            return cached_items

    query = TOPIC_QUERIES.get(topic_id, topic_id)
    logger.info("Fetching YouTube Shorts for topic '%s' (query: '%s')", topic_id, query)

    async with httpx.AsyncClient(timeout=15.0) as client:
        # ── Step 1: search ────────────────────────────────────────────────────
        search_resp = await client.get(f"{YT_BASE}/search", params={
            "part":             "snippet",
            "q":                query,
            "type":             "video",
            "videoDuration":    "short",    # <4 min (Shorts are ≤60s/3min)
            "maxResults":       max_results,
            "key":              api_key,
            "relevanceLanguage": "en",
            "safeSearch":       "moderate",
        })
        search_resp.raise_for_status()

        video_ids = [
            item["id"]["videoId"]
            for item in search_resp.json().get("items", [])
            if item.get("id", {}).get("videoId")
        ]
        if not video_ids:
            logger.warning("No videos found for topic '%s'", topic_id)
            return []

        # ── Step 2: video details (stats + contentDetails) ────────────────────
        videos_resp = await client.get(f"{YT_BASE}/videos", params={
            "part": "snippet,statistics,contentDetails",
            "id":   ",".join(video_ids),
            "key":  api_key,
        })
        videos_resp.raise_for_status()

    items: list[ContentItem] = []
    for v in videos_resp.json().get("items", []):
        vid_id   = v["id"]
        snippet  = v["snippet"]
        stats    = v.get("statistics", {})
        duration = _parse_duration(v.get("contentDetails", {}).get("duration", "PT60S"))

        # Shorts are ≤3 min; skip longer videos that leaked through the filter
        if duration > 180:
            continue

        views = int(stats.get("viewCount", 0))
        likes = int(stats.get("likeCount", 0))

        # Use YouTube tags if available, otherwise fall back to topic id
        raw_tags = snippet.get("tags", [])[:6]
        tags = [t.lower().replace(" ", "-") for t in raw_tags] if raw_tags else [topic_id]

        thumb = (
            snippet["thumbnails"].get("maxres")
            or snippet["thumbnails"].get("high")
            or snippet["thumbnails"].get("default")
            or {}
        ).get("url", f"https://img.youtube.com/vi/{vid_id}/hqdefault.jpg")

        items.append(ContentItem(
            id=f"yt_{vid_id}",
            title=snippet["title"][:100],
            creator=snippet["channelTitle"],
            topic=topic_id,
            tags=tags,
            duration=duration,
            views=views,
            likes=likes,
            thumbnail_url=thumb,
            youtube_id=vid_id,
            score=0.0,
        ))

    logger.info("Fetched %d Shorts for topic '%s'", len(items), topic_id)
    _cache[topic_id] = (time.time(), items)
    return items


def invalidate(topic_id: str | None = None) -> None:
    """Clear cache for one topic or all topics."""
    if topic_id:
        _cache.pop(topic_id, None)
    else:
        _cache.clear()
