from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(max_length=1000, blank=True)
    profile_pic = models.ImageField(upload_to='images', null=True, blank=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

