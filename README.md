# Фреймворк на FastAPI для быстрого старта

## В комплекте идет:  
1. Готовая OAuth2, JWT, Bearer авторизация  
2. Логирование через loguru  
3. Докер  
4. Модуль для работы с базой данных  

## Алгоритм развертки(*команды*):
1. ```docker-compose up -d```
2. ```docker-compose exec app bash```
3. ```alembic revision --autogenerate -m "create  user"```
4. ```alembic upgrade head```
5. ```exit```