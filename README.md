# Веб-сервер на Django со Stripe API

Сервер, который общается со Stripe и создает платежные формы для товаров.

Демо:
**http://borisrouge.ru**

Тэг докер-образа: **borisrouge/django-stripe-webpage**

>Реализованы каталог товаров, страница отдельного товара, добавление товаров в общий заказ, оплата заказа через Stripe Session, скидки через промокоды.
Управление скидками, товаром и заказами в админ-панели.

### Локальный запуск: 
- Создать виртуальное окружение, например:  
`virtualenv venv`  
- Создать в виртуальном окружении переменную **stripe_api_key** с соответствующим ключом.  
- Клонировать репозиторий.  
- Установить зависимости:  
`pip install -r requirements.txt`  
- Запустить сервер:  
`python manage.py runserver`

