Описание. Проект api_yamdb это проект, где представлены отзывы на различные произведения (книги, фильмы, музыка). Зарегистрированный пользователь может оставлять свой отзыв на каждое произведение, ставить ему оценку, а также комментировать чужие отзывы на произведение. В данном проекте представлен backend api_yamdb.

Установка. Как запустить проект: 

Клонировать репозиторий и перейти в него в командной строке:
git clone git@github.com:maximpontnyagin/api_yamdb.git cd api_yamdb 

Cоздать и активировать виртуальное окружение:
python -m venv venv source venv/Scripts/activate 

Установить зависимости из файла requirements.txt:
pip install -r requirements.txt 

Выполнить миграции:
python manage.py migrate 

Запустить проект:
python manage.py runserver

Примеры запросов:

Опубликовать отзыв:
POST запрос на http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
{
"text": "string"
}

Ответ:
{
"id": 0,
"text": "string",
"author": "string",
"pub_date": "2019-08-24T14:15:22Z"
}

Получить список пользователей:
GET запрос на http://127.0.0.1:8000/api/v1/users/

Ответ:
{
"count": 0,
"next": "string",
"previous": "string",
"results": [
{}
]
}

Частично обновить комментарий к отзыву:
PATCH запрос на http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
{
"text": "string"
}

Ответ:
Copy
{
"id": 0,
"text": "string",
"author": "string",
"pub_date": "2019-08-24T14:15:22Z"
}
