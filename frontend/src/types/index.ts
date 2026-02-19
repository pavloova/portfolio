export interface ContentItem {
  id: string;
  title: string;
  creator: string;
  topic: string;
  tags: string[];
  duration: number;
  views: number;
  likes: number;
  thumbnail_url: string;
  youtube_id: string;
  score: number;
}

export interface Topic {
  id: string;
  name: string;
  name_ru: string;
  icon: string;
}

export type FeedAction = "like" | "dislike" | "skip" | "watch";

export type Screen = "onboarding" | "feed" | "topics" | "settings";
