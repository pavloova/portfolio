import type { Topic } from "../types";

interface Props {
  topics: Topic[];
  selected: string[];
  onToggle: (id: string) => void;
  onConfirm: () => void;
  isOnboarding?: boolean;
}

export function TopicSelector({ topics, selected, onToggle, onConfirm, isOnboarding }: Props) {
  return (
    <div className="topic-selector">
      <div className="topic-header">
        <h2>{isOnboarding ? "Выбери темы для развития" : "Мои темы"}</h2>
        <p className="topic-subtitle">
          {isOnboarding
            ? "Алгоритм будет подбирать контент на основе твоего выбора и реакций"
            : "Измени темы — алгоритм подстроится"}
        </p>
      </div>

      <div className="topics-grid">
        {topics.map((t) => (
          <button
            key={t.id}
            className={`topic-chip ${selected.includes(t.id) ? "selected" : ""}`}
            onClick={() => onToggle(t.id)}
          >
            <span className="topic-icon">{t.icon}</span>
            <span className="topic-name">{t.name_ru}</span>
            {selected.includes(t.id) && <span className="check">✓</span>}
          </button>
        ))}
      </div>

      <button
        className="confirm-btn"
        onClick={onConfirm}
        disabled={selected.length === 0}
      >
        {isOnboarding
          ? `Начать — ${selected.length} ${plural(selected.length, "тема", "темы", "тем")}`
          : "Сохранить"}
      </button>
    </div>
  );
}

function plural(n: number, one: string, few: string, many: string) {
  const mod10 = n % 10;
  const mod100 = n % 100;
  if (mod10 === 1 && mod100 !== 11) return one;
  if (mod10 >= 2 && mod10 <= 4 && !(mod100 >= 12 && mod100 <= 14)) return few;
  return many;
}
