from django.contrib import admin
from .models import ArticleColumn
from .models import ArticlePost


class ArticleColumnAdmin(admin.ModelAdmin):
    list_display = ('column', 'created', 'user')
    list_filter = ("column",)


admin.site.register(ArticleColumn, ArticleColumnAdmin)


class ArticlePostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'author')
    list_filter = ('title', )
    search_fields = ('title', 'body')


admin.site.register(ArticlePost, ArticlePostAdmin)