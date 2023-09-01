from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    descriptions = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='media', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    like = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    
    # def __str__(self):
    #     return self.descriptions
    
