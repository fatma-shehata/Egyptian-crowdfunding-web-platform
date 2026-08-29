from django.db.models import Avg
from django.utils import timezone
from django.views.generic import TemplateView

from apps.projects.models import Project, Category


class HomepageView(TemplateView):
    template_name = "core/homepage.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        now = timezone.now()

        ctx["top_rated_projects"] = (
            Project.objects.filter(start_time__lte=now, end_time__gte=now, is_cancelled=False)
            .annotate(avg_rating=Avg("ratings__score"))
            .order_by("-avg_rating")[:5]
        )
        ctx["latest_projects"] = Project.objects.filter(is_cancelled=False).order_by("-created_at")[:5]
        ctx["featured_projects"] = Project.objects.filter(is_featured=True, is_cancelled=False)[:5]
        ctx["categories"] = Category.objects.all()
        return ctx


