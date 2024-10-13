from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="index"),
    path("hunt/<int:hunt_id>", views.hunt_view, name="hunt"),
    path("hunt/<int:hunt_id>/choose-team", views.choose_team, name="choose_team"),
]
