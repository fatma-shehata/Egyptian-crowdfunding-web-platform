from django.contrib import admin
from .models import Category, Project, ProjectImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'category', 'total_target', 'is_featured', 'is_cancelled')
    list_filter = ('is_featured', 'is_cancelled', 'category')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]