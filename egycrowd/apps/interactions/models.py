from django.conf import settings
from django.db import models


class Comment(models.Model):
    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )
    body = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.user} on {self.project}"


class Rating(models.Model):
    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, related_name="ratings"
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ("project", "user")

    def __str__(self):
        return f"{self.user} rated {self.project}: {self.score}/5"


class Report(models.Model):
    REPORT_TYPE_CHOICES = (("project", "Project"), ("comment", "Comment"))

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=10, choices=REPORT_TYPE_CHOICES)
    project = models.ForeignKey(
        "projects.Project", null=True, blank=True, on_delete=models.CASCADE, related_name="reports"
    )
    comment = models.ForeignKey(
        Comment, null=True, blank=True, on_delete=models.CASCADE, related_name="reports"
    )
    reason = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        target = self.project if self.report_type == "project" else self.comment
        return f"Report ({self.report_type}) by {self.reporter} on {target}"