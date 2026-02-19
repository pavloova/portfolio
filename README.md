# portfolio
Портфолио с моими работами.
На каждом branch расположен код, относящийся к определённому проекту:
- TG Bot python
- Проекты по численным методам на с++
- Зоны обитаемости python
- Мини проекты с анимацией на python
- **ContentFlow — Telegram Mini App** (этот branch)

---

# ContentFlow — Telegram Mini App

Мини-приложение для Telegram, которое собирает персональную подборку короткого контента (YouTube Shorts) по выбранным темам развития и обучает алгоритм на основе реакций пользователя.

## Фичи

- **Вертикальный свайп** — листай контент как в TikTok / Reels
- **Жесты**: свайп вверх/вниз — следующий/предыдущий, вправо — лайк, влево — дизлайк
- **Выбор тем**: Программирование, Экономика, Инвестиции, Психология, Продуктивность, Наука, Языки, Фитнес
- **Алгоритм обучения**: content-based filtering с обновлением весов тегов и тем на основе лайков, дизлайков и глубины просмотра
- **Профиль пользователя**: визуализация весов тегов, статистика взаимодействий, сброс обучения
- **Telegram-нативность**: haptic feedback, тема Telegram (цвета), `initData` для идентификации пользователя

## Стек

| Слой      | Технологии |
|-----------|-----------|
| Frontend  | React 18 + TypeScript, Vite, `@twa-dev/sdk` |
| Backend   | Python 3.12, FastAPI, Pydantic v2 |
| Деплой    | Docker + docker-compose, Nginx |

## Структура проекта

```
├── backend/
│   ├── main.py          # FastAPI endpoints
│   ├── recommender.py   # алгоритм рекомендаций
│   ├── data.py          # mock-контент (30+ видео, 8 тем)
│   ├── models.py        # Pydantic схемы
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/  # FeedScreen, VideoCard, TopicSelector, SettingsScreen
│   │   ├── hooks/       # useSwipe, useTelegramApp
│   │   ├── api/         # HTTP клиент
│   │   └── styles/
│   └── Dockerfile
└── docker-compose.yml
```

## API

| Метод | Путь | Описание |
|-------|------|----------|
| GET   | `/topics`             | Список тем |
| GET   | `/user/{id}/profile`  | Профиль пользователя |
| PUT   | `/user/preferences`   | Обновить выбранные темы |
| GET   | `/feed/{id}`          | Персональная лента |
| POST  | `/feedback`           | Отправить реакцию (like/dislike/skip/watch) |

## Запуск

```bash
# Разработка
cd backend  && uvicorn main:app --reload
cd frontend && npm install && npm run dev

# Продакшн
docker-compose up --build
```

## Алгоритм рекомендаций

```
score = topic_weight × 0.45
      + tag_overlap  × 0.30
      + engagement   × 0.15

Лайк    → +0.20 к весам тегов, +0.15 к весу темы
Дизлайк → −0.35 к весам тегов, −0.25 к весу темы
Просмотр > 50% → пропорциональный буст тегов
```
Просмотренные и дизлайкнутые видео исключаются из ленты.
