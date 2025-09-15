#!/bin/bash

# Heroku deployment script for Social Media API

set -e

echo "🚀 Deploying to Heroku..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    print_error "Heroku CLI is not installed. Please install it first."
    exit 1
fi

# Check if user is logged in
if ! heroku auth:whoami &> /dev/null; then
    print_error "Not logged in to Heroku. Please run 'heroku login' first."
    exit 1
fi

# Get app name from user or use default
APP_NAME=${1:-"social-media-api-$(date +%s)"}

print_status "Using app name: $APP_NAME"

# Create Heroku app if it doesn't exist
if ! heroku apps:info $APP_NAME &> /dev/null; then
    print_status "Creating Heroku app: $APP_NAME"
    heroku create $APP_NAME
else
    print_status "Using existing app: $APP_NAME"
fi

# Add PostgreSQL addon
print_status "Adding PostgreSQL database..."
heroku addons:create heroku-postgresql:hobby-dev --app $APP_NAME

# Set environment variables
print_status "Setting environment variables..."
heroku config:set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())') --app $APP_NAME
heroku config:set DEBUG=False --app $APP_NAME
heroku config:set ALLOWED_HOSTS=$APP_NAME.herokuapp.com --app $APP_NAME

# Set buildpacks
print_status "Setting buildpacks..."
heroku buildpacks:set heroku/python --app $APP_NAME

# Add Redis addon (optional)
read -p "Add Redis addon for caching? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Adding Redis addon..."
    heroku addons:create heroku-redis:hobby-dev --app $APP_NAME
fi

# Deploy to Heroku
print_status "Deploying to Heroku..."
git add .
git commit -m "Deploy to Heroku" || true
git push heroku main

# Run migrations
print_status "Running database migrations..."
heroku run python manage.py migrate --settings=social_media_api.settings_production --app $APP_NAME

# Create superuser
print_status "Creating superuser..."
heroku run python manage.py shell --settings=social_media_api.settings_production --app $APP_NAME << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser created: admin/admin123")
else:
    print("Superuser already exists")
EOF

# Open the app
print_status "Opening the deployed app..."
heroku open --app $APP_NAME

print_status "🎉 Deployment completed successfully!"
echo ""
print_status "App URL: https://$APP_NAME.herokuapp.com"
print_status "Admin URL: https://$APP_NAME.herokuapp.com/admin"
print_status "API URL: https://$APP_NAME.herokuapp.com/api/"
print_status "Health Check: https://$APP_NAME.herokuapp.com/health/"
echo ""
print_warning "Remember to:"
echo "1. Change the default admin password"
echo "2. Configure your domain name"
echo "3. Set up SSL certificates"
echo "4. Configure environment variables for production"
echo "5. Set up monitoring and logging"
