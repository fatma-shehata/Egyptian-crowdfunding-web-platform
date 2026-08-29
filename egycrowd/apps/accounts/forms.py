from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    mobile_phone = forms.CharField(max_length=20, required=True)
    profile_picture = forms.ImageField(required=False)
    birthdate = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    country = forms.CharField(max_length=100, required=True)
    facebook_profile = forms.URLField(required=False)  

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.mobile_phone = self.cleaned_data["mobile_phone"]
        user.birthdate = self.cleaned_data["birthdate"]
        user.country = self.cleaned_data["country"]
        if self.cleaned_data.get("profile_picture"):
            user.profile_picture = self.cleaned_data["profile_picture"]
        if self.cleaned_data.get("facebook_profile"):
            user.facebook_profile = self.cleaned_data["facebook_profile"]
        user.save()
        return user


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "mobile_phone", "profile_picture",
            "birthdate", "facebook_profile", "country",
        ]
        widgets = {
            "birthdate": forms.DateInput(attrs={"type": "date"}),
        }


class DeleteAccountForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label="Confirm your password")

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data["password"]
        if not self.user.check_password(password):
            raise forms.ValidationError("Incorrect password.")
        return password