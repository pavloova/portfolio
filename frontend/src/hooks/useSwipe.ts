import { useRef, useCallback } from "react";

type Direction = "up" | "down" | "left" | "right";

interface SwipeHandlers {
  onTouchStart: (e: React.TouchEvent) => void;
  onTouchMove:  (e: React.TouchEvent) => void;
  onTouchEnd:   (e: React.TouchEvent) => void;
}

interface Options {
  onSwipe: (dir: Direction, deltaX: number, deltaY: number) => void;
  threshold?: number;   // px
}

export function useSwipe({ onSwipe, threshold = 50 }: Options): SwipeHandlers {
  const startX = useRef(0);
  const startY = useRef(0);

  const onTouchStart = useCallback((e: React.TouchEvent) => {
    startX.current = e.touches[0].clientX;
    startY.current = e.touches[0].clientY;
  }, []);

  const onTouchMove = useCallback((e: React.TouchEvent) => {
    // Prevent page scroll while swiping
    e.preventDefault();
  }, []);

  const onTouchEnd = useCallback((e: React.TouchEvent) => {
    const dx = e.changedTouches[0].clientX - startX.current;
    const dy = e.changedTouches[0].clientY - startY.current;
    const adx = Math.abs(dx);
    const ady = Math.abs(dy);

    if (adx < threshold && ady < threshold) return;   // tap, not swipe

    if (ady > adx) {
      onSwipe(dy < 0 ? "up" : "down", dx, dy);
    } else {
      onSwipe(dx < 0 ? "left" : "right", dx, dy);
    }
  }, [onSwipe, threshold]);

  return { onTouchStart, onTouchMove, onTouchEnd };
}
