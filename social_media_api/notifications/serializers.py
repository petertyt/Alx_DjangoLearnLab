from rest_framework import serializers
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model.
    """
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    actor_first_name = serializers.CharField(source='actor.first_name', read_only=True)
    actor_last_name = serializers.CharField(source='actor.last_name', read_only=True)
    message = serializers.CharField(read_only=True)
    target_title = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id',
            'actor_username',
            'actor_first_name',
            'actor_last_name',
            'verb',
            'message',
            'target_title',
            'is_read',
            'timestamp',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_target_title(self, obj):
        """Get the title of the target object if it exists."""
        if obj.target:
            if hasattr(obj.target, 'title'):
                return obj.target.title
            elif hasattr(obj.target, 'username'):
                return obj.target.username
        return None


class NotificationListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for notification lists.
    """
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    message = serializers.CharField(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id',
            'actor_username',
            'verb',
            'message',
            'is_read',
            'timestamp',
            'created_at'
        ]


class MarkAsReadSerializer(serializers.Serializer):
    """
    Serializer for marking notifications as read.
    """
    notification_ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="List of notification IDs to mark as read"
    )
