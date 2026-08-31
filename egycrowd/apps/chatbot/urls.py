from django.urls import path
from .views import chat_api

app_name = "chatbot"

urlpatterns = [
    path("api/", chat_api, name="chat_api"),
]