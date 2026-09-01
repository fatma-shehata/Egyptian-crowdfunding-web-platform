from django.urls import path
from .views import HomepageView, contact_view

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path("contact/", contact_view, name="contact"),
]