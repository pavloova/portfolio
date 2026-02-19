from pydantic import BaseModel
from typing import Optional


class ContentItem(BaseModel):
    id: str
    title: str
    creator: str
    topic: str
    tags: list[str]
    duration: int          # seconds
    views: int
    likes: int
    thumbnail_url: str
    youtube_id: str
    score: float = 0.0


class Topic(BaseModel):
    id: str
    name: str
    name_ru: str
    icon: str


class FeedbackRequest(BaseModel):
    user_id: str
    content_id: str
    action: str            # "like" | "dislike" | "skip" | "watch"
    watch_percent: Optional[float] = None   # 0.0 – 1.0


class PreferencesUpdate(BaseModel):
    user_id: str
    selected_topics: list[str]


class UserProfile(BaseModel):
    user_id: str
    selected_topics: list[str]
    liked_ids: list[str]
    disliked_ids: list[str]
    tag_weights: dict[str, float]
    topic_weights: dict[str, float]
