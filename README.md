# Model Share - STL File Exchange Service

Повний Flask сервіс для обміну STL файлами. Навчальний проєкт першого курсу.

## Функціональність

- 👤 Реєстрація та вхід користувачів
- 📁 Завантаження STL файлів із назвою, описом і фото моделі
- 🗂️ Каталог усіх завантажених моделей
- 📥 Скачування STL файлів з підрахунком завантажень
- 🗑️ Видалення власних моделей автором
- 🙍 Особистий профіль із переліком власних завантажень

## Технічний стек

- **Backend**: Flask, Flask-Login, Flask-SQLAlchemy, Flask-WTF, Werkzeug
- **БД**: SQLite + SQLAlchemy ORM
- **Frontend**: HTML, Bootstrap 5
- **Python**: 3.8+

## Встановлення

1. Створи віртуальне середовище та активуй його:

```bash
python -m venv venv
source venv/bin/activate
```

2. Встанови залежності:

```bash
pip install -r requirements.txt
```

3. Запусти додаток:

```bash
python run.py
```

4. Відкрий браузер на `http://localhost:5000`

База даних SQLite створюється автоматично при першому запуску в файлі `app.db`.
Для production-оточення обов'язково задай змінну середовища `SECRET_KEY`.

## Маршрути

- `GET /` — каталог усіх моделей
- `GET, POST /register` — реєстрація
- `GET, POST /login` — вхід
- `GET /logout` — вихід
- `GET, POST /upload` — завантаження моделі
- `GET /profile` — профіль користувача
- `GET /model/<id>` — сторінка моделі
- `GET /download/<id>` — скачування STL
- `POST /delete/<id>` — видалення власної моделі
