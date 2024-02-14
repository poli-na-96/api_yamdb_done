import csv

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import (Category, Comment, Genre,
                            Review, Title, GenreTitle)
from users.models import User


class Command(BaseCommand):
    help = 'Загрузка данных из CSV в базу данных'

    def handle(self, *args, **options):
        models = {
            'User': (User, 'users.csv'),
            'Category': (Category, 'category.csv'),
            'Title': (Title, 'titles.csv'),
            'Comment': (Comment, 'comments.csv'),
            'Genre': (Genre, 'genre.csv'),
            'Review': (Review, 'review.csv'),
            'GenreTitle': (GenreTitle, 'genre_title.csv')
        }

        for model_name, (model, csv_file) in models.items():
            with open(f'{settings.BASE_DIR}/static/data/{csv_file}', 'r',
                      encoding='utf-8') as file:
                reader = csv.DictReader(file)
                instances = [model(**row) for row in reader]
                model.objects.bulk_create(instances)

        self.stdout.write(self.style.SUCCESS('Данные успешно загружены'))
