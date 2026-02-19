import { useState, useEffect, useCallback, useRef } from "react";
import type { ContentItem, Topic, Screen } from "./types";
import { api } from "./api/client";

const DEMO_POOL: ContentItem[] = [
  { id: "d1",  title: "Как работает интернет за 5 минут",   creator: "Kurzgesagt",   topic: "tech",    tags: ["сети","TCP/IP"],          duration: 305,  views: 12400000, likes: 890000,  thumbnail_url: "https://i.ytimg.com/vi/7_LPdttKXPc/hqdefault.jpg",  youtube_id: "7_LPdttKXPc",  score: 0.95 },
  { id: "d2",  title: "Теория относительности за 7 минут",  creator: "TED-Ed",       topic: "science", tags: ["физика","Эйнштейн"],        duration: 420,  views: 8700000,  likes: 560000,  thumbnail_url: "https://i.ytimg.com/vi/yuD34tEpRFw/hqdefault.jpg",  youtube_id: "yuD34tEpRFw",  score: 0.92 },
  { id: "d3",  title: "Почему мы прокрастинируем",          creator: "TED",          topic: "health",  tags: ["психология","продуктивность"], duration: 856, views: 55000000, likes: 1900000, thumbnail_url: "https://i.ytimg.com/vi/arj7oStGLkU/hqdefault.jpg",  youtube_id: "arj7oStGLkU",  score: 0.90 },
  { id: "d4",  title: "Как работает ИИ",                    creator: "3Blue1Brown",  topic: "tech",    tags: ["ML","нейросети"],           duration: 1200, views: 9800000,  likes: 720000,  thumbnail_url: "https://i.ytimg.com/vi/aircAruvnKk/hqdefault.jpg",  youtube_id: "aircAruvnKk",  score: 0.88 },
  { id: "d5",  title: "История денег",                      creator: "RealLifeLore", topic: "history", tags: ["экономика","деньги"],        duration: 730,  views: 3200000,  likes: 180000,  thumbnail_url: "https://i.ytimg.com/vi/YCN2aTlocOw/hqdefault.jpg",  youtube_id: "YCN2aTlocOw",  score: 0.85 },
  { id: "d6",  title: "Чёрные дыры объяснены",              creator: "Kurzgesagt",   topic: "science", tags: ["космос","физика"],           duration: 480,  views: 23000000, likes: 1400000, thumbnail_url: "https://i.ytimg.com/vi/e-P5IFTqB98/hqdefault.jpg",  youtube_id: "e-P5IFTqB98",  score: 0.87 },
  { id: "d7",  title: "Как выучить любой язык",             creator: "Lýdie Barani", topic: "language",tags: ["языки","обучение"],          duration: 652,  views: 6100000,  likes: 320000,  thumbnail_url: "https://i.ytimg.com/vi/HZqUeWshwMs/hqdefault.jpg",  youtube_id: "HZqUeWshwMs",  score: 0.86 },
  { id: "d8",  title: "Мозг во сне",                        creator: "SciShow",      topic: "health",  tags: ["сон","мозг"],                duration: 540,  views: 4500000,  likes: 210000,  thumbnail_url: "https://i.ytimg.com/vi/i2vEBMmArxo/hqdefault.jpg",  youtube_id: "i2vEBMmArxo",  score: 0.84 },
  { id: "d9",  title: "Визуализация сортировок",            creator: "AlgoVision",   topic: "tech",    tags: ["алгоритмы","код"],           duration: 290,  views: 2800000,  likes: 190000,  thumbnail_url: "https://i.ytimg.com/vi/kPRA0W1kECg/hqdefault.jpg",  youtube_id: "kPRA0W1kECg",  score: 0.83 },
  { id: "d10", title: "Краткая история Вселенной",          creator: "PBS Space Time",topic: "science",tags: ["космология","Big Bang"],     duration: 810,  views: 7200000,  likes: 430000,  thumbnail_url: "https://i.ytimg.com/vi/HdPzOWlLrbE/hqdefault.jpg",  youtube_id: "HdPzOWlLrbE",  score: 0.82 },
  { id: "d11", title: "Как работает биткоин",               creator: "3Blue1Brown",  topic: "tech",    tags: ["крипто","блокчейн"],         duration: 924,  views: 10300000, likes: 680000,  thumbnail_url: "https://i.ytimg.com/vi/bBC-nXj3Ng4/hqdefault.jpg",  youtube_id: "bBC-nXj3Ng4",  score: 0.81 },
  { id: "d12", title: "Стоицизм за 5 минут",                creator: "SciShow Psych",topic: "health",  tags: ["философия","психология"],    duration: 360,  views: 3100000,  likes: 175000,  thumbnail_url: "https://i.ytimg.com/vi/R9OCA6UFE-0/hqdefault.jpg",  youtube_id: "R9OCA6UFE-0",  score: 0.80 },
  { id: "d13", title: "Как мозг учится",                    creator: "Sprouts",      topic: "health",  tags: ["нейронауки","обучение"],     duration: 415,  views: 5600000,  likes: 290000,  thumbnail_url: "https://i.ytimg.com/vi/X96oQs4gBk8/hqdefault.jpg",  youtube_id: "X96oQs4gBk8",  score: 0.79 },
  { id: "d14", title: "История холодной войны",             creator: "Overly Sarcastic", topic: "history", tags: ["история","политика"],  duration: 990,  views: 4800000,  likes: 260000,  thumbnail_url: "https://i.ytimg.com/vi/I79TpDe3t2g/hqdefault.jpg",  youtube_id: "I79TpDe3t2g",  score: 0.78 },
  { id: "d15", title: "Квантовые вычисления за 8 минут",    creator: "Kurzgesagt",   topic: "tech",    tags: ["квантовые","вычисления"],    duration: 490,  views: 14600000, likes: 910000,  thumbnail_url: "https://i.ytimg.com/vi/JhHMJCUmq28/hqdefault.jpg",  youtube_id: "JhHMJCUmq28",  score: 0.77 },
];

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

const DEMO_BATCH = 5;

export default function App() {
  const { userId, haptic, hapticNotify } = useTelegramApp();

  const [screen, setScreen]               = useState<Screen>("onboarding");
  const [topics, setTopics]               = useState<Topic[]>([]);
  const [selectedTopics, setSelectedTopics] = useState<string[]>([]);
  const [feed, setFeed]                   = useState<ContentItem[]>([]);
  const [loadingFeed, setLoadingFeed]     = useState(false);
  const [stats, setStats]                 = useState({ liked: 0, disliked: 0, topTags: [] as [string, number][] });
  const demoOffset = useRef(0);

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
      const offset = demoOffset.current % DEMO_POOL.length;
      const batch = [...DEMO_POOL, ...DEMO_POOL]
        .slice(offset, offset + DEMO_BATCH)
        .map((item, i) => ({ ...item, id: `${item.id}_${demoOffset.current + i}` }));
      demoOffset.current += DEMO_BATCH;
      setFeed((prev) => {
        const existingIds = new Set(prev.map((i) => i.id));
        return [...prev, ...batch.filter((i) => !existingIds.has(i.id))];
      });
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
    demoOffset.current = 0;
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
    demoOffset.current = 0;
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
