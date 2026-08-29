from django.urls import path
from . import views

app_name = "interactions"

urlpatterns = [
    path("comment/<int:comment_id>/report/", views.report_comment, name="report_comment"),
]