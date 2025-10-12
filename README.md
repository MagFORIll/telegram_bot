# Telegram Car Bot

Телеграм-бот для подбора автомобилей по вашим предпочтениям.  
Хранит данные пользователей в PostgreSQL и парсит актуальные предложения с сайтов автообъявлений.

---

## Технологии

- Python 3.11+
- aiogram
- SQLAlchemy
- PostgreSQL
- Docker
- BeautifulSoup4 (для парсинга)

---

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/your-username/car-bot.git
cd car-bot
```
### 2. Создание виртуального окружения
```bash
python -m venv venv
source venv/bin/activate     # для macOS/Linux
venv\Scripts\activate        # для Windows
```
### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```
### 4. Настройка окружения
```
Создайте файл .env со своими переменными:

env
BOT_TOKEN=ваш_токен_телеграм
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/carbot_db
```
### 5. Запуск PostgreSQL через Docker
```bash
docker run --name carbot_postgres -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=carbot_db -p 5432:5432 -d postgres
```
### 6. Запуск бота
```bash
python main.py
```
### Функционал
 Регистрация пользователя (по Telegram ID)
 Сохранение предпочтений (бренд, модель, год, цена)
 Просмотр сохранённых предпочтений
 Поиск автомобилей по фильтрам
 Хранение данных в PostgreSQL

#### Планы по доработке
Добавить асинхронный парсер auto.ru
Добавить логирование и тесты (pytest)
Улучшить структуру проекта (Blueprint-style API для backend)
