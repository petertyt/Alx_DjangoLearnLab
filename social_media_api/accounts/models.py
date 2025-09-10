from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Adds bio, profile_picture, and followers fields for social media functionality.
    """
    bio = models.TextField(max_length=500, blank=True, null=True, help_text="User's bio/description")
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', 
        blank=True, 
        null=True,
        help_text="User's profile picture"
    )
    followers = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='following',
        blank=True,
        help_text="Users that this user follows"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    @property
    def followers_count(self):
        """Return the number of followers."""
        return self.followers.count()

    @property
    def following_count(self):
        """Return the number of users this user follows."""
        return self.following.count()

    class Meta:
        db_table = 'accounts_user'
