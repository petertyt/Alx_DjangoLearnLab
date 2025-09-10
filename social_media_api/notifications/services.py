from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import Notification

User = get_user_model()


class NotificationService:
    """
    Service class for creating and managing notifications.
    """
    
    @staticmethod
    def create_notification(recipient, actor, verb, target=None):
        """
        Create a notification for a user.
        
        Args:
            recipient: User who receives the notification
            actor: User who performed the action
            verb: Type of action (like, comment, follow, unfollow)
            target: Object the action was performed on (optional)
        """
        # Don't create notification if user is acting on their own content
        if recipient == actor:
            return None
        
        # Create the notification
        notification = Notification.objects.create(
            recipient=recipient,
            actor=actor,
            verb=verb,
            target=target
        )
        return notification
    
    @staticmethod
    def create_like_notification(post, user):
        """Create a notification when someone likes a post."""
        return NotificationService.create_notification(
            recipient=post.author,
            actor=user,
            verb='like',
            target=post
        )
    
    @staticmethod
    def create_comment_notification(post, user):
        """Create a notification when someone comments on a post."""
        return NotificationService.create_notification(
            recipient=post.author,
            actor=user,
            verb='comment',
            target=post
        )
    
    @staticmethod
    def create_follow_notification(followed_user, follower):
        """Create a notification when someone follows a user."""
        return NotificationService.create_notification(
            recipient=followed_user,
            actor=follower,
            verb='follow'
        )
    
    @staticmethod
    def create_unfollow_notification(unfollowed_user, unfollower):
        """Create a notification when someone unfollows a user."""
        return NotificationService.create_notification(
            recipient=unfollowed_user,
            actor=unfollower,
            verb='unfollow'
        )
    
    @staticmethod
    def get_user_notifications(user, limit=None):
        """Get notifications for a user."""
        queryset = Notification.objects.filter(recipient=user).order_by('-created_at')
        if limit:
            queryset = queryset[:limit]
        return queryset
    
    @staticmethod
    def get_unread_count(user):
        """Get count of unread notifications for a user."""
        return Notification.objects.filter(recipient=user, is_read=False).count()
