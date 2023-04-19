from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .models import *
from .forms import *


class SpaceHome(ListView):
    model = Objects
    template_name = 'space/index.html'
    context_object_name = 'posts'

    # extra_context = {'title': 'Главная страница'}   # Добавляем статический контекст

    # Функция для формирования динамического и статического контекста
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # Сохраняем сформированный контекст
        # context['menu'] = menu    # Добавляем динамический контекст
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0

        return context

    def get_queryset(self):  # Настройка запроса из БД
        return Objects.objects.filter(is_published=True)  # Фильтруем записи из БД


def about(request):
    context = {
        'title': "О сайте"
    }
    return render(request, 'space/about.html', context=context)


class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'space/addpage.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи'

        return context



def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse("Авторизация")


class ShowPost(DetailView):
    model = Objects
    template_name = 'space/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title

        return context


class SpaceCategory(ListView):
    model = Objects
    template_name = 'space/index.html'
    context_object_name = 'posts'
    allow_empty = False  # При отсутствии записей формируется ошибка 404

    def get_queryset(self):
        return Objects.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['cat_selected'] = context['posts'][0].cat_id

        return context


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
