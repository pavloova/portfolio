import { useState, useRef, useEffect } from "react";
import type { ContentItem } from "../types";

interface Props {
  item: ContentItem;
  isActive: boolean;
  onLike: () => void;
  onDislike: () => void;
  onOpen: () => void;
}

function formatViews(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000)     return `${(n / 1_000).toFixed(0)}K`;
  return String(n);
}

function formatDuration(s: number): string {
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

export function VideoCard({ item, isActive, onLike, onDislike, onOpen }: Props) {
  const [liked, setLiked]       = useState(false);
  const [disliked, setDisliked] = useState(false);
  const [showFeedback, setShowFeedback] = useState<"like" | "dislike" | null>(null);
  const feedbackTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Reset state when card changes
  useEffect(() => {
    setLiked(false);
    setDisliked(false);
    setShowFeedback(null);
  }, [item.id]);

  const flash = (type: "like" | "dislike") => {
    setShowFeedback(type);
    if (feedbackTimer.current) clearTimeout(feedbackTimer.current);
    feedbackTimer.current = setTimeout(() => setShowFeedback(null), 800);
  };

  const handleLike = () => {
    setLiked(true);
    setDisliked(false);
    flash("like");
    onLike();
  };

  const handleDislike = () => {
    setDisliked(true);
    setLiked(false);
    flash("dislike");
    onDislike();
  };

  const youtubeThumb = `https://img.youtube.com/vi/${item.youtube_id}/hqdefault.jpg`;

  return (
    <div className={`video-card ${isActive ? "active" : ""}`}>
      {/* Thumbnail */}
      <div className="video-thumb" onClick={onOpen}>
        <img
          src={item.thumbnail_url}
          alt={item.title}
          onError={(e) => {
            (e.currentTarget as HTMLImageElement).src = youtubeThumb;
          }}
          loading="lazy"
        />
        <div className="play-overlay">
          <div className="play-icon">▶</div>
        </div>
        <div className="duration-badge">{formatDuration(item.duration)}</div>
      </div>

      {/* Feedback overlay */}
      {showFeedback && (
        <div className={`feedback-overlay ${showFeedback}`}>
          {showFeedback === "like" ? "❤️" : "👎"}
        </div>
      )}

      {/* Action sidebar */}
      <div className="action-sidebar">
        <button
          className={`action-btn ${liked ? "active-like" : ""}`}
          onClick={handleLike}
          aria-label="Нравится"
        >
          <span className="action-icon">{liked ? "❤️" : "🤍"}</span>
          <span className="action-label">{formatViews(item.likes)}</span>
        </button>

        <button
          className={`action-btn ${disliked ? "active-dislike" : ""}`}
          onClick={handleDislike}
          aria-label="Не нравится"
        >
          <span className="action-icon">👎</span>
          <span className="action-label">Скип</span>
        </button>

        <button className="action-btn" onClick={onOpen} aria-label="Открыть">
          <span className="action-icon">▶️</span>
          <span className="action-label">Смотреть</span>
        </button>
      </div>

      {/* Meta info */}
      <div className="video-meta">
        <div className="creator">@{item.creator}</div>
        <div className="video-title">{item.title}</div>
        <div className="tags">
          {item.tags.slice(0, 3).map((t) => (
            <span key={t} className="tag">#{t}</span>
          ))}
        </div>
        <div className="stats">
          <span>👁 {formatViews(item.views)}</span>
          <span className="score-badge">
            {Math.round(item.score * 100)}% match
          </span>
        </div>
      </div>
    </div>
  );
}
