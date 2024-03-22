from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    categoryName=models.CharField(max_length=100)
    
    def __str__(self):
        return self.categoryName

class Listing(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    description = models.CharField(max_length=500)
    image = models.CharField(max_length=500, blank=True)
    starting_price = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    price = models.IntegerField()
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(max_length=500)