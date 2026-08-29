from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from apps.projects.models import Project
from .forms import DonationForm
from .models import Donation


@login_required
@require_POST
def donate_ajax(request, slug):
    project = get_object_or_404(Project, slug=slug, is_cancelled=False)

    if not project.is_running:
        return JsonResponse({"success": False, "error": "This project is not accepting donations right now."})

    form = DonationForm(request.POST)
    if form.is_valid():
        donation = form.save(commit=False)
        donation.project = project
        donation.donor = request.user
        donation.status = "completed"
        donation.save()

        return JsonResponse({
            "success": True,
            "total_donated": float(project.total_donated),
            "progress_percent": float(project.progress_percent),
            "amount": float(donation.amount),
        })

    return JsonResponse({"success": False, "error": "Please enter a valid amount."})