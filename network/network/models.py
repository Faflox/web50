from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    description = models.CharField(max_length=255, default="") 
    profilePicture = models.ImageField(null=True, blank=True, upload_to="images", default="profilePictures/default.png")
