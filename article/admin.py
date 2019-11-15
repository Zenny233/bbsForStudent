from django.contrib import admin
from .models import ArticleColumn
from .models import ArticlePost
from .models import Comment

class ArticleColumnAdmin(admin.ModelAdmin):
    list_display = ('column', 'created', 'user')
    list_filter = ("column",)


admin.site.register(ArticleColumn, ArticleColumnAdmin)


class ArticlePostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'author','is_check_article')
    list_filter = ('is_check_article', )
    search_fields = ('title', 'body')


admin.site.register(ArticlePost, ArticlePostAdmin)

class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ('body','commentator','created', 'article','is_check_comment')
    list_filter = ('is_check_comment', )
    search_fields = ('commentator', 'body',)


admin.site.register(Comment, ArticleCommentAdmin)