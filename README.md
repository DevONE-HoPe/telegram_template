# Шаблон простого Telegram-бота на aiogram

## Описание

Тестовое задание: привести устаревший проект к нормальной архитектуре, заменить Peewee на SQLAlchemy, внедрить Alembic, обновить Python и aiogram до актуальной версии.

## Используемые технологии

- **aiogram** — фреймворк для Telegram-ботов
- **SQLAlchemy** — ORM для работы с базой данных
- **Alembic** — инструмент для миграций базы данных
- **asyncpg** — асинхронный драйвер для работы с PostgreSQL
- **psycopg2-binary** — синхронный драйвер PostgreSQL для Alembic
- **aioschedule** — планировщик задач для ежедневных уведомлений о статусе бота
- **Redis** — кэширование и хранение состояний
- **PostgreSQL** — основная база данных

## Инструкции по установке

Требуется Docker. Настройте файл `.env.example`, указав нужные данные.

Далее `make start_docker` запускает:

```yaml
postgres:
  image: postgres:14-alpine
  container_name: ${COMPOSE_PROJECT_NAME}-postgres
  restart: always
  env_file:
    - .env
  environment:
    - POSTGRES_USER=${DB_USER}
    - POSTGRES_PASSWORD=${DB_PASS}
    - POSTGRES_DB=${DB_NAME}
    - PGDATA='/var/lib/postgresql/data/pgdata'
  networks:
    - app
  volumes:
    - postgres-data:/var/lib/postgresql/data
  ports:
    - "5432:5432"

redis:
  image: redis:7-alpine
  container_name: ${COMPOSE_PROJECT_NAME}-redis
  restart: always
  env_file:
    - .env
  ports:
    - "6379:6379"
  networks:
    - app
  volumes:
    - redis-data:/bitnami/redis/data
  command: /bin/sh -c 'if [ -n "$REDIS_PASS" ]; then redis-server --requirepass "$REDIS_PASS"; else redis-server; fi'

bot:
  build:
    context: .
    dockerfile: ./Dockerfile
  image: bot:latest
  container_name: tg_bot_template
  restart: always
  env_file:
    - .env
  networks:
    - app
  depends_on:
    - postgres
    - redis
```

## Файловая структура

```
.
├── .dockerignore
├── alembic.ini
├── logs/
│   └── TGbot_template.log
├── .gitignore
├── .env.example
├── pyproject.toml
├── README.md
├── migrations/
│   ├── README
│   ├── script.py.mako
│   ├── versions/
│   │   └── 2f955a0075e0_create_users_table.py
│   └── env.py
├── tg_bot_template/
│   ├── __main__.py
│   ├── services/
│   │   ├── users.py
│   │   └── __init__.py
│   ├── states/
│   │   ├── states.py
│   │   └── __init__.py
│   ├── filters/
│   │   ├── __init__.py
│   │   └── admin.py
│   ├── handlers/
│   │   ├── cancel.py
│   │   ├── start.py
│   │   ├── all_message.py
│   │   ├── tap_handler.py
│   │   ├── profile.py
│   │   ├── top.py
│   │   ├── start_game.py
│   │   ├── __init__.py
│   │   ├── help.py
│   │   └── admin.py
│   ├── middlewares/
│   │   ├── auth.py
│   │   ├── database.py
│   │   └── __init__.py
│   ├── keyboards/
│   │   ├── reply/
│   │   │   ├── cancel.py
│   │   │   ├── menu.py
│   │   │   └── __init__.py
│   │   ├── default_commands.py
│   │   ├── __init__.py
│   │   └── inline/
│   │       ├── click.py
│   │       ├── menu.py
│   │       └── __init__.py
│   ├── database/
│   │   ├── models/
│   │   │   ├── base.py
│   │   │   ├── user.py
│   │   │   └── __init__.py
│   │   ├── database.py
│   │   └── __init__.py
│   ├── core/
│   │   ├── loader.py
│   │   ├── config.py
│   │   └── __init__.py
│   └── cache/
│       ├── redis.py
│       ├── __init__.py
│       └── serialization.py
├── uv.lock
├── Dockerfile
├── .env
├── docker-compose.yml
├── .python-version
└── Makefile
```