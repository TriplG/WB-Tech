from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import *


class TestUrls(SimpleTestCase):

    def test_url_name_index(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_url_name_all_articles(self):
        url = reverse('all_articles')
        self.assertEquals(resolve(url).func.view_class, AllArticles)

    def test_url_name_authors(self):
        url = reverse('authors')
        self.assertEquals(resolve(url).func.view_class, Author)

    def test_url_name_sort_list_user(self):
        url = reverse('sort_list_user')
        self.assertEquals(resolve(url).func.view_class, SortListUser)

    def test_url_name_author_detail(self):
        url = reverse('author_detail', args=['1234'])
        self.assertEquals(resolve(url).func.view_class, ShowArticleAuthor)

    def test_url_name_register(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func.view_class, RegisterUser)

    def test_url_name_login(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, LoginUser)

    def test_url_name_logout(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout_user)

