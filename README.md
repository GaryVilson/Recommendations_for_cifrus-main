# Установка приложения рекомендаций для сайта cifrus.ru (Django)

1. Открываем терминал в папке проекта и создаем виртуальное окружение
```
python -m venv venv
```
2. Активируем виртуальное окружение
```
. venv/Scripts/activate
```
3. Устанавливаем необходимые библиотеки из `requirements.txt`
```
pip install -r requirements.txt
```
4. Запускаем докер контейнер PostgreSQL:
```
docker-compose up
```
5. Подключаемся к серверу и создаем базу `cifrus_db`.
6. В файле `settings.py` устанавливаем конфигурацию базы данных:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cifrus_db',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
7. Переходим в директорию `cifrus_app`
```
cd cifrus_app
```
8. Запускаем миграции
```
python manage.py migrate
```
9. Запускаем скрипт `cifrus_parser` для сбора и добавления данных в базу
```
python manage.py runscript cifrus_parser -v2
```
10. Запускаем локальный сервер
```
python manage.py runserver
```
