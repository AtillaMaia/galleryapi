from django.db import models

from ..authentication.models import User


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False,
                              blank=False)
    photo = models.ImageField(upload_to='media/', null=False, blank=False)
    approved = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='related_likes')

    class Meta:
        ordering = ['approved', '-created_at']

    def __str__(self):
        return self.owner.username


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False,
                              blank=False)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
