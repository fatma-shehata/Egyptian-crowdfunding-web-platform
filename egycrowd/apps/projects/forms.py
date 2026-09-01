from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone

from .models import Project, ProjectImage


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "details", "category", "tags", "total_target", "start_time", "end_time"]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "details": forms.Textarea(attrs={"rows": 6}),
        }

    def clean_total_target(self):
        target = self.cleaned_data["total_target"]
        if target <= 0:
            raise forms.ValidationError("Target must be a positive amount.")
        return target

    def clean_start_time(self):
        start = self.cleaned_data["start_time"]
        # Only enforce "can't be in the past" when the field actually
        # changed. On edit, the original start_time is naturally in the
        # past by now — that's expected and shouldn't block saving other
        # unrelated changes (title, details, images, etc).
        original_start = self.instance.start_time if self.instance.pk else None
        if start != original_start and start < timezone.now():
            raise forms.ValidationError("Start time cannot be in the past.")
        return start

    def clean(self):
        cleaned = super().clean()
        start, end = cleaned.get("start_time"), cleaned.get("end_time")
        if start and end and end <= start:
            raise forms.ValidationError("End time must be after start time.")
        return cleaned

class BaseProjectImageFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        # Ignore completely empty extra rows (no image uploaded, not marked
        # for deletion) instead of treating them as validation errors.
        for form in self.forms:
            if not form.cleaned_data:
                continue
            if not form.cleaned_data.get("image") and not form.cleaned_data.get("DELETE"):
                form.cleaned_data["DELETE"] = True


ProjectImageFormSet = inlineformset_factory(
    Project,
    ProjectImage,
    formset=BaseProjectImageFormSet,
    fields=["image"],
    extra=5,
    max_num=10,
    can_delete=True,
)