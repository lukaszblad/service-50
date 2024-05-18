from django.urls import path

from . import views

urlpatterns = [
    path('', views.default_search, name='default_search'),
]