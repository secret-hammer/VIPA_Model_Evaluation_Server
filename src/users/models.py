from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator


class User(AbstractUser):
    # Fields
    gender = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female')), blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    institute = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    homepage_link = models.URLField(blank=True, null=True)
    email = models.EmailField(
        max_length=254,
        validators=[EmailValidator()],
    )

    # Methods
    def __str__(self):
        return self.username

