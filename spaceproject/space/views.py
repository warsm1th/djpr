from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AddPostForm
from .models import *
from .utils import *
from django.core.paginator import Paginator


class SpaceHome(DataMixin, ListView):
    model = Objects
    template_name = 'space/index.html'
    context_object_name = 'posts'


    # Функция для формирования динамического и статического контекста
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # Сохраняем сформированный контекст
        mixin_context = self.get_user_context(title='Главная страница')
        return context | mixin_context

    def get_queryset(self):  # Настройка запроса из БД
        return Objects.objects.filter(is_published=True)  # Фильтруем записи из БД


def about(request):
    contact_list = Objects.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, 'space/about.html', {'page_obj': page_object, 'menu': menu, 'title': 'О сайте'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'space/addpage.html'
    success_url = reverse_lazy('home')    # Перенаправление при успешном добавлении статьи
    login_url = reverse_lazy('home')      # Перенаправление при отсутствии авторизации
    raise_exception = True                # ошибка 403 "Доступ запрещен" при отсутствии авторизации

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Добавление статьи')
        return context | mixin_context


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse("Авторизация")


class ShowPost(DataMixin, DetailView):
    model = Objects
    template_name = 'space/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title=context["post"])
        return context | mixin_context


class SpaceCategory(DataMixin, ListView):
    model = Objects
    template_name = 'space/index.html'
    context_object_name = 'posts'
    allow_empty = False  # При отсутствии записей формируется ошибка 404

    def get_queryset(self):
        return Objects.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        title = 'Категория - ' + str(context['posts'][0].cat)
        mixin_context = self.get_user_context(title=title, cat_selected=context['posts'][0].cat_id)
        return context | mixin_context


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
