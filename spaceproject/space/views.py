from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404

menu =['О сайте', "Добавить статью", "Обратная связь", "Войти"]

def index(request):
    return render(request, 'space/index.html', {'menu': menu, 'title': 'Главная страница'})


def categories(request, catid):
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>{catid}</p>")


def archive(request, year):
    if int(year) > 2020 or int(year) < 2000:
        return redirect('home', permanent=True)
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
