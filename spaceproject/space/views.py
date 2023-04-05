from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .models import *

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'}]


def index(request):
    posts = Objects.objects.all()
    cats = Category.objects.all()
    context = {
        'posts': posts,
        'menu': menu,
        'cats': cats,
        'title': "Главная страница",
        'cat_selected': 0,
    }
    return render(request, 'space/index.html', context=context)


def about(request):
    context = {
        'menu': menu,
        'title': "О сайте"
    }
    return render(request, 'space/about.html', context=context)


def addpage(request):
    return HttpResponse('Добавить статью')


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse("Авторизация")


def show_post(request, post_id):
    return HttpResponse(f"Отображение статьи с id = {post_id}")


def show_category(request, cat_id):
    posts = Objects.objects.filter(cat_id=cat_id)
    if len(posts) == 0:
        raise Http404()
    
    cats = Category.objects.all()
    context = {
        'posts': posts,
        'menu': menu,
        'cats': cats,
        'title': "Отображение по рубрикам",
        'cat_selected': cat_id,
    }
    return render(request, 'space/index.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
