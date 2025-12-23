from django.db import models
from posts.models import Post
from django.conf import settings
# Create your models here.



User = settings.AUTH_USER_MODEL


class Repost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='reposts'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'original_post')
        indexes = [
            models.Index(fields=['original_post']),
        ]
