import { useState, useEffect, useCallback } from "react";
import type { ContentItem, Topic, Screen } from "./types";
import { api } from "./api/client";

const DEMO_TOPICS: Topic[] = [
  { id: "tech",     name: "Technology",  name_ru: "Технологии",  icon: "💻" },
  { id: "science",  name: "Science",     name_ru: "Наука",       icon: "🔬" },
  { id: "business", name: "Business",    name_ru: "Бизнес",      icon: "📈" },
  { id: "design",   name: "Design",      name_ru: "Дизайн",      icon: "🎨" },
  { id: "history",  name: "History",     name_ru: "История",     icon: "🏛️" },
  { id: "health",   name: "Health",      name_ru: "Здоровье",    icon: "🧘" },
  { id: "language", name: "Languages",   name_ru: "Языки",       icon: "🌍" },
  { id: "math",     name: "Math",        name_ru: "Математика",  icon: "📐" },
];
import { useTelegramApp } from "./hooks/useTelegramApp";
import { FeedScreen } from "./components/FeedScreen";
import { TopicSelector } from "./components/TopicSelector";
import { SettingsScreen } from "./components/SettingsScreen";
import { BottomNav } from "./components/BottomNav";

export default function App() {
  const { userId, haptic, hapticNotify } = useTelegramApp();

  const [screen, setScreen]               = useState<Screen>("onboarding");
  const [topics, setTopics]               = useState<Topic[]>([]);
  const [selectedTopics, setSelectedTopics] = useState<string[]>([]);
  const [feed, setFeed]                   = useState<ContentItem[]>([]);
  const [loadingFeed, setLoadingFeed]     = useState(false);
  const [stats, setStats]                 = useState({ liked: 0, disliked: 0, topTags: [] as [string, number][] });

  // Load topics on mount
  useEffect(() => {
    api.getTopics().then(setTopics).catch(() => setTopics(DEMO_TOPICS));
    // Try to restore existing profile
    api.getProfile(userId).then((profile: any) => {
      if (profile.selected_topics?.length > 0) {
        setSelectedTopics(profile.selected_topics);
        setScreen("feed");
        refreshStats(profile);
      }
    }).catch(() => { /* first visit */ });
  }, [userId]);

  const refreshStats = (profile: any) => {
    const tagWeights: Record<string, number> = profile.tag_weights ?? {};
    const topTags = Object.entries(tagWeights)
      .filter(([, w]) => (w as number) > 0)
      .sort(([, a], [, b]) => (b as number) - (a as number))
      .slice(0, 8) as [string, number][];
    setStats({
      liked:    (profile.liked_ids ?? []).length,
      disliked: (profile.disliked_ids ?? []).length,
      topTags,
    });
  };

  const loadFeed = useCallback(async () => {
    if (loadingFeed || selectedTopics.length === 0) return;
    setLoadingFeed(true);
    try {
      const { items } = await api.getFeed(userId, 10);
      setFeed((prev) => {
        const existingIds = new Set(prev.map((i) => i.id));
        const fresh = items.filter((i) => !existingIds.has(i.id));
        return [...prev, ...fresh];
      });
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingFeed(false);
    }
  }, [userId, selectedTopics, loadingFeed]);

  // Load feed whenever topics are confirmed
  useEffect(() => {
    if (selectedTopics.length > 0 && screen === "feed") {
      setFeed([]);
      setTimeout(loadFeed, 0);
    }
  }, [selectedTopics, screen]);  // eslint-disable-line

  const handleTopicToggle = (id: string) => {
    haptic("light");
    setSelectedTopics((prev) =>
      prev.includes(id) ? prev.filter((t) => t !== id) : [...prev, id]
    );
  };

  const handleTopicsConfirm = async () => {
    haptic("medium");
    setFeed([]);
    setScreen("feed");
    await api.updatePreferences(userId, selectedTopics).catch(console.error);
  };

  const handleLike = async (id: string) => {
    hapticNotify("success");
    await api.sendFeedback(userId, id, "like").catch(console.error);
    const profile = await api.getProfile(userId).catch(() => null);
    if (profile) refreshStats(profile);
  };

  const handleDislike = async (id: string) => {
    haptic("medium");
    await api.sendFeedback(userId, id, "dislike").catch(console.error);
    const profile = await api.getProfile(userId).catch(() => null);
    if (profile) refreshStats(profile);
  };

  const handleResetProfile = async () => {
    haptic("heavy");
    // Re-init profile by updating preferences (backend creates fresh weights)
    await api.updatePreferences(userId, selectedTopics).catch(console.error);
    setFeed([]);
    setStats({ liked: 0, disliked: 0, topTags: [] });
    await loadFeed();
  };

  const handleScreenChange = (s: Screen) => {
    haptic("light");
    setScreen(s);
  };

  // ── Onboarding ─────────────────────────────────────────────────────────────
  if (screen === "onboarding") {
    return (
      <div className="app onboarding">
        <div className="onboarding-logo">
          <div className="logo-icon">▶</div>
          <h1 className="logo-title">ContentFlow</h1>
          <p className="logo-sub">Учись за минуту в день</p>
        </div>
        <TopicSelector
          topics={topics}
          selected={selectedTopics}
          onToggle={handleTopicToggle}
          onConfirm={handleTopicsConfirm}
          isOnboarding
        />
      </div>
    );
  }

  // ── Main app ───────────────────────────────────────────────────────────────
  return (
    <div className="app">
      <div className="screen-area">
        {screen === "feed" && (
          <FeedScreen
            items={feed}
            onLike={handleLike}
            onDislike={handleDislike}
            onLoadMore={loadFeed}
            loading={loadingFeed}
          />
        )}

        {screen === "topics" && (
          <div className="scrollable">
            <TopicSelector
              topics={topics}
              selected={selectedTopics}
              onToggle={handleTopicToggle}
              onConfirm={handleTopicsConfirm}
            />
          </div>
        )}

        {screen === "settings" && (
          <div className="scrollable">
            <SettingsScreen stats={stats} onResetProfile={handleResetProfile} />
          </div>
        )}
      </div>

      <BottomNav active={screen} onChange={handleScreenChange} />
    </div>
  );
}
