from django import template
from space.models import *

register = template.Library()


def get_categories():
    return Category.objects.all()
