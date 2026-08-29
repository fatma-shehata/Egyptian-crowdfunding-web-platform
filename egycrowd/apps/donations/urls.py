from django.urls import path
from . import views

app_name = "donations"

urlpatterns = [
    path("<slug:slug>/donate/", views.donate_ajax, name="donate_ajax"),
]