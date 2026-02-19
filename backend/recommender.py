"""
Content-based recommendation engine with user feedback learning.

Scoring formula:
  score = topic_weight * W_TOPIC
         + tag_overlap  * W_TAG
         + engagement   * W_ENGAGEMENT
  Seen items are excluded; disliked items are heavily penalised.

content / content_map are passed in at call-time so the recommender works
with both static mock data and dynamically fetched YouTube content.
"""
from models import ContentItem, UserProfile

W_TOPIC      = 0.45
W_TAG        = 0.30
W_ENGAGEMENT = 0.15
W_RECENCY    = 0.10   # unused for static data, kept for real-API extension

# How much a single like/dislike shifts tag weights
LIKE_DELTA    =  0.20
DISLIKE_DELTA = -0.35
WATCH_DELTA   =  0.10   # per 10 % of video watched beyond 50 %
TOPIC_LIKE    =  0.15
TOPIC_DISLIKE = -0.25


def _engagement(item: ContentItem) -> float:
    """Normalised engagement ratio capped at 1."""
    if item.views == 0:
        return 0.0
    return min(item.likes / item.views * 10, 1.0)   # scale: 10 % likes ≈ 1.0


def _tag_score(item: ContentItem, tag_weights: dict[str, float]) -> float:
    if not item.tags or not tag_weights:
        return 0.0
    total = sum(tag_weights.get(t, 0.0) for t in item.tags)
    return max(0.0, min(total / len(item.tags), 1.0))


def score_item(item: ContentItem, profile: UserProfile) -> float:
    topic_w = profile.topic_weights.get(item.topic, 0.0)
    tag_w   = _tag_score(item, profile.tag_weights)
    eng     = _engagement(item)
    return (topic_w * W_TOPIC + tag_w * W_TAG + eng * W_ENGAGEMENT)


def get_feed(
    profile: UserProfile,
    content: list[ContentItem],
    limit: int = 10,
) -> list[ContentItem]:
    import random
    seen   = set(profile.liked_ids) | set(profile.disliked_ids)
    scored = []
    for item in content:
        if item.topic not in profile.selected_topics:
            continue
        if item.id in seen:
            continue
        scored.append((score_item(item, profile), item))

    # Descending score with a tiny random tie-breaker for exploration
    scored.sort(key=lambda x: x[0] + random.uniform(0, 0.05), reverse=True)
    results = [item for _, item in scored[:limit]]

    # Pad with unseen items if the scored list was too short
    if len(results) < limit:
        result_ids = {i.id for i in results}
        extras = [i for i in content
                  if i.id not in seen and i.id not in result_ids
                  and i.topic in profile.selected_topics]
        random.shuffle(extras)
        results += extras[: limit - len(results)]

    for item in results:
        item.score = round(score_item(item, profile), 4)
    return results


def apply_feedback(
    profile: UserProfile,
    content_id: str,
    action: str,
    watch_percent: float | None,
    content_map: dict[str, ContentItem],
) -> UserProfile:
    item = content_map.get(content_id)
    if item is None:
        return profile

    if action == "like":
        if content_id not in profile.liked_ids:
            profile.liked_ids.append(content_id)
        profile.disliked_ids = [i for i in profile.disliked_ids if i != content_id]
        # boost tags
        for tag in item.tags:
            profile.tag_weights[tag] = round(
                min(1.0, profile.tag_weights.get(tag, 0.0) + LIKE_DELTA), 4)
        # boost topic
        profile.topic_weights[item.topic] = round(
            min(1.0, profile.topic_weights.get(item.topic, 0.5) + TOPIC_LIKE), 4)

    elif action == "dislike":
        if content_id not in profile.disliked_ids:
            profile.disliked_ids.append(content_id)
        profile.liked_ids = [i for i in profile.liked_ids if i != content_id]
        for tag in item.tags:
            profile.tag_weights[tag] = round(
                max(-1.0, profile.tag_weights.get(tag, 0.0) + DISLIKE_DELTA), 4)
        profile.topic_weights[item.topic] = round(
            max(0.0, profile.topic_weights.get(item.topic, 0.5) + TOPIC_DISLIKE), 4)

    elif action == "watch" and watch_percent is not None:
        # Reward watching more than 50 %
        extra = max(0.0, watch_percent - 0.5) * 2   # 0..1
        delta = WATCH_DELTA * extra
        for tag in item.tags:
            profile.tag_weights[tag] = round(
                min(1.0, profile.tag_weights.get(tag, 0.0) + delta), 4)

    return profile


def build_default_profile(user_id: str, selected_topics: list[str]) -> UserProfile:
    topic_weights = {t: 1.0 for t in selected_topics}
    return UserProfile(
        user_id=user_id,
        selected_topics=selected_topics,
        liked_ids=[],
        disliked_ids=[],
        tag_weights={},
        topic_weights=topic_weights,
    )
