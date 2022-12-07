from django.urls import path


app_name = "order"
from . import views

urlpatterns = [
    path("trackord/", views.tracker, name="tracker"),
]
