from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Post(models.Model):
    """
    Post model representing social media posts with text and/or image content.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(
        blank=True,
        help_text="What's on your mind? Share your thoughts."
    )
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True,
        help_text="Attach an image (JPG, PNG, WEBP, max 10MB)"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']

    def __str__(self):
        snippet = (self.content[:30] + '...') if len(self.content) > 30 else (self.content or "[Image Post]")
        return f"Post by @{self.user.username}: {snippet}"

    def clean(self):
        super().clean()
        if not self.content and not self.image:
            raise ValidationError("A post must contain either text content or an image.")

    @property
    def has_image(self):
        return bool(self.image and hasattr(self.image, 'url'))
