from django.urls import path

from . import views

app_name = "clasificador"

urlpatterns = [
    path("", views.inicio, name="inicio"),
]
