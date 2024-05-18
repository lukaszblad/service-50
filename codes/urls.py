from django.urls import path

from . import views

urlpatterns = [
    path("add_ci", views.add_configuration_item, name='add_ci'),
    path('add_user', views.add_user, name='add_user'),
    path("get_user/<str:criteria>", views.search_user, name="search_user"),
    path("get_team/<str:criteria>", views.search_team, name="search_team"),
    path("get_lctn/<str:criteria>", views.search_location, name="search_location"),
    path("get_srvc/<str:criteria>", views.search_service, name="search_service"),
    path("get_conf/<str:criteria>", views.search_ci, name="search_ci"),
    path("get_assignees/<str:team>", views.search_assignees, name="search_assignee"),
    path("entry_added", views.entry_added, name='entry_added'),
]