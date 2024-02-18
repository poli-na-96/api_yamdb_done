import csv
import os

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from user.models import User


class Command(BaseCommand):
    """
    Добавляет данные из csv файлов в модели.
    Для запуска скрипта: python manage.py load_data
    """

    def handle(self, *args, **kwargs):
        dir_path = os.path.abspath(
            os.path.join('.', 'static', 'data')
        )

        file_model = {
            'category.csv': Category,
            'genre.csv': Genre,
            'users.csv': User,
            'titles.csv': Title,
            'genre_title.csv': GenreTitle,
            'review.csv': Review,
            'comments.csv': Comment,
        }

        for file, model in file_model.items():
            path = os.path.join(dir_path, file)

            obj_list = []
            with open(path, encoding='utf-8') as csv_file:
                for obj_dict in csv.DictReader(csv_file):
                    if file == 'titles.csv':
                        obj_dict['category'] = Category(
                            int(obj_dict['category'])
                        )
                    elif file == 'review.csv':
                        obj_dict['author'] = User(int(obj_dict['author_id']))
                    elif file == 'comments.csv':
                        obj_dict['author'] = User(int(obj_dict['author']))
                    obj_list.append(model(**obj_dict))
                model.objects.bulk_create(obj_list)
        self.stdout.write(self.style.SUCCESS('Данные успешно загружены'))
