from django.db.models import Sum, Avg, Q

from apps.projects.models import Project, Category
from apps.donations.models import Donation
from apps.accounts.models import User

# ---------------------------------------------------------------------------
# Each function here is one "tool" the model can call. The new google-genai
# SDK reads each function's type hints + docstring automatically to build
# its own schema — no manual JSON schema needed like the old Groq version.
# Keep return values as plain dicts/lists (JSON-serializable) — never
# return Django model instances directly.
# ---------------------------------------------------------------------------

def get_top_donated_projects(limit: int = 5) -> list:
    """Get the projects that have raised the most money (highest total donations).
    Use this when the user asks about the top, best, or highest funded project(s).

    Args:
        limit: How many projects to return, default 5.
    """
    projects = (
        Project.objects.filter(is_cancelled=False)
        .annotate(total_raised=Sum("donations__amount"))
        .order_by("-total_raised")[:limit]
    )
    return [
        {
            "title": p.title,
            "total_raised": float(p.total_raised or 0),
            "target": float(p.total_target),
            "category": p.category.name if p.category else None,
            "url": f"/projects/{p.slug}/",
        }
        for p in projects
    ]


def get_lowest_donated_projects(limit: int = 5) -> list:
    """Get the projects that have raised the least money.
    Use this when the user asks about the lowest, weakest, or least funded project(s).

    Args:
        limit: How many projects to return, default 5.
    """
    projects = (
        Project.objects.filter(is_cancelled=False)
        .annotate(total_raised=Sum("donations__amount"))
        .order_by("total_raised")[:limit]
    )
    return [
        {
            "title": p.title,
            "total_raised": float(p.total_raised or 0),
            "target": float(p.total_target),
            "category": p.category.name if p.category else None,
            "url": f"/projects/{p.slug}/",
        }
        for p in projects
    ]


def get_top_rated_projects(limit: int = 5) -> list:
    """Get the highest-rated projects by average star rating.

    Args:
        limit: How many projects to return, default 5.
    """
    projects = (
        Project.objects.filter(is_cancelled=False)
        .annotate(avg_rating=Avg("ratings__score"))
        .order_by("-avg_rating")[:limit]
    )
    return [
        {
            "title": p.title,
            "average_rating": round(p.avg_rating or 0, 1),
            "category": p.category.name if p.category else None,
            "url": f"/projects/{p.slug}/",
        }
        for p in projects
    ]


def get_platform_stats() -> dict:
    """Get overall platform statistics: total number of projects, total
    donations raised across the whole platform, total number of donors,
    total categories."""
    return {
        "total_projects": Project.objects.filter(is_cancelled=False).count(),
        "total_donations_egp": float(
            Donation.objects.filter(status="completed").aggregate(t=Sum("amount"))["t"] or 0
        ),
        "total_donors": Donation.objects.values("donor").distinct().count(),
        "total_categories": Category.objects.count(),
    }


def search_projects(query: str, limit: int = 5) -> list:
    """Search for projects by keyword in their title or tags.

    Args:
        query: Search keyword.
        limit: Max results, default 5.
    """
    projects = Project.objects.filter(
        Q(title__icontains=query) | Q(tags__name__icontains=query),
        is_cancelled=False,
    ).distinct()[:limit]
    return [
        {
            "title": p.title,
            "category": p.category.name if p.category else None,
            "progress_percent": p.progress_percent,
            "url": f"/projects/{p.slug}/",
        }
        for p in projects
    ]


def get_projects_by_category(category_name: str, limit: int = 5) -> list:
    """Get projects that belong to a specific category.

    Args:
        category_name: Category name, e.g. Education, Health.
        limit: Max results, default 5.
    """
    projects = Project.objects.filter(
        category__name__icontains=category_name, is_cancelled=False
    )[:limit]
    return [
        {
            "title": p.title,
            "progress_percent": p.progress_percent,
            "url": f"/projects/{p.slug}/",
        }
        for p in projects
    ]


def get_all_categories() -> list:
    """List all available project categories on the platform."""
    return list(Category.objects.values_list("name", flat=True))




def get_current_user_info(user_id: int) -> dict:
    """Get information about the currently logged-in user: their name,
    email, mobile phone, country, how many projects they've created, and
    their total donation history. Use this whenever the user asks about
    themselves — e.g. "what are my projects", "how much have I donated",
    "what's my name", "show my profile".

    Args:
        user_id: The internal ID of the currently authenticated user.
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return {"error": "User not found."}

    my_projects = user.projects.filter(is_cancelled=False).values(
        "title", "total_target", "progress_percent"
    )
    my_donations = user.donations.filter(status="completed")

    return {
        "full_name": user.get_full_name(),
        "email": user.email,
        "country": user.country or None,
        "member_since": user.date_joined.strftime("%B %Y"),
        "projects_created": list(my_projects),
        "total_donated_egp": float(
            my_donations.aggregate(total=Sum("amount"))["total"] or 0
        ),
        "number_of_donations": my_donations.count(),
    }
# ---------------------------------------------------------------------------
# List of tool functions the model can call directly.
# ---------------------------------------------------------------------------
CHATBOT_TOOLS = [
    get_top_donated_projects,
    get_lowest_donated_projects,
    get_top_rated_projects,
    get_platform_stats,
    search_projects,
    get_projects_by_category,
    get_all_categories,
    get_current_user_info
]