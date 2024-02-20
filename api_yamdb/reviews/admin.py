from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'pub_date', 'review')
    search_fields = ('text',)
    list_filter = ('author', 'review', 'pub_date',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'score', 'pub_date', 'title')
    search_fields = ('text',)
    list_filter = ('author', 'title', 'pub_date',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name', 'slug')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name', 'slug')


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('name', 'year', 'category')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('genre')
        return queryset

    def genre_names(self, obj):
        return ', '.join([genre.name for genre in obj.genre.all()])

    list_display = ('name', 'year', 'description', 'category', 'genre_names')
