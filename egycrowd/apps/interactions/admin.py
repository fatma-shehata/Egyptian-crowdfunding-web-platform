from django.contrib import admin
from .models import Comment, Rating, Report


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "project", "parent", "created_at")
    search_fields = ("body", "user__email")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("user", "project", "score")
    list_filter = ("score",)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("reporter", "report_type", "project", "comment", "is_resolved", "created_at")
    list_filter = ("report_type", "is_resolved")
    actions = ["mark_resolved"]

    @admin.action(description="Mark selected reports as resolved")
    def mark_resolved(self, request, queryset):
        queryset.update(is_resolved=True)