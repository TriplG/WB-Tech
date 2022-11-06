from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Article, MarkedArticle, CountArticleUser, ReadTheArticle
from django.contrib import auth
import json


class TestViews(TestCase):

    def setUp(self):
        self.testuser1 = User.objects.create_user(username='testuser1', password='12345')
        self.article1 = Article.objects.create(
            slug='Statiya-1',
            title='Статья 1',
            content='Статья 1 пользователя testuser1',
            author=self.testuser1
        )
        CountArticleUser.objects.create(author=self.testuser1, count=1)

    def test_views_index_GET_notAuth(self):
        client = Client()
        response = client.get(reverse('index'))
        self.assertEquals(response.url, '/all_articles/')
        self.assertEquals(response.status_code, 302)

    def test_views_index_GET_Auth(self):
        client = Client()
        client.login(username='testuser1', password='12345')
        response = client.get(reverse('index'))
        self.assertEquals(response.url, '/rec_article/')
        self.assertEquals(response.status_code, 302)

    def test_views_AllArticles_GET(self):
        client = Client()
        response = client.get(reverse('all_articles'))
        self.assertTemplateUsed(response, 'Blog/index.html')
        self.assertEquals(response.status_code, 200)

    def test_views_RecArticle_GET(self):
        client = Client()
        client.login(username='testuser1', password='12345')
        response = client.get(reverse('rec_article'))
        self.assertTemplateUsed(response, 'Blog/index.html')
        self.assertEquals(response.status_code, 200)

    def test_views_ShowArticleAuthor_GET(self):
        client = Client()
        response = client.get(reverse('author_detail', args=[self.testuser1.pk]))
        self.assertTemplateUsed(response, 'Blog/author_detail.html')
        self.assertEquals(response.status_code, 200)

    def test_views_AddArticle_POST(self):
        client = Client()
        client.login(username='testuser1', password='12345')
        response = client.post(reverse('add_article'), {
            # 'slug': 'Statiya-2',
            'title': 'Статья 2',
            'content': 'Статья 2 пользователя testuser1',
            # 'author': client
        })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(CountArticleUser.objects.get(author=self.testuser1).count, 2)
        self.assertEquals(Article.objects.all().count(), 2)
        self.assertEquals(Article.objects.last().title, 'Статья 2')



    def test_views_RegisterUser_POST(self):
        client = Client()
        response = client.post(reverse('register'), {
            'username': 'create_testuser',
            'password1': 'karamaba10',
            'password2': 'karamaba10'
        })
        self.assertEquals(CountArticleUser.objects.all().count(), 2)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(User.objects.all().count(), 2)
        self.assertEquals(auth.get_user(client).is_authenticated, True)



