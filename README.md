# Model Share - STL File Exchange Service

Простий сервіс для обміну STL файлами на Flask + Python. Навчальний проєкт для першого курсу.

## Функціональність

- 📁 Завантаження STL файлів
- 📸 Додавання фото моделей (опціонально)
- 📝 Опис моделей (опціонально)
- 👥 Реєстрація та вхід користувачів
- 💾 Скачування файлів
- 🗑️ Видалення власних файлів

## Технічний стек

- **Backend**: Flask, Flask-Login, Flask-SQLAlchemy
- **БД**: SQLite
- **Frontend**: HTML, Bootstrap 5
- **Python**: 3.8+

## Встановлення

1. Клонуй репозиторій:
```bash
git clone https://github.com/yevhenii-khokhlov/model-share.git
cd model-share
```

2. Створи віртуальне середовище:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# або
venv\Scripts\activate  # Windows
```

3. Встанови залежності:
```bash
pip install -r requirements.txt
```

4. Запусти додаток:
```bash
python run.py
```

5. Відкрий браузер на `http://localhost:5000`

## Структура проєкту

```
model-share/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── routes.py
│   ├── templates/
│   └── static/
├── run.py
├── config.py
├── requirements.txt
└── README.md
```

## Автор

Yevhenii Khokhlov
