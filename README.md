# HR_tech
Веб-сайт для внутренних опросов компании
---
### Для развертывания пректа в Docker.

1. Скопировать репозиторий.
2. Собрать контейнеры командой: docker-compose build.
3. Запустить контейнеры: docker-compose up.
4. Провести миграции БД: docker-compose run web python /code/manage.py migrate --noinput.
5. Загрузить фикстуры в БД: docker-compose run web python /code/manage.py loaddata data.xml
6. Запустить контейнеры: docker-compose up.
***
Сайт работает по адресу localhost:8000
В базе данных предустановлены пользователи: 
    
    Суперпользователь: логин admin, пароль 1  
    Пользователь с привилегиями менеджера (создание и редактирование опросов и тестов): логин user1, пароль 12345678aq
    Пользователь с обычными привилегями: логин user2, пароль 12345678aq. 
***

Сайт на heroku: [Нажмите чтобы перейти](https://intense-waters-15921.herokuapp.com/)