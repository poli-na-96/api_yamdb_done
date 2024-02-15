from django.contrib import admin

from .models import Comment, Review, Category, Genre, Title


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'pub_date', 'review')
    search_fields = ('text',)
    list_filter = ('author', 'review', 'pub_date',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'score', 'pub_date', 'title')
    search_fields = ('text',)
    list_filter = ('author', 'title', 'pub_date',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name', 'slug')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name', 'slug')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'genre', 'category')
    search_fields = ('name',)
    list_filter = ('name', 'year')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
