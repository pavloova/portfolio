import type { ContentItem, FeedAction, Topic } from "../types";

const BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
  return res.json() as Promise<T>;
}

export const api = {
  getTopics: (): Promise<Topic[]> =>
    request("/topics"),

  getProfile: (userId: string) =>
    request(`/user/${userId}/profile`),

  updatePreferences: (userId: string, topics: string[]) =>
    request("/user/preferences", {
      method: "PUT",
      body: JSON.stringify({ user_id: userId, selected_topics: topics }),
    }),

  getFeed: (userId: string, limit = 10): Promise<{ items: ContentItem[] }> =>
    request(`/feed/${userId}?limit=${limit}`),

  sendFeedback: (
    userId: string,
    contentId: string,
    action: FeedAction,
    watchPercent?: number
  ) =>
    request("/feedback", {
      method: "POST",
      body: JSON.stringify({
        user_id: userId,
        content_id: contentId,
        action,
        watch_percent: watchPercent ?? null,
      }),
    }),
};
