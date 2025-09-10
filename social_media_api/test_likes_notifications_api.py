#!/usr/bin/env python3
"""
Test script for the Likes and Notifications API functionality.
Run this script to test all likes and notifications endpoints.
"""

import requests
import json

# API base URL
BASE_URL = "http://127.0.0.1:8000/api"

def get_auth_token():
    """Get authentication token by logging in."""
    print("🔐 Getting authentication token...")
    
    # First try to register a new user
    register_url = f"{BASE_URL}/accounts/register/"
    register_data = {
        "username": "liketest",
        "email": "liketest@example.com",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "first_name": "Like",
        "last_name": "Test",
        "bio": "Test user for likes and notifications"
    }
    
    try:
        response = requests.post(register_url, json=register_data)
        if response.status_code == 201:
            print("✅ User registered successfully")
            return response.json()['token']
    except:
        pass
    
    # If registration fails, try to login
    login_url = f"{BASE_URL}/accounts/login/"
    login_data = {
        "username": "liketest",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(login_url, json=login_data)
        if response.status_code == 200:
            print("✅ User logged in successfully")
            return response.json()['token']
    except:
        pass
    
    print("❌ Failed to get authentication token")
    return None

def create_second_user():
    """Create a second user for testing likes and notifications."""
    print("\n👤 Creating second user...")
    
    register_url = f"{BASE_URL}/accounts/register/"
    register_data = {
        "username": "liketest2",
        "email": "liketest2@example.com",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "first_name": "Like2",
        "last_name": "Test2",
        "bio": "Second test user for likes"
    }
    
    try:
        response = requests.post(register_url, json=register_data)
        if response.status_code == 201:
            print("✅ Second user created successfully")
            return response.json()['user']['id'], response.json()['token']
        else:
            print("❌ Failed to create second user")
            return None, None
    except:
        print("❌ Failed to create second user")
        return None, None

def test_like_post(token, post_id):
    """Test liking a post."""
    print(f"\n❤️ Testing Like Post (ID: {post_id})...")
    
    url = f"{BASE_URL}/posts/{post_id}/like/"
    headers = {"Authorization": f"Token {token}"}
    
    try:
        response = requests.post(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Post liked successfully!")
            print(f"Message: {data['message']}")
            print(f"Likes count: {data['likes_count']}")
        else:
            print("❌ Like post failed!")
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the Django server is running.")

def test_unlike_post(token, post_id):
    """Test unliking a post."""
    print(f"\n💔 Testing Unlike Post (ID: {post_id})...")
    
    url = f"{BASE_URL}/posts/{post_id}/unlike/"
    headers = {"Authorization": f"Token {token}"}
    
    try:
        response = requests.post(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Post unliked successfully!")
            print(f"Message: {data['message']}")
            print(f"Likes count: {data['likes_count']}")
        else:
            print("❌ Unlike post failed!")
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the Django server is running.")

def test_create_post(token):
    """Test creating a post."""
    print("\n📝 Creating a test post...")
    
    url = f"{BASE_URL}/posts/"
    headers = {"Authorization": f"Token {token}"}
    data = {
        "title": "Test Post for Likes",
        "content": "This is a test post to verify likes functionality works correctly."
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            post_data = response.json()
            print("✅ Post created successfully!")
            print(f"Post ID: {post_data['id']}")
            print(f"Title: {post_data['title']}")
            return post_data['id']
        else:
            print("❌ Post creation failed!")
            print(f"Error: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the Django server is running.")
        return None

def test_follow_user(token, user_id):
    """Test following a user."""
    print(f"\n👥 Testing Follow User (ID: {user_id})...")
    
    url = f"{BASE_URL}/accounts/follow/{user_id}/"
    headers = {"Authorization": f"Token {token}"}
    
    try:
        response = requests.post(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ User followed successfully!")
            print(f"Message: {data['message']}")
        else:
            print("❌ Follow user failed!")
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the Django server is running.")

def test_get_notifications(token):
    """Test getting notifications."""
    print("\n🔔 Testing Get Notifications...")
    
    url = f"{BASE_URL}/notifications/"
    headers = {"Authorization": f"Token {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Notifications retrieved successfully!")
            print(f"Total notifications: {len(data['results'])}")
            for notification in data['results'][:3]:  # Show first 3
                print(f"  - {notification['message']} ({notification['created_at']})")
        else:
            print("❌ Get notifications failed!")
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the Django server is running.")

def test_get_unread_count(token):
    """Test getting unread notification count."""
    print("\n🔔 Testing Get Unread Count...")
    
    url = f"{BASE_URL}/notifications/unread_count/"
    headers = {"Authorization": f"Token {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Unread count retrieved successfully!")
            print(f"Unread notifications: {data['unread_count']}")
        else:
            print("❌ Get unread count failed!")
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the Django server is running.")

def test_mark_notifications_read(token):
    """Test marking notifications as read."""
    print("\n✅ Testing Mark Notifications as Read...")
    
    # First get notifications to get IDs
    url = f"{BASE_URL}/notifications/"
    headers = {"Authorization": f"Token {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                # Mark first notification as read
                notification_id = data['results'][0]['id']
                mark_url = f"{BASE_URL}/notifications/mark_as_read/"
                mark_data = {"notification_ids": [notification_id]}
                
                mark_response = requests.post(mark_url, json=mark_data, headers=headers)
                print(f"Mark as read status: {mark_response.status_code}")
                
                if mark_response.status_code == 200:
                    print("✅ Notification marked as read!")
                else:
                    print("❌ Mark as read failed!")
            else:
                print("ℹ️ No notifications to mark as read")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the Django server is running.")

def test_comment_on_post(token, post_id):
    """Test commenting on a post."""
    print(f"\n💬 Testing Comment on Post (ID: {post_id})...")
    
    url = f"{BASE_URL}/comments/"
    headers = {"Authorization": f"Token {token}"}
    data = {
        "post": post_id,
        "content": "This is a test comment to generate notifications."
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            comment_data = response.json()
            print("✅ Comment created successfully!")
            print(f"Comment ID: {comment_data['id']}")
        else:
            print("❌ Comment creation failed!")
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the Django server is running.")

def main():
    """Run all likes and notifications API tests."""
    print("🚀 Likes and Notifications API Test Suite")
    print("=" * 60)
    
    # Get authentication token
    token = get_auth_token()
    if not token:
        print("❌ Cannot proceed without authentication token")
        return
    
    # Create a second user for testing
    user2_id, user2_token = create_second_user()
    if not user2_id:
        print("❌ Cannot proceed without second user")
        return
    
    # Create a post with user1
    post_id = test_create_post(token)
    if not post_id:
        print("❌ Cannot proceed without a post")
        return
    
    # Test like functionality
    test_like_post(user2_token, post_id)  # User2 likes User1's post
    test_like_post(token, post_id)  # User1 likes their own post (should fail)
    
    # Test follow functionality (creates notifications)
    test_follow_user(user2_token, 1)  # User2 follows User1
    
    # Test comment functionality (creates notifications)
    test_comment_on_post(user2_token, post_id)  # User2 comments on User1's post
    
    # Test notification functionality
    test_get_notifications(token)  # User1 checks their notifications
    test_get_unread_count(token)  # User1 checks unread count
    test_mark_notifications_read(token)  # User1 marks notifications as read
    
    # Test unlike functionality
    test_unlike_post(user2_token, post_id)  # User2 unlikes the post
    
    print("\n" + "=" * 60)
    print("✅ Likes and Notifications API test suite completed!")

if __name__ == "__main__":
    main()
