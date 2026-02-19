import type { Screen } from "../types";

interface Props {
  active: Screen;
  onChange: (s: Screen) => void;
}

const items: { id: Screen; icon: string; label: string }[] = [
  { id: "feed",     icon: "▶️",  label: "Лента"     },
  { id: "topics",   icon: "🎯",  label: "Темы"      },
  { id: "settings", icon: "⚙️",  label: "Настройки" },
];

export function BottomNav({ active, onChange }: Props) {
  return (
    <nav className="bottom-nav">
      {items.map(({ id, icon, label }) => (
        <button
          key={id}
          className={`nav-item ${active === id ? "active" : ""}`}
          onClick={() => onChange(id)}
        >
          <span className="nav-icon">{icon}</span>
          <span className="nav-label">{label}</span>
        </button>
      ))}
    </nav>
  );
}
