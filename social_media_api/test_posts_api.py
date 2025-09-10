#!/usr/bin/env python3
"""
Test script for the Posts and Comments API functionality.
Run this script to test all post and comment endpoints.
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

def test_post_creation(token):
    """Test creating a new post."""
    print("\n📝 Testing Post Creation...")
    
    url = f"{BASE_URL}/posts/"
    headers = {"Authorization": f"Token {token}"}
    data = {
        "title": "My First Post",
        "content": "This is the content of my first post. It's really exciting to be able to share my thoughts!"
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Post created successfully!")
            post_data = response.json()
            print(f"Post ID: {post_data['id']}")
            print(f"Title: {post_data['title']}")
            print(f"Author: {post_data['author']}")
            return post_data['id']
        else:
            print("❌ Post creation failed!")
            print(f"Error: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the Django server is running.")
        return None

def test_post_listing(token):
    """Test listing posts."""
    print("\n📋 Testing Post Listing...")
    
    url = f"{BASE_URL}/posts/"
    headers = {"Authorization": f"Token {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Posts retrieved successfully!")
            print(f"Total posts: {data['count']}")
            print(f"Current page: {data['page']}")
            print(f"Results per page: {len(data['results'])}")
            
            for post in data['results']:
                print(f"  - {post['title']} by {post['author']} ({post['likes_count']} likes)")
        else:
            print("❌ Post listing failed!")
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the Django server is running.")

def test_post_detail(token, post_id):
    """Test retrieving post details."""
    print(f"\n🔍 Testing Post Detail (ID: {post_id})...")
    
    url = f"{BASE_URL}/posts/{post_id}/"
    headers = {"Authorization": f"Token {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            post = response.json()
            print("✅ Post details retrieved successfully!")
            print(f"Title: {post['title']}")
            print(f"Content: {post['content'][:100]}...")
            print(f"Author: {post['author']}")
            print(f"Likes: {post['likes_count']}")
            print(f"Comments: {post['comments_count']}")
        else:
            print("❌ Post detail retrieval failed!")
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the Django server is running.")

def test_post_like(token, post_id):
    """Test liking a post."""
    print(f"\n❤️ Testing Post Like (ID: {post_id})...")
    
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
            print("❌ Post like failed!")
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the Django server is running.")

def test_comment_creation(token, post_id):
    """Test creating a comment on a post."""
    print(f"\n💬 Testing Comment Creation (Post ID: {post_id})...")
    
    url = f"{BASE_URL}/comments/"
    headers = {"Authorization": f"Token {token}"}
    data = {
        "post": post_id,
        "content": "This is a great post! Thanks for sharing your thoughts."
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Comment created successfully!")
            comment_data = response.json()
            print(f"Comment ID: {comment_data['id']}")
            print(f"Content: {comment_data['content']}")
            print(f"Author: {comment_data['author']}")
            return comment_data['id']
        else:
            print("❌ Comment creation failed!")
            print(f"Error: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the Django server is running.")
        return None

def test_comment_listing(token):
    """Test listing comments."""
    print("\n📝 Testing Comment Listing...")
    
    url = f"{BASE_URL}/comments/"
    headers = {"Authorization": f"Token {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Comments retrieved successfully!")
            print(f"Total comments: {data['count']}")
            print(f"Current page: {data['page']}")
            print(f"Results per page: {len(data['results'])}")
            
            for comment in data['results']:
                print(f"  - {comment['content'][:50]}... by {comment['author']}")
        else:
            print("❌ Comment listing failed!")
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the Django server is running.")

def test_comment_like(token, comment_id):
    """Test liking a comment."""
    print(f"\n❤️ Testing Comment Like (ID: {comment_id})...")
    
    url = f"{BASE_URL}/comments/{comment_id}/like/"
    headers = {"Authorization": f"Token {token}"}
    
    try:
        response = requests.post(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Comment liked successfully!")
            print(f"Message: {data['message']}")
            print(f"Likes count: {data['likes_count']}")
        else:
            print("❌ Comment like failed!")
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the Django server is running.")

def test_post_update(token, post_id):
    """Test updating a post."""
    print(f"\n✏️ Testing Post Update (ID: {post_id})...")
    
    url = f"{BASE_URL}/posts/{post_id}/"
    headers = {"Authorization": f"Token {token}"}
    data = {
        "title": "Updated Post Title",
        "content": "This is the updated content of my post. I've made some changes!"
    }
    
    try:
        response = requests.patch(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Post updated successfully!")
            post_data = response.json()
            print(f"Updated Title: {post_data['title']}")
            print(f"Updated Content: {post_data['content'][:100]}...")
        else:
            print("❌ Post update failed!")
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the Django server is running.")

def test_search_posts(token):
    """Test searching posts."""
    print("\n🔍 Testing Post Search...")
    
    url = f"{BASE_URL}/posts/?search=first"
    headers = {"Authorization": f"Token {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Post search completed!")
            print(f"Found {data['count']} posts matching 'first'")
            for post in data['results']:
                print(f"  - {post['title']} by {post['author']}")
        else:
            print("❌ Post search failed!")
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the Django server is running.")

def main():
    """Run all posts API tests."""
    print("🚀 Posts and Comments API Test Suite")
    print("=" * 50)
    
    # Get authentication token
    token = get_auth_token()
    if not token:
        print("❌ Cannot proceed without authentication token")
        return
    
    # Test post operations
    post_id = test_post_creation(token)
    if post_id:
        test_post_detail(token, post_id)
        test_post_like(token, post_id)
        test_post_update(token, post_id)
    
    # Test comment operations
    comment_id = test_comment_creation(token, post_id) if post_id else None
    if comment_id:
        test_comment_like(token, comment_id)
    
    # Test listing and search
    test_post_listing(token)
    test_comment_listing(token)
    test_search_posts(token)
    
    print("\n" + "=" * 50)
    print("✅ Posts and Comments API test suite completed!")

if __name__ == "__main__":
    main()
