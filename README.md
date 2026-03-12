Документация backend API — Enactus Кыргызстан
Проект: Enactus KG
Версия: 1.0
Автор: Максат Токторбеков
Дата: 12 марта 2026

Стек

Python 3.12
Django 5.0
Django REST Framework 3.15
PostgreSQL 16
JWT авторизация

ь## Авторизация

Все `/api/admin/` эндпоинты требуют JWT токен в заголовке:
```
Authorization: Bearer <access_token>
```

Получить токен:
```
POST /api/auth/token/
{
    "username": "admin",
    "password": "password"
}
```

Обновить токен:
```
POST /api/auth/token/refresh/
{
    "refresh": "<refresh_token>"
}
```

---

## Мультиязычность

Все публичные эндпоинты принимают параметр `?lang=`. Доступные значения: `ru`, `kg`, `en`. Если перевод на запрошенный язык отсутствует — возвращается русская версия.
```
GET /api/programs/?lang=kg
GET /api/news/?lang=en
```

---

## Программы

### Публичные

**Список программ**
```
GET /api/programs/?lang=ru


Ответ:
json[
    {
        "id": 1,
        "slug": "enactus",
        "program_type": "enactus",
        "image": "/media/programs/photo.jpg",
        "title": "Программа Enactus",
        "description": "Краткое описание"
    }
]
```

**Одна программа**
```
GET /api/programs/<slug>/?lang=ru


Тело запроса для создания:
json{
    "program_type": "enactus",
    "is_active": true,
    "sort_order": 0,
    "translations": [
        {
            "lang": "ru",
            "title": "Программа Enactus",
            "description": "Описание",
            "content": "Полный текст",
            "instruction": "Инструкция",
            "meta_title": "Enactus KG",
            "meta_description": "SEO описание"
        },
        {
            "lang": "kg",
            "title": "Enactus программасы",
            "description": "Кыскача сүрөттөмө",
            "content": "Толук текст",
            "instruction": "Нускама",
            "meta_title": "Enactus KG",
            "meta_description": "SEO сүрөттөмө"
        }
    ]
}
```

**Получить / обновить / удалить**
```
GET    /api/admin/programs/<id>/
PUT    /api/admin/programs/<id>/
PATCH  /api/admin/programs/<id>/
DELETE /api/admin/programs/<id>/
```

> Удаление — мягкое. Программа не удаляется из базы, а скрывается (`is_active = false`).

### Галерея программы
```
GET    /api/admin/programs/<id>/gallery/
POST   /api/admin/programs/<id>/gallery/
GET    /api/admin/programs/<id>/gallery/<id>/
PUT    /api/admin/programs/<id>/gallery/<id>/
DELETE /api/admin/programs/<id>/gallery/<id>/
```

### Команды программы
```
GET    /api/admin/programs/<id>/teams/
POST   /api/admin/programs/<id>/teams/
GET    /api/admin/programs/<id>/teams/<id>/
PUT    /api/admin/programs/<id>/teams/<id>/
DELETE /api/admin/programs/<id>/teams/<id>/
```

### Советники программы
```
GET    /api/admin/programs/<id>/advisors/
POST   /api/admin/programs/<id>/advisors/
GET    /api/admin/programs/<id>/advisors/<id>/
PUT    /api/admin/programs/<id>/advisors/<id>/
DELETE /api/admin/programs/<id>/advisors/<id>/
```

### Таймлайн программы
```
GET    /api/admin/programs/<id>/timeline/
POST   /api/admin/programs/<id>/timeline/
GET    /api/admin/programs/<id>/timeline/<id>/
PUT    /api/admin/programs/<id>/timeline/<id>/
DELETE /api/admin/programs/<id>/timeline/<id>/
```

---

## Партнёры

### Публичные
```
GET /api/partners/?lang=ru

Ответ:
json[
    {
        "id": 1,
        "name": "ЮСАИД",
        "logo": "/media/partners/usaid.png",
        "website_url": "https://usaid.gov",
        "sort_order": 0
    }
]
```

### Административные
```
GET    /api/admin/partners/
POST   /api/admin/partners/
GET    /api/admin/partners/<id>/
PUT    /api/admin/partners/<id>/
PATCH  /api/admin/partners/<id>/
DELETE /api/admin/partners/<id>/

{
    "logo": "<file>",
    "website_url": "https://example.com",
    "is_active": true,
    "sort_order": 0,
    "translations": [
        {"lang": "ru", "name": "ЮСАИД"},
        {"lang": "kg", "name": "ЮСАИД"},
        {"lang": "en", "name": "USAID"}
    ]
}
```

**Изменить порядок партнёров**
```
PATCH /api/admin/partners/reorder/
{
    "ids": [3, 1, 2]
}
```

Партнёры будут отображаться в том порядке, в котором переданы ID.

---

## Новости

### Публичные

**Список новостей**
```
GET /api/news/?lang=ru
GET /api/news/?lang=ru&category=events
GET /api/news/?lang=ru&limit=3
```

**Одна новость**
```
GET /api/news/<slug>/?lang=ru
```

**Категории**
```
GET /api/news/categories/?lang=ru
```

### Административные
```
GET    /api/admin/news/
POST   /api/admin/news/
GET    /api/admin/news/<id>/
PUT    /api/admin/news/<id>/
PATCH  /api/admin/news/<id>/
DELETE /api/admin/news/<id>/

{
    "category": 1,
    "is_published": true,
    "published_at": "2026-03-12T09:00:00Z",
    "translations": [
        {
            "lang": "ru",
            "title": "Заголовок новости",
            "excerpt": "Краткое описание",
            "content": "Полный текст новости",
            "meta_title": "SEO заголовок",
            "meta_description": "SEO описание"
        }
    ]
}
```

> Удаление — мягкое. Новость скрывается (`is_published = false`).

**Категории новостей**
```
GET    /api/admin/news/categories/
POST   /api/admin/news/categories/
GET    /api/admin/news/categories/<id>/
PUT    /api/admin/news/categories/<id>/
DELETE /api/admin/news/categories/<id>/
```

---

## Медиафайлы

Все загружаемые файлы доступны по адресу:
```
http://localhost:8000/media/<путь_к_файлу>
```

Максимальный размер файла — 10 МБ.

---

## Документация API

После запуска сервера документация доступна по адресам:
```
http://localhost:8000/swagger/
http://localhost:8000/redoc/
