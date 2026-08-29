from django.db.models import Q
from django.views.generic import DetailView, ListView

from .models import Project


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView

from .forms import ProjectForm, ProjectImageFormSet


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from apps.interactions.models import Comment, Rating
from .models import Category


from django.http import JsonResponse
from django.utils.text import slugify

from apps.interactions.models import Report


class ProjectListView(ListView):
    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"
    paginate_by = 12

    def get_queryset(self):
        qs = Project.objects.filter(is_cancelled=False).select_related("category")
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(Q(title__icontains=query) | Q(tags__name__icontains=query)).distinct()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["query"] = self.request.GET.get("q", "")
        return ctx


class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/project_detail.html"
    context_object_name = "project"
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        project = self.object
        ctx["similar_projects"] = project.similar_projects()
        ctx["comments"] = project.comments.filter(parent__isnull=True).select_related("user")
        return ctx


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_create.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # مفيش self.object هنا لسه (لسه المستخدم مبعتش الفورم)،
        # يعني similar_projects/comments مالهومش مكان — دي حاجات خاصة بصفحة التفاصيل بس.
        # اللي محتاجينه هنا هو الـ image_formset بس، وكان ناقص من قبل.
        if self.request.POST:
            ctx["image_formset"] = ProjectImageFormSet(self.request.POST, self.request.FILES)
        else:
            ctx["image_formset"] = ProjectImageFormSet()
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        image_formset = ctx["image_formset"]
        form.instance.creator = self.request.user
        if image_formset.is_valid():
            self.object = form.save()
            image_formset.instance = self.object
            image_formset.save()
            messages.success(self.request, "Your project is live!")
            return redirect(self.object.get_absolute_url())
        return self.render_to_response(self.get_context_data(form=form))


@login_required
@require_POST
def add_comment(request, slug):
    project = get_object_or_404(Project, slug=slug)
    body = request.POST.get("body", "").strip()
    parent_id = request.POST.get("parent_id")

    if body:
        comment = Comment(project=project, user=request.user, body=body)
        if parent_id:
            comment.parent_id = parent_id
        comment.save()
    return redirect(project.get_absolute_url())


@login_required
@require_POST
def rate_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    score = int(request.POST.get("score", 0))
    if 1 <= score <= 5:
        Rating.objects.update_or_create(
            project=project, user=request.user, defaults={"score": score}
        )
    return redirect(project.get_absolute_url())


class CategoryProjectsView(ListView):
    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"
    paginate_by = 12

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return Project.objects.filter(category=self.category, is_cancelled=False)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["category"] = self.category
        return ctx


@login_required
@require_POST
def add_category_ajax(request):
    name = request.POST.get("name", "").strip()
    if not name:
        return JsonResponse({"success": False, "error": "Category name is required."})

    category, created = Category.objects.get_or_create(
        name=name, defaults={"slug": slugify(name)}
    )
    return JsonResponse({"success": True, "id": category.id, "name": category.name})

@login_required
@require_POST
def cancel_project(request, slug):
    project = get_object_or_404(Project, slug=slug, creator=request.user)

    if not project.can_be_cancelled:
        messages.error(request, "This project can't be cancelled — donations have already reached 25% or more of the target.")
    else:
        project.is_cancelled = True
        project.save(update_fields=["is_cancelled"])
        messages.success(request, "Your project has been cancelled.")

    return redirect(project.get_absolute_url())




@login_required
@require_POST
def report_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    reason = request.POST.get("reason", "").strip()
    if reason:
        Report.objects.create(
            reporter=request.user,
            report_type="project",
            project=project,
            reason=reason,
        )
    return JsonResponse({"success": True})