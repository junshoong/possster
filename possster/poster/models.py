from django.db import models
from django.contrib.auth.models import User


class Poster(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='poster')
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=5000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    end = models.DateTimeField(null=True, blank=True)
