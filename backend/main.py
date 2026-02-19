"""
ContentFlow API — FastAPI backend.

On startup the server tries to fetch real YouTube Shorts for every topic.
If YOUTUBE_API_KEY is not set (or the request fails), mock data is used
as a fallback so the app always works even without credentials.
"""
import asyncio
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from data import CONTENT as MOCK_CONTENT, CONTENT_MAP as MOCK_CONTENT_MAP, TOPICS, TOPICS_MAP
from models import ContentItem, FeedbackRequest, PreferencesUpdate, UserProfile
from recommender import apply_feedback, build_default_profile, get_feed
from youtube import fetch_shorts

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Dynamic content store ─────────────────────────────────────────────────────
# Populated on startup; falls back to MOCK_CONTENT when YouTube is unavailable.
_content: list[ContentItem] = []
_content_map: dict[str, ContentItem] = {}


def _rebuild_map() -> None:
    global _content_map
    _content_map = {item.id: item for item in _content}


async def _load_youtube_content() -> None:
    """Fetch Shorts for all topics concurrently and merge into _content."""
    global _content

    api_key = os.getenv("YOUTUBE_API_KEY", "")
    if not api_key:
        logger.warning("YOUTUBE_API_KEY not set — using mock data only")
        _content = list(MOCK_CONTENT)
        _rebuild_map()
        return

    tasks = [fetch_shorts(topic.id) for topic in TOPICS]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    yt_items: list[ContentItem] = []
    for topic, result in zip(TOPICS, results):
        if isinstance(result, Exception):
            logger.error("YouTube fetch failed for '%s': %s", topic.id, result)
        else:
            yt_items.extend(result)

    if yt_items:
        # Merge: real YouTube content first, mock as fallback for any topic
        # that returned 0 results
        covered = {item.topic for item in yt_items}
        fallback = [i for i in MOCK_CONTENT if i.topic not in covered]
        _content = yt_items + fallback
        logger.info("Content store: %d YouTube + %d mock items", len(yt_items), len(fallback))
    else:
        logger.warning("All YouTube fetches failed — using mock data")
        _content = list(MOCK_CONTENT)

    _rebuild_map()


# ── Lifespan (replaces deprecated @app.on_event) ─────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    await _load_youtube_content()
    yield   # app runs here


app = FastAPI(title="ContentFlow API", version="1.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── In-memory user store ──────────────────────────────────────────────────────
_users: dict[str, UserProfile] = {}


def _get_or_create(user_id: str) -> UserProfile:
    if user_id not in _users:
        _users[user_id] = build_default_profile(user_id, [])
    return _users[user_id]


# ── Topics ────────────────────────────────────────────────────────────────────

@app.get("/topics")
def list_topics():
    return TOPICS


# ── User ──────────────────────────────────────────────────────────────────────

@app.get("/user/{user_id}/profile")
def get_profile(user_id: str):
    return _get_or_create(user_id)


@app.put("/user/preferences")
def update_preferences(body: PreferencesUpdate):
    profile = _get_or_create(body.user_id)
    profile.selected_topics = body.selected_topics
    for t in body.selected_topics:
        if t not in profile.topic_weights:
            profile.topic_weights[t] = 1.0
    return {"status": "ok", "profile": profile}


# ── Feed ──────────────────────────────────────────────────────────────────────

@app.get("/feed/{user_id}")
def get_user_feed(user_id: str, limit: int = 10):
    profile = _get_or_create(user_id)
    if not profile.selected_topics:
        raise HTTPException(status_code=400, detail="No topics selected")
    items = get_feed(profile, _content, limit=limit)
    return {"items": items, "count": len(items)}


# ── Feedback ──────────────────────────────────────────────────────────────────

@app.post("/feedback")
def post_feedback(body: FeedbackRequest):
    if body.action not in ("like", "dislike", "skip", "watch"):
        raise HTTPException(status_code=422, detail="Unknown action")

    # Check both dynamic and mock stores
    if body.content_id not in _content_map and body.content_id not in MOCK_CONTENT_MAP:
        raise HTTPException(status_code=404, detail="Content not found")

    # Merge maps so feedback always resolves
    merged_map = {**MOCK_CONTENT_MAP, **_content_map}

    profile = _get_or_create(body.user_id)
    updated = apply_feedback(profile, body.content_id,
                             body.action, body.watch_percent, merged_map)
    _users[body.user_id] = updated
    return {"status": "ok"}


# ── Admin ─────────────────────────────────────────────────────────────────────

@app.post("/admin/refresh")
async def refresh_content():
    """Force-refresh the YouTube content cache (admin use)."""
    from youtube import invalidate
    invalidate()
    await _load_youtube_content()
    return {"status": "ok", "total_items": len(_content)}


# ── Health ────────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "users": len(_users),
        "content_items": len(_content),
        "youtube_enabled": bool(os.getenv("YOUTUBE_API_KEY")),
    }
