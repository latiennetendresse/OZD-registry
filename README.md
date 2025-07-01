# Асинхронное REST API для управления справочником организаций, зданий и видов деятельности.

## Стэк
- Python 3.11
- FastAPI
- SQLAlchemy(async)
- Alembic
- Pydantic
- PostgreSQL + asyncpg
- Poetry
- Docker, Docker Compose


## Функционал
- CRUD для зданий и видов деятельности
- Создание и поиск организаций:
  - По зданию
  - По виду деятельности (включая вложенные)
  - По геозоне (радиус/прямоугольник)
  - По названию
  - Авторизация через Bearer-токен в заголовке `Authorization`


## Запуск
1. Скопировать `.env.example` в `.env` и заполнить.
2. `docker-compose up --build`
3. Swagger UI: http://localhost:8000/api/v1/docs  


## Заполнение БД демо-данными
```bash
docker compose exec app python -m app.scripts.demo_data