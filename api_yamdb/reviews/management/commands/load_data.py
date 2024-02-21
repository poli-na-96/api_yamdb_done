import csv
import os

from django.core.management.base import BaseCommand

from reviews.constants import (CATEGORY_CSV, COMMENTS_CSV, GENRE_CSV,
                               GENRE_TITLE_CSV, REVIEW_CSV, TITLES_CSV,
                               USERS_CSV)
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from user.models import User


class Command(BaseCommand):
    """Добавляет данные из CSV файлов в модели.

    Позволяет загрузить данные из CSV файлов в базу данных.

    Для того, чтобы запустить комманду, введите: python manage.py load_data

    Public методы:
    - handle(*args, **kwargs): Обработка данных из CSV-файлов и загрузка в БД
    """

    def handle(self, *args, **kwargs):
        """Обработка данных и их загрузка в базу данных."""
        dir_path = os.path.abspath(
            os.path.join('.', 'static', 'data')
        )

        file_model = {
            CATEGORY_CSV: Category,
            GENRE_CSV: Genre,
            USERS_CSV: User,
            TITLES_CSV: Title,
            GENRE_TITLE_CSV: GenreTitle,
            REVIEW_CSV: Review,
            COMMENTS_CSV: Comment,
        }

        for file, model in file_model.items():
            path = os.path.join(dir_path, file)

            obj_list = []
            with open(path, encoding='utf-8') as csv_file:
                for obj_dict in csv.DictReader(csv_file):
                    if file == TITLES_CSV:
                        obj_dict['category'] = Category(
                            int(obj_dict['category'])
                        )
                    elif file == REVIEW_CSV:
                        obj_dict['author'] = User(int(obj_dict['author_id']))
                    elif file == COMMENTS_CSV:
                        obj_dict['author'] = User(int(obj_dict['author']))
                    obj_list.append(model(**obj_dict))
                model.objects.bulk_create(obj_list)
        self.stdout.write(self.style.SUCCESS('Данные успешно загружены'))

    """Добавляет данные из CSV файлов в модели.

    Позволяет загрузить данные из CSV файлов в базу данных.

    Для того, чтобы запустить комманду, введите: python manage.py load_data

    Public методы:
    - handle(*args, **kwargs): Обработка данных из CSV-файлов и загрузка в БД
    """

    def handle(self, *args, **kwargs):
        """Обработка данных и их загрузка в базу данных."""
        dir_path = os.path.abspath(
            os.path.join('.', 'static', 'data')
        )

        file_model = {
            CATEGORY_CSV: Category,
            GENRE_CSV: Genre,
            USERS_CSV: User,
            TITLES_CSV: Title,
            GENRE_TITLE_CSV: GenreTitle,
            REVIEW_CSV: Review,
            COMMENTS_CSV: Comment,
        }

        for file, model in file_model.items():
            path = os.path.join(dir_path, file)

            obj_list = []
            with open(path, encoding='utf-8') as csv_file:
                for obj_dict in csv.DictReader(csv_file):
                    if file == TITLES_CSV:
                        obj_dict['category'] = Category(
                            int(obj_dict['category'])
                        )
                    elif file == REVIEW_CSV:
                        obj_dict['author'] = User(int(obj_dict['author_id']))
                    elif file == COMMENTS_CSV:
                        obj_dict['author'] = User(int(obj_dict['author']))
                    obj_list.append(model(**obj_dict))
                model.objects.bulk_create(obj_list)
