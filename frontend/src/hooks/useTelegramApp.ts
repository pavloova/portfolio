import { useEffect, useState } from "react";

declare global {
  interface Window {
    Telegram?: {
      WebApp: {
        initData: string;
        initDataUnsafe: {
          user?: { id: number; first_name: string; username?: string };
        };
        ready(): void;
        expand(): void;
        close(): void;
        enableClosingConfirmation(): void;
        BackButton: { show(): void; hide(): void; onClick(cb: () => void): void };
        HapticFeedback: {
          impactOccurred(style: "light" | "medium" | "heavy"): void;
          notificationOccurred(type: "success" | "warning" | "error"): void;
        };
        colorScheme: "light" | "dark";
        themeParams: Record<string, string>;
      };
    };
  }
}

export interface TelegramUser {
  id: string;
  firstName: string;
  username?: string;
}

export function useTelegramApp() {
  const tg = window.Telegram?.WebApp;
  const [userId, setUserId] = useState<string>("demo_user");
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    if (tg) {
      tg.ready();
      tg.expand();
      setIsDark(tg.colorScheme === "dark");

      const tgUser = tg.initDataUnsafe?.user;
      if (tgUser) {
        setUserId(String(tgUser.id));
      }
    }
  }, []);

  const haptic = (type: "light" | "medium" | "heavy" = "light") => {
    tg?.HapticFeedback?.impactOccurred(type);
  };

  const hapticNotify = (type: "success" | "warning" | "error") => {
    tg?.HapticFeedback?.notificationOccurred(type);
  };

  return { tg, userId, isDark, haptic, hapticNotify };
}
