#!/bin/bash

# Deployment script for Social Media API
# This script automates the deployment process

set -e

echo "🚀 Starting deployment process..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if .env file exists
if [ ! -f .env ]; then
    print_error ".env file not found. Please copy env.example to .env and configure it."
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

print_status "Environment variables loaded"

# Install dependencies
print_status "Installing dependencies..."
pip install -r requirements_production.txt

# Run database migrations
print_status "Running database migrations..."
python manage.py migrate --settings=social_media_api.settings_production

# Collect static files
print_status "Collecting static files..."
python manage.py collectstatic --noinput --settings=social_media_api.settings_production

# Create logs directory
mkdir -p logs

# Run tests
print_status "Running tests..."
python manage.py test --settings=social_media_api.settings_production

# Create superuser if it doesn't exist
print_status "Checking for superuser..."
python manage.py shell --settings=social_media_api.settings_production << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print("Creating superuser...")
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser created: admin/admin123")
else:
    print("Superuser already exists")
EOF

print_status "Deployment completed successfully! 🎉"

# Display next steps
echo ""
print_status "Next steps:"
echo "1. Start the application with: gunicorn --config gunicorn.conf.py social_media_api.wsgi:application"
echo "2. Configure Nginx with the provided nginx.conf"
echo "3. Set up SSL certificates"
echo "4. Configure your domain DNS"
echo "5. Test the API endpoints"
