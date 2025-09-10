from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, get_user_model
from .models import User

User = get_user_model()
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserProfileSerializer,
    UserUpdateSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Register a new user.
    
    POST /api/accounts/register/
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'User registered successfully',
            'token': token.key,
            'user': UserProfileSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login a user and return a token.
    
    POST /api/accounts/login/
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response({
            'message': 'Login successful',
            'token': token.key,
            'user': UserProfileSerializer(user).data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    Get the current user's profile.
    
    GET /api/accounts/profile/
    """
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update the current user's profile.
    
    PUT/PATCH /api/accounts/profile/
    """
    partial = request.method == 'PATCH'
    serializer = UserUpdateSerializer(request.user, data=request.data, partial=partial)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Profile updated successfully',
            'user': UserProfileSerializer(request.user).data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Logout the current user by deleting their token.
    
    POST /api/accounts/logout/
    """
    try:
        request.user.auth_token.delete()
        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
    except:
        return Response({
            'error': 'Error during logout'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    """
    Follow a user.
    
    POST /api/accounts/follow/{user_id}/
    """
    try:
        user_to_follow = User.objects.get(id=user_id)
        if user_to_follow == request.user:
            return Response({
                'error': 'Cannot follow yourself'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if user_to_follow in request.user.following.all():
            return Response({
                'error': 'Already following this user'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.following.add(user_to_follow)
        
        return Response({
            'message': 'Followed successfully',
            'following_count': request.user.following_count
        }, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response({
            'error': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    """
    Unfollow a user.
    
    POST /api/accounts/unfollow/{user_id}/
    """
    try:
        user_to_unfollow = User.objects.get(id=user_id)
        if user_to_unfollow == request.user:
            return Response({
                'error': 'Cannot unfollow yourself'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if user_to_unfollow not in request.user.following.all():
            return Response({
                'error': 'Not following this user'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.following.remove(user_to_unfollow)
        
        return Response({
            'message': 'Unfollowed successfully',
            'following_count': request.user.following_count
        }, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response({
            'error': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def following_list(request):
    """
    Get list of users that the current user is following.
    
    GET /api/accounts/following/
    """
    following_users = request.user.following.all()
    serializer = UserProfileSerializer(following_users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def followers_list(request):
    """
    Get list of users that follow the current user.
    
    GET /api/accounts/followers/
    """
    followers = request.user.followers.all()
    serializer = UserProfileSerializer(followers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

