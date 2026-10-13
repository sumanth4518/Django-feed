from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static


class Profile(models.Model):
    """
    Profile model extending the built-in Django User model.
    Stores additional user information like profile picture and biography.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        help_text="Upload a square profile picture (JPEG, PNG, WEBP)"
    )
    bio = models.TextField(blank=True, max_length=500, help_text="Short bio about yourself")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def display_name(self):
        full = f"{self.user.first_name} {self.user.last_name}".strip()
        return full if full else self.user.username

    @property
    def avatar_url(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        return static('images/default-avatar.svg')

    @property
    def post_count(self):
        return self.user.posts.count()
