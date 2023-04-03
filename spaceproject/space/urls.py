from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('categories/<int:catid>/', categories),
    re_path(r'^archive/(?P<year>\d{4})/', archive)
]