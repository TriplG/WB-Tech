from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    slug = models.SlugField(verbose_name='Название статьи на английском', max_length=50)
    title = models.CharField(verbose_name='Название статьи', max_length=50)
    content = models.TextField(verbose_name='Содержание')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title


class MarkedArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Пост')
    showing_to_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Показывать для пользователя')
    subscribe_to_post = models.BooleanField(default=False, verbose_name='Подписка на пост')
    time_subscribe_to_post = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')
    # read_article = models.BooleanField(default=False, verbose_name='Прочитанная статья')

    class Meta:
        verbose_name = 'Статья для авторизованного пользователя'
        verbose_name_plural = 'Статьи для авторизованных пользователей'

    def __str__(self):
        return f"Пост {self.article} для пользователя {self.showing_to_user}"


class CountArticleUser(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(verbose_name='Количество статей автора')

    def __str__(self):
        return f"Количество статей пользователя - {self.author}({self.count})"

    class Meta:
        verbose_name = 'Количество статей пользователя'
        verbose_name_plural = 'Количество статей пользоватей'


class ReadTheArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Пост')
    showing_to_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Показывать для пользователя')

    def __str__(self):
        return f"Прочитанные статьи"

    class Meta:
        verbose_name = 'Количество прочитанных статей пользователя'
        verbose_name_plural = 'Количество прочитанных статей пользоватей'
