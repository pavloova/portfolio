from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import FeedbackRequest, PreferencesUpdate, UserProfile
from data import TOPICS, CONTENT_MAP
from recommender import get_feed, apply_feedback, build_default_profile

app = FastAPI(title="Content Curator API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory user store (replace with DB in production)
_users: dict[str, UserProfile] = {}


def _get_or_create(user_id: str) -> UserProfile:
    if user_id not in _users:
        _users[user_id] = build_default_profile(user_id, [])
    return _users[user_id]


# ── Topics ────────────────────────────────────────────────────────────────────

@app.get("/topics")
def list_topics():
    return TOPICS


# ── User preferences ──────────────────────────────────────────────────────────

@app.get("/user/{user_id}/profile")
def get_profile(user_id: str):
    return _get_or_create(user_id)


@app.put("/user/preferences")
def update_preferences(body: PreferencesUpdate):
    profile = _get_or_create(body.user_id)
    profile.selected_topics = body.selected_topics
    # Ensure every selected topic has at least a baseline weight
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
    items = get_feed(profile, limit=limit)
    return {"items": items, "count": len(items)}


# ── Feedback ──────────────────────────────────────────────────────────────────

@app.post("/feedback")
def post_feedback(body: FeedbackRequest):
    if body.action not in ("like", "dislike", "skip", "watch"):
        raise HTTPException(status_code=422, detail="Unknown action")
    if body.content_id not in CONTENT_MAP:
        raise HTTPException(status_code=404, detail="Content not found")
    profile = _get_or_create(body.user_id)
    updated = apply_feedback(profile, body.content_id,
                             body.action, body.watch_percent)
    _users[body.user_id] = updated
    return {"status": "ok"}


# ── Health ────────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "healthy", "users": len(_users)}
