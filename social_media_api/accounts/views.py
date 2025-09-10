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

