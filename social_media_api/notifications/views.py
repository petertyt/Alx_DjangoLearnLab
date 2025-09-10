from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Notification
from .serializers import NotificationSerializer, NotificationListSerializer, MarkAsReadSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for managing notifications.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        """Return notifications for the current user."""
        return Notification.objects.filter(recipient=self.request.user)

    def list(self, request, *args, **kwargs):
        """List notifications with optional filtering."""
        queryset = self.get_queryset()
        
        # Filter by read status
        is_read = request.query_params.get('is_read')
        if is_read is not None:
            queryset = queryset.filter(is_read=is_read.lower() == 'true')
        
        # Filter by notification type
        verb = request.query_params.get('verb')
        if verb:
            queryset = queryset.filter(verb=verb)
        
        # Order by most recent first
        queryset = queryset.order_by('-created_at')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread notifications."""
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'unread_count': count})

    @action(detail=False, methods=['post'])
    def mark_as_read(self, request):
        """Mark specific notifications as read."""
        serializer = MarkAsReadSerializer(data=request.data)
        if serializer.is_valid():
            notification_ids = serializer.validated_data['notification_ids']
            notifications = self.get_queryset().filter(id__in=notification_ids)
            updated_count = notifications.update(is_read=True)
            return Response({
                'message': f'{updated_count} notifications marked as read',
                'updated_count': updated_count
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Mark all notifications as read."""
        updated_count = self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({
            'message': f'{updated_count} notifications marked as read',
            'updated_count': updated_count
        })

    @action(detail=True, methods=['post'])
    def mark_single_as_read(self, request, pk=None):
        """Mark a single notification as read."""
        notification = self.get_object()
        if not notification.is_read:
            notification.mark_as_read()
            return Response({'message': 'Notification marked as read'})
        return Response({'message': 'Notification was already read'})