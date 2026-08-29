from django.urls import path
from . import views

app_name = "projects"

urlpatterns = [
    path("", views.ProjectListView.as_view(), name="project_list"),
    path("create/", views.ProjectCreateView.as_view(), name="project_create"),
    path("category/add/", views.add_category_ajax, name="add_category_ajax"),
    path("category/<slug:slug>/", views.CategoryProjectsView.as_view(), name="category_projects"),
    path("<slug:slug>/", views.ProjectDetailView.as_view(), name="project_detail"),
    path("<slug:slug>/comment/", views.add_comment, name="add_comment"),
    path("<slug:slug>/rate/", views.rate_project, name="project_rate"),
    path("<slug:slug>/cancel/", views.cancel_project, name="project_cancel"),
    path("<slug:slug>/report/", views.report_project, name="report_project"),
]