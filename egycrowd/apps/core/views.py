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

#=======================================================================================================

from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from .forms import ContactForm
from .models import ContactMessage


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(**form.cleaned_data)

            # Send an automatic confirmation email to the user (not a real
            # reply to their question — just an acknowledgment that we
            # received it, same pattern as the activation email).
            send_mail(
                subject="We received your message — EgyCrowd",
                message=(
                    f"Hi {form.cleaned_data['name']},\n\n"
                    "Thanks for reaching out to EgyCrowd! We've received your message:\n\n"
                    f"Subject: {form.cleaned_data['subject']}\n"
                    f"Message: {form.cleaned_data['message']}\n\n"
                    "Our team will get back to you within 1-2 business days.\n\n"
                    "— The EgyCrowd Team"
                ),
                from_email=None,  # uses DEFAULT_FROM_EMAIL from settings
                recipient_list=[form.cleaned_data['email']],
                fail_silently=True,
            )

            messages.success(request, "Thanks for reaching out! We've sent a confirmation to your email, and we'll get back to you soon.")
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "core/contact.html", {"form": form})