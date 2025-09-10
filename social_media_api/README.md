# Social Media API

A Django REST Framework-based Social Media API with user authentication, profile management, and social features.

## Features

- **User Authentication**: Token-based authentication with registration and login
- **Custom User Model**: Extended user model with bio, profile picture, and followers
- **Profile Management**: Update user profiles with bio and profile pictures
- **Posts System**: Create, read, update, and delete posts with like functionality
- **Comments System**: Add comments to posts with like functionality
- **Search & Filtering**: Search posts by title/content and filter by author
- **Pagination**: Efficient handling of large datasets
- **RESTful API**: Clean API endpoints following REST principles

## Project Structure

```
social_media_api/
├── social_media_api/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── posts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── permissions.py
├── manage.py
├── requirements.txt
├── test_api.py
├── test_posts_api.py
└── README.md
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd social_media_api
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser** (optional):
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Authentication

- **POST** `/api/accounts/register/` - Register a new user
- **POST** `/api/accounts/login/` - Login and get authentication token
- **POST** `/api/accounts/logout/` - Logout (delete token)

### User Profile

- **GET** `/api/accounts/profile/` - Get current user's profile
- **PUT/PATCH** `/api/accounts/profile/update/` - Update user profile

### User Follows

- **POST** `/api/accounts/follow/{user_id}/` - Follow a user
- **POST** `/api/accounts/unfollow/{user_id}/` - Unfollow a user
- **GET** `/api/accounts/following/` - Get list of users you're following
- **GET** `/api/accounts/followers/` - Get list of your followers

#### Follow User Example
```bash
curl -X POST http://127.0.0.1:8000/api/accounts/follow/2/ \
  -H "Authorization: Token your_token_here"
```

#### Unfollow User Example
```bash
curl -X POST http://127.0.0.1:8000/api/accounts/unfollow/2/ \
  -H "Authorization: Token your_token_here"
```

#### Get Following List Example
```bash
curl -X GET http://127.0.0.1:8000/api/accounts/following/ \
  -H "Authorization: Token your_token_here"
```

#### Get Followers List Example
```bash
curl -X GET http://127.0.0.1:8000/api/accounts/followers/ \
  -H "Authorization: Token your_token_here"
```

### Posts

- **GET** `/api/posts/` - List all posts (with pagination, search, filtering)
- **POST** `/api/posts/` - Create a new post
- **GET** `/api/posts/{id}/` - Get post details
- **PUT/PATCH** `/api/posts/{id}/` - Update a post
- **DELETE** `/api/posts/{id}/` - Delete a post
- **POST** `/api/posts/{id}/like/` - Like/unlike a post
- **GET** `/api/posts/my_posts/` - Get current user's posts
- **GET** `/api/posts/liked_posts/` - Get posts liked by current user
- **GET** `/api/posts/feed/` - Get feed of posts from followed users (router-based)
- **GET** `/api/feed/` - Get feed of posts from followed users (explicit route)
- **GET** `/api/posts/{id}/retrieve_with_comments/` - Get post with all comments
- **POST** `/api/posts/{id}/like/` - Like a post
- **POST** `/api/posts/{id}/unlike/` - Unlike a post

### Comments

- **GET** `/api/comments/` - List all comments (with pagination, filtering)
- **POST** `/api/comments/` - Create a new comment
- **GET** `/api/comments/{id}/` - Get comment details
- **PUT/PATCH** `/api/comments/{id}/` - Update a comment
- **DELETE** `/api/comments/{id}/` - Delete a comment

### Notifications

- **GET** `/api/notifications/` - List user notifications (with pagination, filtering)
- **GET** `/api/notifications/unread_count/` - Get count of unread notifications
- **POST** `/api/notifications/mark_as_read/` - Mark specific notifications as read
- **POST** `/api/notifications/mark_all_as_read/` - Mark all notifications as read
- **POST** `/api/notifications/{id}/mark_single_as_read/` - Mark single notification as read
- **POST** `/api/comments/{id}/like/` - Like/unlike a comment
- **GET** `/api/comments/my_comments/` - Get current user's comments

## API Usage Examples

### 1. User Registration

```bash
curl -X POST http://127.0.0.1:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Hello, I am John!"
  }'
```

**Response**:
```json
{
  "message": "User registered successfully",
  "token": "your-auth-token-here",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Hello, I am John!",
    "profile_picture": null,
    "followers_count": 0,
    "following_count": 0,
    "created_at": "2023-10-09T17:30:00Z",
    "updated_at": "2023-10-09T17:30:00Z"
  }
}
```

### 2. User Login

```bash
curl -X POST http://127.0.0.1:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepassword123"
  }'
