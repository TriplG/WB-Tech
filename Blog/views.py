from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.base import View
from django.core.paginator import Paginator

from django.contrib import messages
from transliterate import slugify

from .models import *
from .forms import *


def index(request):
    if request.user.is_authenticated:
        return redirect(f'/rec_article/')
    return redirect(f'/all_articles/')


class AllArticles(ListView):
    # Представление главной страницы со всеми статьями
    paginate_by = 10
    model = Article
    template_name = 'Blog/index.html'
    context_object_name = 'articles'
    queryset = Article.objects.all().order_by('-pk')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['sort_form'] = SortHomeForm()
        context['head'] = 'Все статьи'

        return context


class RecArticle(View):
    # Представление главной страницы с рекомендациями
    def get(self, request):
        # Поиск рекомендованных статей
        subscribe_article = MarkedArticle.objects.filter(subscribe_to_post=True, showing_to_user=request.user)
        recommended_articles = Article.objects.none()

        if subscribe_article.exists():
            for i in subscribe_article:
                recommended_articles = recommended_articles.union(
                    Article.objects.filter(author=i.article.author, time_create__gte=i.time_subscribe_to_post)
                )
            recommended_articles = recommended_articles.order_by('-time_create')
            head = 'Ваши рекомендации'
            paginator = Paginator(recommended_articles, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

        else:
            head = 'Вы не подписались не на одну статью'
            page_obj = None

        context = {
            'page_obj': page_obj,
            'title': 'Рекомендации',
            'head': head
        }
        return render(request, 'Blog/index.html', context=context)


class ReadArticle(View):
    # Представление прочитанных статей на главной странице

    def get(self, request):
        # Поиск прочитанных статей
        articles_read = ReadTheArticle.objects.filter(showing_to_user=self.request.user)
        articles_read_user = Article.objects.none()
        if articles_read.exists():
            for i in articles_read:
                articles_read_user = articles_read_user.union(Article.objects.filter(pk=i.article.pk))

        if articles_read_user.exists():
            head = 'Прочитанные статьи'
            paginator = Paginator(articles_read_user, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        else:
            head = 'Вы не прочитали не одной статьи'
            page_obj = None


        context = {
            'page_obj': page_obj,
            'title': 'Прочитанные статьи',
            'head': head
        }
        return render(request, 'Blog/index.html', context=context)


class Author(ListView):
    # Представление страницы пользователей с количествами постов
    model = CountArticleUser
    template_name = 'Blog/authors.html'
    context_object_name = 'count_article_user'
    queryset = CountArticleUser.objects.all().order_by('author')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_form'] = SortAutorForm()
        context['title'] = 'Пользователи'
        return context


class SortListUser(View):
    # Представление отсортированной страницы пользователей(по количеству постов, по авторам)
    def post(self, request):
        sort_form = SortAutorForm(request.POST)
        count_article_user = CountArticleUser.objects.all()
        if sort_form.is_valid():
            needed_sort = sort_form.cleaned_data.get("sort_autor_form")
            if needed_sort == "количество":
                count_article_user = count_article_user.order_by("-count")
            elif needed_sort == "автор":
                count_article_user = count_article_user.order_by("author")
        context = {
            'sort_form': sort_form,
            'count_article_user': count_article_user,
            'title': 'Пользователи'
        }
        return render(request, 'Blog/authors.html', context=context)


class ShowArticleAuthor(DetailView):
    # Представление страницы пользователя с написанными им статьями
    model = User
    template_name = 'blog/author_detail.html'
    context_object_name = 'user'
    pk_url_kwarg = 'user_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Посты пользователя {self.request.user}'
        context['article'] = Article.objects.filter(author=self.request.user).order_by('-time_create')

        return context


class ShowArticle(DetailView):
    # Представление для конкретной статьи
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'
    slug_url_kwarg = 'article_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Пост {context["article"]}'
        print(context["article"].slug)
        a = Article.objects.get(slug=context["article"].slug)
        try:
            context['marked_article'] = MarkedArticle.objects.get(showing_to_user=self.request.user, article=a)
        except MarkedArticle.DoesNotExist:
            context['marked_article'] = None

        try:
            context['read_the_article'] = ReadTheArticle.objects.get(showing_to_user=self.request.user, article=a)
        except ReadTheArticle.DoesNotExist:
            context['read_the_article'] = None

        return context


def sub_from_post(request, article_slug):
    subscribe_to_post = MarkedArticle.objects.create(
        article=Article.objects.get(slug=article_slug), showing_to_user=request.user, subscribe_to_post=True
    )

    return redirect(f'/article/{article_slug}/')


def unsub_from_post(request, article_slug):
    a = Article.objects.get(slug=article_slug)
    unsub = MarkedArticle.objects.get(showing_to_user=request.user, article=a)
    unsub.delete()

    return redirect(f'/article/{article_slug}/')


def mark_as_read(request, article_slug):
    marked_article = ReadTheArticle.objects.create(
        article=Article.objects.get(slug=article_slug), showing_to_user=request.user
    )

    return redirect(f'/article/{article_slug}/')


def remove_the_mark(request, article_slug):
    a = Article.objects.get(slug=article_slug)
    remove_mark = ReadTheArticle.objects.get(showing_to_user=request.user, article=a)
    remove_mark.delete()

    return redirect(f'/article/{article_slug}/')


class AddArticlePage(View):
    def get(self, request):
        form = AddArticleForm(request.POST)
        context = {
            'title': 'Добавление статьи',
            'form': form
        }
        return render(request, 'Blog/add_article.html', context)


class AddArticle(View):
    def post(self, request):
        form = AddArticleForm(request.POST)
        if form.is_valid():
            add_article = form.save(commit=False)
            add_article.title = form.cleaned_data['title']
            add_article.content = form.cleaned_data['content']
            add_article.author = request.user
            add_article.slug = slugify(form.cleaned_data['title'])
            add_article.save()

            cau = CountArticleUser.objects.get(author=request.user)
            cau.count += 1
            cau.save()

            messages.add_message(request, messages.INFO, "Статья успешно добавлена!")
            return HttpResponseRedirect('/')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'Blog/register.html'
    success_url = reverse_lazy('authors')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Регистрация"
        messages.add_message(self.request, messages.INFO, "Статья успешно добавлена!")

        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        CountArticleUser.objects.create(
            author=self.request.user, count=0
        )
        return redirect('index')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'Blog/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('index')


def logout_user(request):
    logout(request)
    print('hello')
    return redirect('login')


