from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('all_articles/', AllArticles.as_view(), name='all_articles'),
    path('authors/', Author.as_view(), name='authors'),
    path('sort_list_user/', SortListUser.as_view(), name='sort_list_user'),
    path('author/<int:user_id>/', ShowArticleAuthor.as_view(), name='author_detail'),
    path('article/<slug:article_slug>/', ShowArticle.as_view(), name='article_detail'),
    path('sub_from_post/<slug:article_slug>/', sub_from_post, name='sub_from_post'),
    path('unsub_from_post/<slug:article_slug>/', unsub_from_post, name='unsub_from_post'),
    path('rec_article/', RecArticle.as_view(), name='rec_article'),
    path('mark_as_read/<slug:article_slug>/', mark_as_read, name='mark_as_read'),
    path('remove_the_mark/<slug:article_slug>/', remove_the_mark, name='remove_the_mark'),
    path('read_article/', ReadArticle.as_view(), name='read_article'),
    path('add_article/', AddArticle.as_view(), name='add_article'),
    path('add_article_page/', AddArticlePage.as_view(), name='add_article_page'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),


]

