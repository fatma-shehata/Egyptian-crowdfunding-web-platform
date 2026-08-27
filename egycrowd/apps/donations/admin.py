from django.contrib import admin
from .models import Donation


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("donor", "project", "amount", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("donor__email", "project__title")