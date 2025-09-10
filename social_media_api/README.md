# Social Media API

A Django REST Framework-based Social Media API with user authentication, profile management, and social features.

## Features

- **User Authentication**: Token-based authentication with registration and login
- **Custom User Model**: Extended user model with bio, profile picture, and followers
- **Profile Management**: Update user profiles with bio and profile pictures
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
├── manage.py
├── requirements.txt
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

## User Model

The custom User model extends Django's AbstractUser with the following additional fields:

- `bio`: TextField for user's bio/description (max 500 characters)
- `profile_picture`: ImageField for user's profile picture
- `followers`: ManyToManyField for users that this user follows
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
