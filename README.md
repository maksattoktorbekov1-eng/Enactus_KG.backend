Документация Backend API — Enactus Кыргызстан
Проект: Enactus KG
Версия: 1.1
Автор: Максат Токторбеков
Дата: 14 марта 2026

Стек:

Python 3.12
Django 5.2
Django REST Framework 3.16
PostgreSQL 16
JWT авторизация


Авторизация
Все /api/admin/ эндпоинты требуют JWT токен в заголовке:
Authorization: Bearer <access_token>
Получить токен:
POST /api/auth/token/
{
    "username": "admin",
    "password": "password"
}
Обновить токен:
POST /api/auth/token/refresh/
{
    "refresh": "<refresh_token>"
}

Мультиязычность
Все публичные эндпоинты принимают параметр ?lang=. Доступные значения: ru, kg, en. Если перевод на запрошенный язык отсутствует — возвращается русская версия.
GET /api/programs/?lang=kg
GET /api/news/?lang=en

Программы
Публичные
Список программ
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
Ответ:
json{
    "id": 1,
    "slug": "enactus",
    "program_type": "enactus",
    "image": "/media/programs/photo.jpg",
    "title": "Программа Enactus",
    "description": "Краткое описание",
    "content": "Полный текст",
    "instruction": "Инструкция по созданию команды",
    "career_guidance": "",
    "support_initiatives": "",
    "meta_title": "Enactus KG",
    "meta_description": "SEO описание",
    "gallery": [],
    "teams": [],
    "advisors": [],
    "timeline": [],
    "summer_camps": []
}
```

### Административные

**Список / создание**
```
GET  /api/admin/programs/
POST /api/admin/programs/
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
            "career_guidance": "",
            "support_initiatives": "",
            "meta_title": "Enactus KG",
            "meta_description": "SEO описание"
        },
        {
            "lang": "kg",
            "title": "Enactus программасы",
            "description": "Кыскача сүрөттөмө",
            "content": "Толук текст",
            "instruction": "Нускама",
            "career_guidance": "",
            "support_initiatives": "",
            "meta_title": "Enactus KG",
            "meta_description": "SEO сүрөттөмө"
        }
    ]
}
```

> Поля `career_guidance` и `support_initiatives` заполняются только для типа `youth_initiatives`.

**Получить / обновить / удалить**
```
GET    /api/admin/programs/<id>/
PUT    /api/admin/programs/<id>/
PATCH  /api/admin/programs/<id>/
DELETE /api/admin/programs/<id>/
```

> Удаление — мягкое. Программа не удаляется из базы, а скрывается (`is_active = false`).

**Галерея программы**
```
GET    /api/admin/programs/<id>/gallery/
POST   /api/admin/programs/<id>/gallery/
GET    /api/admin/programs/<id>/gallery/<id>/
PUT    /api/admin/programs/<id>/gallery/<id>/
DELETE /api/admin/programs/<id>/gallery/<id>/
```

**Команды программы**
```
GET    /api/admin/programs/<id>/teams/
POST   /api/admin/programs/<id>/teams/
GET    /api/admin/programs/<id>/teams/<id>/
PUT    /api/admin/programs/<id>/teams/<id>/
DELETE /api/admin/programs/<id>/teams/<id>/
```

**Советники программы**
```
GET    /api/admin/programs/<id>/advisors/
POST   /api/admin/programs/<id>/advisors/
GET    /api/admin/programs/<id>/advisors/<id>/
PUT    /api/admin/programs/<id>/advisors/<id>/
DELETE /api/admin/programs/<id>/advisors/<id>/
```

**Таймлайн программы**
```
GET    /api/admin/programs/<id>/timeline/
POST   /api/admin/programs/<id>/timeline/
GET    /api/admin/programs/<id>/timeline/<id>/
PUT    /api/admin/programs/<id>/timeline/<id>/
DELETE /api/admin/programs/<id>/timeline/<id>/
Тело запроса:
json{
    "year": 2021,
    "sort_order": 0,
    "translations": [
        {
            "lang": "ru",
            "title": "Основание",
            "description": "Программа была основана"
        }
    ]
}
```

**Летний лагерь**
```
GET    /api/admin/programs/<id>/summer-camps/
POST   /api/admin/programs/<id>/summer-camps/
GET    /api/admin/programs/<id>/summer-camps/<id>/
PUT    /api/admin/programs/<id>/summer-camps/<id>/
DELETE /api/admin/programs/<id>/summer-camps/<id>/
Тело запроса:
json{
    "start_date": "2026-07-01",
    "end_date": "2026-07-14",
    "location": "Иссык-Куль",
    "is_active": true,
    "sort_order": 0,
    "translations": [
        {
            "lang": "ru",
            "title": "Летний лагерь 2026",
            "description": "Описание лагеря"
        }
    ]
}
```

### Типы программ

| Значение | Название |
|----------|----------|
| `enactus` | Enactus |
| `hult_prize` | Hult Prize |
| `ybi` | YBI |
| `youth_initiatives` | Молодёжные инициативы |

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
Тело запроса:
json{
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
Тело запроса:
json{
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

##Медиафайлы

Все загружаемые файлы доступны по адресу:
```
http://localhost:8000/media/<путь_к_файлу>
```

| Раздел | Папка |
|--------|-------|
| Программы | `media/programs/` |
| Галерея | `media/programs/gallery/` |
| Команды | `media/programs/teams/` |
| Советники | `media/programs/advisors/` |
| Летний лагерь | `media/programs/summer_camp/` |
| Партнёры | `media/partners/` |
| Новости | `media/news/` |

Максимальный размер файла — 10 МБ.

---

## Документация API

После запуска сервера документация доступна по адресам:
```
http://localhost:8000/swagger/
http://localhost:8000/redoc/
