from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
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
        return Objects.objects.filter(is_published=True).select_related('cat')  # Фильтруем записи из БД
                                                        # и делаем жадную загрузку связанных данных


def about(request):
    return render(request, 'space/about.html',
                  {'menu': menu, 'title': 'О сайте'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'space/addpage.html'
    success_url = reverse_lazy('home')  # Перенаправление при успешном добавлении статьи
    login_url = reverse_lazy('home')  # Перенаправление при отсутствии авторизации
    raise_exception = True  # ошибка 403 "Доступ запрещен" при отсутствии авторизации

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Добавление статьи')
        return context | mixin_context


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'space/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Обратная связь')
        return context | mixin_context

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


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
        return Objects.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        title = 'Категория - ' + str(c.name)
        mixin_context = self.get_user_context(title=title, cat_selected=c.pk)
        return context | mixin_context


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'space/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        mixin_context = self.get_user_context(title='Регистрация')
        return context | mixin_context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'space/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        mixin_context = self.get_user_context(title='Авторизация')
        return context | mixin_context

    def get_success_url(self):
        return reverse_lazy('home')


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def logout_user(request):
    logout(request)
    return redirect('login')
