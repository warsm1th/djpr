from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .models import *
from .forms import *


def index(request):
    posts = Objects.objects.all()
    context = {
        'posts': posts,
        'title': "Главная страница",
        'cat_selected': 0,
    }
    return render(request, 'space/index.html', context=context)


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


def show_post(request, post_slug):
    post = get_object_or_404(Objects, slug=post_slug)

    context = {
        'post': post,
        'title': post.title,
        'cat_selected': post.cat_id,
    }

    return render(request, 'space/post.html', context=context)


def show_category(request, cat_slug):
    cat = Category.objects.get(slug=cat_slug)
    posts = Objects.objects.filter(cat_id=cat.pk)
    if len(posts) == 0:
        raise Http404()

    context = {
        'posts': posts,
        'title': "Отображение по рубрикам",
        'cat_selected': cat.pk,
    }
    return render(request, 'space/index.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
