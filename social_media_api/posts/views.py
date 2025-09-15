from rest_framework import viewsets, status, filters, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Post, Comment, Like
from .serializers import (
    PostListSerializer, 
    PostDetailSerializer, 
    PostCreateUpdateSerializer,
    CommentSerializer,
    CommentCreateSerializer,
    PostWithCommentsSerializer,
    LikeSerializer
)
from notifications.services import NotificationService
from notifications.models import Notification
from .permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing posts.
    Provides CRUD operations for posts with filtering and search.
    """
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'content', 'author__username']
    ordering_fields = ['created_at', 'updated_at', 'likes_count', 'comments_count']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return PostListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        elif self.action == 'retrieve_with_comments':
            return PostWithCommentsSerializer
        return PostDetailSerializer

    def get_queryset(self):
        """Return posts with related data."""
        return Post.objects.select_related('author').prefetch_related('likes', 'comments')

    def perform_create(self, serializer):
        """Set the author to the current user when creating a post."""
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """Like or unlike a post."""
        post = generics.get_object_or_404(Post, pk=pk)
        user = request.user
        
        # Check if user has already liked this post
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            # Unlike the post
            like.delete()
            message = 'Post unliked'
        else:
            # Like the post and create notification
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb='like',
                target=post
            )
            message = 'Post liked'
        
        return Response({
            'message': message,
            'likes_count': post.post_likes.count()
        })

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        """Unlike a post."""
        post = generics.get_object_or_404(Post, pk=pk)
        user = request.user
        
        try:
            like = Like.objects.get(user=user, post=post)
            like.delete()
            message = 'Post unliked'
        except Like.DoesNotExist:
            message = 'Post was not liked'
        
        return Response({
            'message': message,
            'likes_count': post.post_likes.count()
        })

    @action(detail=True, methods=['get'])
    def retrieve_with_comments(self, request, pk=None):
        """Retrieve a post with all its comments."""
        post = self.get_object()
        serializer = self.get_serializer(post)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_posts(self, request):
        """Get posts by the current user."""
        posts = self.get_queryset().filter(author=request.user)
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def liked_posts(self, request):
        """Get posts liked by the current user."""
        posts = self.get_queryset().filter(likes=request.user)
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def feed(self, request):
        """Get feed of posts from users that the current user follows."""
        # Get posts from users that the current user follows
        following_users = request.user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing comments.
    Provides CRUD operations for comments with filtering.
    """
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['post', 'author']
    ordering_fields = ['created_at', 'updated_at', 'likes_count']
    ordering = ['created_at']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action in ['create']:
            return CommentCreateSerializer
        return CommentSerializer

    def get_queryset(self):
        """Return comments with related data."""
        return Comment.objects.select_related('author', 'post').prefetch_related('likes')

    def perform_create(self, serializer):
        """Set the author when creating a comment and create notification."""
        comment = serializer.save(author=self.request.user)
        # Create notification for the post author
        NotificationService.create_comment_notification(comment.post, self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """Like or unlike a comment."""
        comment = self.get_object()
        user = request.user
        
        if comment.likes.filter(id=user.id).exists():
            comment.likes.remove(user)
            message = 'Comment unliked'
        else:
            comment.likes.add(user)
            message = 'Comment liked'
        
        return Response({
            'message': message,
            'likes_count': comment.likes_count
        })

    @action(detail=False, methods=['get'])
    def my_comments(self, request):
        """Get comments by the current user."""
        comments = self.get_queryset().filter(author=request.user)
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)