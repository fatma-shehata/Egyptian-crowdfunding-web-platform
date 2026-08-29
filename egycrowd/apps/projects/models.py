from django.conf import settings
from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Project(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects'
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    details = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='projects'
    )
    tags = TaggableManager(blank=True)

    total_target = models.DecimalField(max_digits=12, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    is_featured = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse("projects:project_detail", kwargs={"slug": self.slug})

    @property
    def total_donated(self):
        from django.db.models import Sum
        return self.donations.aggregate(total=Sum('amount'))['total'] or 0

    @property
    def progress_percent(self):
        if not self.total_target:
            return 0
        return round(min((self.total_donated / self.total_target) * 100, 100), 1)

    @property
    def average_rating(self):
        from django.db.models import Avg
        return self.ratings.aggregate(avg=Avg('score'))['avg'] or 0

    @property
    def is_running(self):
        from django.utils import timezone
        now = timezone.now()
        return self.start_time <= now <= self.end_time and not self.is_cancelled

    @property
    def can_be_cancelled(self):
        return self.progress_percent < 25

    def similar_projects(self, count=4):
            tag_ids = self.tags.values_list('id', flat=True)
            return (
                    Project.objects.filter(tags__in=tag_ids, is_cancelled=False)
                    .exclude(id=self.id)
                    .distinct()[:count]
                    )
class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/%Y/%m/')
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']