from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()


class PostListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing posts (minimal data).
    """
    author = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'author', 'created_at', 
            'likes_count', 'comments_count'
        )


class PostDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed post view.
    """
    author = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'content', 'author', 'created_at', 'updated_at',
            'likes_count', 'comments_count', 'is_liked'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_is_liked(self, obj):
        """Check if the current user has liked this post."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating posts.
    """
    class Meta:
        model = Post
        fields = ('title', 'content')

    def create(self, validated_data):
        """Create a new post with the current user as author."""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for comments.
    """
    author = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'id', 'content', 'author', 'created_at', 'updated_at',
            'likes_count', 'is_liked'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_is_liked(self, obj):
        """Check if the current user has liked this comment."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

    def create(self, validated_data):
        """Create a new comment with the current user as author."""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class CommentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating comments.
    """
    class Meta:
        model = Comment
        fields = ('post', 'content')

    def create(self, validated_data):
        """Create a new comment with the current user as author."""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostWithCommentsSerializer(serializers.ModelSerializer):
    """
    Serializer for posts with their comments.
    """
    author = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'content', 'author', 'created_at', 'updated_at',
            'likes_count', 'comments_count', 'is_liked', 'comments'
        )

    def get_is_liked(self, obj):
        """Check if the current user has liked this post."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False
