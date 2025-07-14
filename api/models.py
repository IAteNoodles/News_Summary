from django.db import models
from django.conf import settings

class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    source_name = models.CharField(max_length=100)
    summary = models.TextField()
    published_at = models.DateTimeField()
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures a user cannot save the same article URL twice
        unique_together = ('user', 'url',)