```

### 3. Get User Profile (Authenticated)

```bash
curl -X GET http://127.0.0.1:8000/api/accounts/profile/ \
  -H "Authorization: Token your-auth-token-here"
```

### 4. Update User Profile

```bash
curl -X PATCH http://127.0.0.1:8000/api/accounts/profile/update/ \
  -H "Authorization: Token your-auth-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "bio": "Updated bio text",
    "first_name": "Johnny"
  }'
```

### 5. Create a Post

```bash
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Authorization: Token your-auth-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Post",
    "content": "This is the content of my first post!"
  }'
```

### 6. List Posts with Search

```bash
curl -X GET "http://127.0.0.1:8000/api/posts/?search=first&page=1" \
  -H "Authorization: Token your-auth-token-here"
```

### 7. Like a Post

```bash
curl -X POST http://127.0.0.1:8000/api/posts/1/like/ \
  -H "Authorization: Token your-auth-token-here"
```

### 8. Create a Comment

```bash
curl -X POST http://127.0.0.1:8000/api/comments/ \
  -H "Authorization: Token your-auth-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "post": 1,
    "content": "Great post! Thanks for sharing."
  }'
```

### 9. Get Posts with Comments

```bash
curl -X GET http://127.0.0.1:8000/api/posts/1/retrieve_with_comments/ \
  -H "Authorization: Token your-auth-token-here"
```

### 10. Follow a User

```bash
curl -X POST http://127.0.0.1:8000/api/accounts/follow/2/ \
  -H "Authorization: Token your-auth-token-here"
```

### 11. Get User Feed

```bash
curl -X GET http://127.0.0.1:8000/api/posts/feed/ \
  -H "Authorization: Token your-auth-token-here"
```

### 11b. Get User Feed (Explicit Route)

```bash
curl -X GET http://127.0.0.1:8000/api/feed/ \
  -H "Authorization: Token your-auth-token-here"
```

### 12. Get Following List

```bash
curl -X GET http://127.0.0.1:8000/api/accounts/following/ \
  -H "Authorization: Token your-auth-token-here"
```

### 13. Unfollow a User

```bash
curl -X POST http://127.0.0.1:8000/api/accounts/unfollow/2/ \
  -H "Authorization: Token your-auth-token-here"
```

### 14. Like a Post

```bash
curl -X POST http://127.0.0.1:8000/api/posts/1/like/ \
  -H "Authorization: Token your-auth-token-here"
```

### 15. Unlike a Post

```bash
curl -X POST http://127.0.0.1:8000/api/posts/1/unlike/ \
  -H "Authorization: Token your-auth-token-here"
```

### 16. Get Notifications

```bash
curl -X GET http://127.0.0.1:8000/api/notifications/ \
  -H "Authorization: Token your-auth-token-here"
```

### 17. Get Unread Notification Count

```bash
curl -X GET http://127.0.0.1:8000/api/notifications/unread_count/ \
  -H "Authorization: Token your-auth-token-here"
```

### 18. Mark Notifications as Read

```bash
curl -X POST http://127.0.0.1:8000/api/notifications/mark_as_read/ \
  -H "Authorization: Token your-auth-token-here" \
  -H "Content-Type: application/json" \
  -d '{"notification_ids": [1, 2, 3]}'
```

## User Model

The custom User model extends Django's AbstractUser with the following additional fields:

- `bio`: TextField for user's bio/description (max 500 characters)
- `profile_picture`: ImageField for user's profile picture
- `following`: ManyToManyField for users that this user follows
- `followers`: Related field for users who follow this user (via following field)
- `created_at`: DateTimeField for account creation timestamp
- `updated_at`: DateTimeField for last update timestamp

## Authentication

The API uses Django REST Framework's Token Authentication. Include the token in the Authorization header:

```
Authorization: Token your-auth-token-here
```

## Testing

Run the test suite:

```bash
python manage.py test
```

## Development

### Running Migrations

After making changes to models:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Creating a Superuser

```bash
python manage.py createsuperuser
```

### Django Admin

Access the Django admin interface at `http://127.0.0.1:8000/admin/` to manage users and other data.

## Next Steps

This is the foundation of the Social Media API. Future enhancements could include:

- Post creation and management
- Comments system
- Like/unlike functionality
- Real-time notifications
- Image upload optimization
- API rate limiting
- Advanced search and filtering
- User privacy settings

## License

This project is part of the ALX Django Learning Lab curriculum.

