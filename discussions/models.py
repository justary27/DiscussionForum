from django.db import models

from users.models import CustomUser


class Discussion(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='discussions')
    text = models.TextField()
    image = models.ImageField(upload_to='discussion_images/', null=True, blank=True)
    hashtags = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='likes')
    created_on = models.DateTimeField(auto_now_add=True)
