from django.contrib import admin
from .models import *


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Article, ArticleAdmin)
admin.site.register(MarkedArticle)
admin.site.register(CountArticleUser)
admin.site.register(ReadTheArticle)

