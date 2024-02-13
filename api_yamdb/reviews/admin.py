from django.contrib import admin

from .models import Comment, Review


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'pub_date', 'review')
    search_fields = ('text',)
    list_filter = ('author', 'review', 'pub_date',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'score', 'pub_date', 'title')
    search_fields = ('text',)
    list_filter = ('author', 'title', 'pub_date',)


admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
