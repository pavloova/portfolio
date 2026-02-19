import { useState, useCallback, useEffect, useRef } from "react";
import type { ContentItem } from "../types";
import { VideoCard } from "./VideoCard";
import { useSwipe } from "../hooks/useSwipe";

interface Props {
  items: ContentItem[];
  onLike: (id: string) => void;
  onDislike: (id: string) => void;
  onLoadMore: () => void;
  loading: boolean;
}

export function FeedScreen({ items, onLike, onDislike, onLoadMore, loading }: Props) {
  const [index, setIndex] = useState(0);
  const [slideDir, setSlideDir] = useState<"up" | "down" | null>(null);
  const animating = useRef(false);

  const current = items[index];

  const goNext = useCallback(() => {
    if (animating.current || index >= items.length - 1) {
      if (index >= items.length - 1) onLoadMore();
      return;
    }
    animating.current = true;
    setSlideDir("up");
    setTimeout(() => {
      setIndex((i) => i + 1);
      setSlideDir(null);
      animating.current = false;
    }, 280);
    if (index >= items.length - 3) onLoadMore();
  }, [index, items.length, onLoadMore]);

  const goPrev = useCallback(() => {
    if (animating.current || index === 0) return;
    animating.current = true;
    setSlideDir("down");
    setTimeout(() => {
      setIndex((i) => i - 1);
      setSlideDir(null);
      animating.current = false;
    }, 280);
  }, [index]);

  // Reset index when a completely new feed arrives (topic change)
  useEffect(() => {
    setIndex(0);
    setSlideDir(null);
  }, [items[0]?.id]);

  const swipeHandlers = useSwipe({
    onSwipe: (dir) => {
      if (dir === "up")    goNext();
      if (dir === "down")  goPrev();
      if (dir === "right" && current) { onLike(current.id);    goNext(); }
      if (dir === "left"  && current) { onDislike(current.id); goNext(); }
    },
  });

  const openVideo = (item: ContentItem) => {
    const url = `https://www.youtube.com/shorts/${item.youtube_id}`;
    window.open(url, "_blank");
  };

  if (loading && items.length === 0) {
    return (
      <div className="feed-loading">
        <div className="spinner" />
        <p>Подбираем контент…</p>
      </div>
    );
  }

  if (!current) {
    return (
      <div className="feed-empty">
        <div className="empty-icon">🎬</div>
        <p>Весь контент просмотрен!</p>
        <p className="muted">Смени тему или сбрось историю в настройках</p>
      </div>
    );
  }

  return (
    <div className={`feed-screen ${slideDir ? `slide-${slideDir}` : ""}`}
         {...swipeHandlers}>
      <VideoCard
        key={current.id}
        item={current}
        isActive
        onLike={()    => { onLike(current.id);    goNext(); }}
        onDislike={() => { onDislike(current.id); goNext(); }}
        onOpen={()    => openVideo(current)}
      />

      {/* Progress dots */}
      <div className="progress-dots">
        {items.slice(Math.max(0, index - 2), index + 5).map((item, i) => {
          const real = Math.max(0, index - 2) + i;
          return (
            <div
              key={item.id}
              className={`dot ${real === index ? "active" : real < index ? "seen" : ""}`}
            />
          );
        })}
      </div>

      {/* Swipe hint (shown only on first card) */}
      {index === 0 && (
        <div className="swipe-hint">
          <span>↑ свайп вверх — следующее</span>
          <span>→ вправо — лайк</span>
        </div>
      )}
    </div>
  );
}
