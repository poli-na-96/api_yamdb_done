# Групповой проект api_yamdb

**Описание.**
Проект api_yamdb это проект, где представлены отзывы и составлен рейтинг на различные произведения (книги, фильмы, музыка). Зарегистрированный пользователь может оставлять свой отзыв на каждое произведение, ставить ему оценку, а также комментировать чужие отзывы на произведение. В данном проекте представлен backend api_yamdb.

**Стек используемых технологий.**
* Django 
* sqlite3 
* python 3.9.10

**Как развернуть проект.**
1. Клонировать репозиторий и перейти в него в командной строке:
_git clone git@github.com:maximpontnyagin/api_yamdb.git cd api_yamdb_

2. Cоздать и активировать виртуальное окружение:
_python -m venv venv source venv/Scripts/activate_ 

3. Установить зависимости из файла requirements.txt:
_pip install -r requirements.txt_ 

4. Выполнить миграции:
_python manage.py migrate_

5. Запустить проект:
_python manage.py runserver_

**Примеры запросов и ответов.**
- **_Опубликовать отзыв:**_
_POST запрос на http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
{
"text": "string"
}_
**_Ответ:_**
_{
"id": 0,
"text": "string",
"author": "string",
"pub_date": "2019-08-24T14:15:22Z"
}_

- **_Получить список пользователей:_**
_GET запрос на http://127.0.0.1:8000/api/v1/users/_
**_Ответ:_**
_{
"count": 0,
"next": "string",
"previous": "string",
"results": [
{}
]
}_

- **_Частично обновить комментарий к отзыву:_**
_PATCH запрос на http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
{
"text": "string"
}_
**_Ответ:_**
_Copy
{
"id": 0,
"text": "string",
"author": "string",
"pub_date": "2019-08-24T14:15:22Z"
}_

**Авторы проекта.**
Максим Понтрягин - _https://github.com/maximpontryagin_
Вероника Бархатова - _https://github.com/veronikabarhatova_
Полина Путилина - _https://github.com/poli-na-96_
