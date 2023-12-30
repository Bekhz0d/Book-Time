from django.db import models
from django.contrib.auth.models import AbstractUser


class Readers(AbstractUser):
    picture = models.ImageField(default='profile_pictures/anonim_user.png', upload_to='profile_pictures/')
    address = models.CharField(max_length=300, blank=True, null=True)
    phone = models.CharField(max_length=13)

    class Meta:
        verbose_name = 'Reader'
        verbose_name_plural = 'Readers'
        