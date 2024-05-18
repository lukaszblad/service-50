from django.urls import path

from . import views

urlpatterns = [
    path("default_dashboard", views.default_dashboard, name="default_dashboard"),
    path("profile_dashboard/<str:owner_username>", views.profile_dashboard, name="profile_dashboard"),
    path("team_dashboard/<str:team_code>", views.team_dashboard, name="team_dashboard"),
    path("configuration_item_dashboard/<str:ci_code>", views.configuration_item_dashboard, name="configuration_item_dashboard"),
    path("service_dashboard/<str:service_code>", views.service_dashboard, name="service_dashboard"),
]