from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
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


def addpage(request):
    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()
    return render(request, 'space/addpage.html', {'form': form, 'title': 'Добавление статьи'})


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse("Авторизация")


# def show_post(request, post_slug):
#     post = get_object_or_404(Objects, slug=post_slug)
#
#     context = {
#         'post': post,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'space/post.html', context=context)


class ShowPost(DetailView):
    model = Objects
    template_name = 'space/post.html'


class SpaceCategory(ListView):
    model = Objects
    template_name = 'space/index.html'
    context_object_name = 'posts'
    allow_empty = False     # При отсутствии записей формируется ошибка 404

    def get_queryset(self):
        return Objects.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['cat_selected'] = context['posts'][0].cat_id

        return context


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
