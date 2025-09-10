#!/usr/bin/env python3
"""
Simple test script to demonstrate the Social Media API functionality.
Run this script to test user registration, login, and profile management.
"""

import requests
import json

# API base URL
BASE_URL = "http://127.0.0.1:8000/api/accounts"

def test_user_registration():
    """Test user registration endpoint."""
    print("🧪 Testing User Registration...")
    
    url = f"{BASE_URL}/register/"
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "first_name": "Test",
        "last_name": "User",
        "bio": "This is a test user bio"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ Registration successful!")
            print(f"Token: {result['token']}")
            print(f"User: {result['user']['username']}")
            return result['token']
        else:
            print("❌ Registration failed!")
            print(f"Error: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the Django server is running.")
        return None

def test_user_login():
    """Test user login endpoint."""
    print("\n🧪 Testing User Login...")
    
    url = f"{BASE_URL}/login/"
    data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Login successful!")
            print(f"Token: {result['token']}")
            return result['token']
        else:
            print("❌ Login failed!")
            print(f"Error: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the Django server is running.")
        return None

def test_user_profile(token):
    """Test user profile endpoint."""
    print("\n🧪 Testing User Profile...")
    
    url = f"{BASE_URL}/profile/"
    headers = {"Authorization": f"Token {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Profile retrieved successfully!")
            print(f"Username: {result['username']}")
            print(f"Email: {result['email']}")
            print(f"Bio: {result['bio']}")
            print(f"Followers: {result['followers_count']}")
            print(f"Following: {result['following_count']}")
        else:
            print("❌ Profile retrieval failed!")
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the Django server is running.")

def test_update_profile(token):
    """Test profile update endpoint."""
    print("\n🧪 Testing Profile Update...")
    
    url = f"{BASE_URL}/profile/update/"
    headers = {"Authorization": f"Token {token}"}
    data = {
        "bio": "Updated bio - this is a test update!",
        "first_name": "UpdatedTest"
    }
    
    try:
        response = requests.patch(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Profile updated successfully!")
            print(f"Updated Bio: {result['user']['bio']}")
            print(f"Updated First Name: {result['user']['first_name']}")
        else:
            print("❌ Profile update failed!")
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the Django server is running.")

def main():
    """Run all API tests."""
    print("🚀 Social Media API Test Suite")
    print("=" * 40)
    
    # Test registration
    token = test_user_registration()
    
    if token:
        # Test profile retrieval
        test_user_profile(token)
        
        # Test profile update
        test_update_profile(token)
    else:
        # Try login if registration failed (user might already exist)
        token = test_user_login()
        if token:
            test_user_profile(token)
            test_update_profile(token)
    
    print("\n" + "=" * 40)
    print("✅ Test suite completed!")

if __name__ == "__main__":
    main()
