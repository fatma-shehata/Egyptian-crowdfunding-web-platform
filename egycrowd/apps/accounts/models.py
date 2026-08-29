from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import validate_egyptian_phone


class User(AbstractUser):
    email = models.EmailField(unique=True)
    mobile_phone = models.CharField(
            max_length=20, unique=True, validators=[validate_egyptian_phone]
            )
    profile_picture = models.ImageField(
        upload_to='profiles/', blank=True, null=True
    )

    birthdate = models.DateField(null=True, blank=True)
    facebook_profile = models.URLField(blank=True)
    country = models.CharField(max_length=100, blank=True, default='Egypt')

    is_activated = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'mobile_phone']

    def __str__(self):
        return f"{self.get_full_name()} <{self.email}>"


class RegularUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_staff=False)


class AdminUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_staff=True)


class RegularUser(User):
    """Proxy model — same database table as User, but shows only
    non-staff (regular donors/creators) in a separate admin section."""
    objects = RegularUserManager()

    class Meta:
        proxy = True
        verbose_name = "Regular User"
        verbose_name_plural = "Regular Users"


class AdminUser(User):
    """Proxy model — same database table as User, but shows only
    staff/admin accounts in a separate admin section."""
    objects = AdminUserManager()

    class Meta:
        proxy = True
        verbose_name = "Admin User"
        verbose_name_plural = "Admin Users"