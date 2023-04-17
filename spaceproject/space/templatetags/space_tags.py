from django import template
from space.models import *

register = template.Library()  # Экземляр класса, через который происходит регистрация собственных тегов


# Образец простого тега с принимаемым аргументом
@register.simple_tag(name='getcats')  # С помощью декоратора передаем функцию в тег
def get_categories(filter=None):
    if filter:
        return Category.objects.filter(pk=filter)
    else:
        return Category.objects.all()


@register.simple_tag(name='menu')
def get_menu():
    menu = [{'title': 'О сайте', 'url_name': 'about'},
            {'title': 'Добавить статью', 'url_name': 'add_page'},
            {'title': 'Обратная связь', 'url_name': 'contact'},
            {'title': 'Войти', 'url_name': 'login'}]
    return menu


# Вложенный тег
@register.inclusion_tag('space/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if sort:
        cats = Category.objects.order_by(sort)
    else:
        cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}  # Параметры передаются в шаблон list_categories.html

