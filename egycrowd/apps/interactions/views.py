from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from .models import Comment, Report


@login_required
@require_POST
def report_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    reason = request.POST.get("reason", "").strip()
    if reason:
        Report.objects.create(
            reporter=request.user,
            report_type="comment",
            comment=comment,
            reason=reason,
        )
    return JsonResponse({"success": True})