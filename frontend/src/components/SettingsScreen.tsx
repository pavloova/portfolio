interface AlgorithmStats {
  liked: number;
  disliked: number;
  topTags: [string, number][];
}

interface Props {
  stats: AlgorithmStats;
  onResetProfile: () => void;
}

export function SettingsScreen({ stats, onResetProfile }: Props) {
  return (
    <div className="settings-screen">
      <h2 className="settings-title">Настройки</h2>

      <section className="settings-section">
        <h3>Алгоритм обучения</h3>
        <p className="settings-desc">
          Алгоритм запоминает твои лайки и дизлайки, анализирует теги и темы,
          чтобы улучшать подборку с каждым взаимодействием.
        </p>

        <div className="stats-row">
          <div className="stat-card">
            <div className="stat-value">❤️ {stats.liked}</div>
            <div className="stat-label">Лайков</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">👎 {stats.disliked}</div>
            <div className="stat-label">Скипов</div>
          </div>
        </div>
      </section>

      {stats.topTags.length > 0 && (
        <section className="settings-section">
          <h3>Топ тегов в профиле</h3>
          <div className="tag-weights">
            {stats.topTags.map(([tag, weight]) => (
              <div key={tag} className="tag-weight-row">
                <span className="tag-name">#{tag}</span>
                <div className="weight-bar-bg">
                  <div
                    className="weight-bar"
                    style={{ width: `${Math.max(0, weight) * 100}%` }}
                  />
                </div>
                <span className="weight-val">{weight.toFixed(2)}</span>
              </div>
            ))}
          </div>
        </section>
      )}

      <section className="settings-section">
        <h3>Сброс профиля</h3>
        <p className="settings-desc">
          Удалит историю лайков и веса тегов. Начнёшь с чистого листа.
        </p>
        <button className="reset-btn" onClick={onResetProfile}>
          Сбросить обучение
        </button>
      </section>

      <section className="settings-section about">
        <h3>О приложении</h3>
        <p className="settings-desc">
          <strong>ContentFlow</strong> — Telegram Mini App для обучения через
          короткий контент. Алгоритм использует content-based filtering с
          обучением на основе обратной связи.
        </p>
        <p className="settings-desc muted">v1.0.0 · FastAPI + React</p>
      </section>
    </div>
  );
}
