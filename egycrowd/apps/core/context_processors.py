from django.db.models import Sum, Count
from apps.projects.models import Project, Category
from apps.donations.models import Donation
from apps.accounts.models import User


def admin_dashboard_stats(request):
    """Computes stats only when viewing the admin, to avoid unnecessary
    database queries on every page of the site."""
    if not request.path.startswith('/admin/'):
        return {}

    total_users = User.objects.count()
    total_projects = Project.objects.count()
    total_donations = Donation.objects.filter(status='completed').aggregate(
        total=Sum('amount')
    )['total'] or 0

    categories_data = (
        Category.objects.annotate(project_count=Count('projects'))
        .values('name', 'project_count')
    )

    return {
        'dashboard_total_users': total_users,
        'dashboard_total_projects': total_projects,
        'dashboard_total_donations': total_donations,
        'dashboard_category_labels': [c['name'] for c in categories_data],
        'dashboard_category_data': [c['project_count'] for c in categories_data],
    }