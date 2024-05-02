from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, default="", null=True, blank=True) 
    profilePicture = models.ImageField(null=True, blank=True, upload_to="images")
    

class Post(models.Model):
    content = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.content
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post")
    
class Followers(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="is_following")
    follower_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_by")
    def __str__(self):
        return f"{self.user_id} is following {self.follower_id}"