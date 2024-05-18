from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("incident/<str:code>", views.incident, name="incident"),
    path("incident/<str:code>/data", views.incident_information, name="incident_information"),
    path('new_incident', views.new_incident, name='new_incident'),
    path('update_incident', views.update_incident, name='update_incident'),
    path("incident/<str:code>/work_notes", views.work_notes, name="work_notes"),
    path("get_current_user", views.get_current_user, name="get_current_user"),
]
