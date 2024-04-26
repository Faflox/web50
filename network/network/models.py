from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    description = models.CharField(max_length=255, default="") 
    profilePicture = models.ImageField(null=True, blank=True, upload_to="images")

class Post(models.Model):
    content = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    def __str__(self):
        return self.content