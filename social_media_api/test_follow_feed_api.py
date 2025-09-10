#!/usr/bin/env python3
"""
Test script for the Follow and Feed API functionality.
Run this script to test all follow and feed endpoints.
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
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "first_name": "Test",
        "last_name": "User",
        "bio": "Test user for API testing"
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
        "username": "testuser",
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
    """Create a second user for testing follow functionality."""
    print("\n👤 Creating second user...")
    
    register_url = f"{BASE_URL}/accounts/register/"
    register_data = {
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "first_name": "Test2",
        "last_name": "User2",
        "bio": "Second test user"
    }
    
    try:
        response = requests.post(register_url, json=register_data)
        if response.status_code == 201:
            print("✅ Second user created successfully")
            return response.json()['user']['id']
        else:
            print("❌ Failed to create second user")
            return None
    except:
        print("❌ Failed to create second user")
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
            print(f"Following count: {data['following_count']}")
        else:
            print("❌ Follow user failed!")
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the Django server is running.")

def test_unfollow_user(token, user_id):
    """Test unfollowing a user."""
    print(f"\n👥 Testing Unfollow User (ID: {user_id})...")
    
    url = f"{BASE_URL}/accounts/unfollow/{user_id}/"
    headers = {"Authorization": f"Token {token}"}
    
    try:
        response = requests.post(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ User unfollowed successfully!")
            print(f"Message: {data['message']}")
            print(f"Following count: {data['following_count']}")
        else:
            print("❌ Unfollow user failed!")
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the Django server is running.")

def test_following_list(token):
    """Test getting list of following users."""
    print("\n👥 Testing Following List...")
    
    url = f"{BASE_URL}/accounts/following/"
    headers = {"Authorization": f"Token {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Following list retrieved successfully!")
            print(f"Following {len(data)} users:")
            for user in data:
                print(f"  - {user['username']} ({user['first_name']} {user['last_name']})")
        else:
            print("❌ Following list retrieval failed!")
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the Django server is running.")

def test_followers_list(token):
    """Test getting list of followers."""
    print("\n👥 Testing Followers List...")
    
    url = f"{BASE_URL}/accounts/followers/"
    headers = {"Authorization": f"Token {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Followers list retrieved successfully!")
            print(f"Has {len(data)} followers:")
            for user in data:
                print(f"  - {user['username']} ({user['first_name']} {user['last_name']})")
        else:
            print("❌ Followers list retrieval failed!")
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the Django server is running.")

def test_feed(token):
    """Test getting the user's feed."""
    print("\n📰 Testing User Feed...")
    
    url = f"{BASE_URL}/posts/feed/"
    headers = {"Authorization": f"Token {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Feed retrieved successfully!")
            print(f"Feed contains {len(data['results'])} posts:")
            for post in data['results']:
                print(f"  - {post['title']} by {post['author']}")
        else:
            print("❌ Feed retrieval failed!")
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the Django server is running.")

def create_post_for_feed(token):
    """Create a post to test the feed functionality."""
    print("\n📝 Creating a post for feed testing...")
    
    url = f"{BASE_URL}/posts/"
    headers = {"Authorization": f"Token {token}"}
    data = {
        "title": "Feed Test Post",
        "content": "This is a test post to verify the feed functionality works correctly."
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

def main():
    """Run all follow and feed API tests."""
    print("🚀 Follow and Feed API Test Suite")
    print("=" * 50)
    
    # Get authentication token
    token = get_auth_token()
    if not token:
        print("❌ Cannot proceed without authentication token")
        return
    
    # Create a second user for testing
    user2_id = create_second_user()
    if not user2_id:
        print("❌ Cannot proceed without second user")
        return
    
    # Test follow functionality
    test_follow_user(token, user2_id)
    test_following_list(token)
    test_followers_list(token)
    
    # Create a post to test feed
    post_id = create_post_for_feed(token)
    
    # Test feed functionality
    test_feed(token)
    
    # Test unfollow functionality
    test_unfollow_user(token, user2_id)
    test_following_list(token)
    
    print("\n" + "=" * 50)
    print("✅ Follow and Feed API test suite completed!")

if __name__ == "__main__":
    main()
