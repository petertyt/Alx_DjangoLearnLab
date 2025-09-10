from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError

User = get_user_model()


class Post(models.Model):
    """
    Post model for social media posts.
    """
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='posts',
        help_text="The user who created this post"
    )
    title = models.CharField(
        max_length=200, 
        help_text="The title of the post"
    )
    content = models.TextField()
    description = models.TextField(
        blank=True,
        null=True,
        help_text="The main content of the post"
    )
    summary = models.TextField(
        blank=True,
        null=True,
        help_text="Optional summary of the post"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the post was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When the post was last updated"
    )
    likes = models.ManyToManyField(
        User,
        related_name='liked_posts',
        blank=True,
        help_text="Users who liked this post"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f"{self.title} by {self.author.username}"

    @property
    def likes_count(self):
        """Return the number of likes."""
        return self.likes.count()

    @property
    def comments_count(self):
        """Return the number of comments."""
        return self.comments.count()

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    """
    Comment model for post comments.
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="The post this comment belongs to"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="The user who wrote this comment"
    )
    content = models.TextField()
    message = models.TextField(
        blank=True,
        null=True,
        help_text="The content of the comment"
    )
    reply_to = models.TextField(
        blank=True,
        null=True,
        help_text="Optional reply to another comment"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the comment was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When the comment was last updated"
    )
    likes = models.ManyToManyField(
        User,
        related_name='liked_comments',
        blank=True,
        help_text="Users who liked this comment"
    )

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

    @property
    def likes_count(self):
        """Return the number of likes."""
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('comment-detail', kwargs={'pk': self.pk})


class Like(models.Model):
    """
    Like model for tracking post likes.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes',
        help_text="The user who liked the post"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='post_likes',
        help_text="The post that was liked"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"

    def clean(self):
        if self.user == self.post.author:
            raise ValidationError("Users cannot like their own posts.")