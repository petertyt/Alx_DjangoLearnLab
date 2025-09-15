# Social Media API - Production Deployment Guide

This guide provides comprehensive instructions for deploying the Social Media API to production.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Database Setup](#database-setup)
4. [Deployment Options](#deployment-options)
5. [Configuration](#configuration)
6. [Security](#security)
7. [Monitoring](#monitoring)
8. [Maintenance](#maintenance)
9. [Troubleshooting](#troubleshooting)

## Prerequisites

- Python 3.11+
- PostgreSQL 12+
- Redis (optional, for caching)
- Nginx (for reverse proxy)
- SSL Certificate
- Domain name

## Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/social_media_api
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements_production.txt
```

### 4. Environment Variables

Copy the environment template and configure:

```bash
cp env.example .env
```

Edit `.env` with your production values:

```env
SECRET_KEY=your-super-secret-production-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=social_media_api
DB_USER=your_db_user
DB_PASSWORD=your_secure_password
DB_HOST=your_db_host
DB_PORT=5432
```

## Database Setup

### PostgreSQL Configuration

1. Install PostgreSQL:

```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# CentOS/RHEL
sudo yum install postgresql-server postgresql-contrib
```

2. Create database and user:

```sql
sudo -u postgres psql
CREATE DATABASE social_media_api;
CREATE USER your_db_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE social_media_api TO your_db_user;
\q
```

3. Run migrations:

```bash
python manage.py migrate --settings=social_media_api.settings_production
```

## Deployment Options

### Option 1: Traditional VPS Deployment

#### 1. Server Setup (Ubuntu 20.04+)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install python3.11 python3.11-venv python3-pip postgresql postgresql-contrib nginx redis-server -y
```

#### 2. Application Deployment

```bash
# Run deployment script
chmod +x deploy.sh
./deploy.sh
```

#### 3. Gunicorn Service

Create systemd service file:

```bash
sudo nano /etc/systemd/system/social-media-api.service
```

```ini
[Unit]
Description=Social Media API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/social_media_api
Environment="PATH=/path/to/social_media_api/venv/bin"
ExecStart=/path/to/social_media_api/venv/bin/gunicorn --config gunicorn.conf.py social_media_api.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable social-media-api
sudo systemctl start social-media-api
```

#### 4. Nginx Configuration

```bash
# Copy nginx config
sudo cp nginx.conf /etc/nginx/sites-available/social-media-api
sudo ln -s /etc/nginx/sites-available/social-media-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Option 2: Docker Deployment

#### 1. Build and Run

```bash
# Build the image
docker build -t social-media-api .

# Run with docker-compose
docker-compose up -d
```

#### 2. Production Docker Compose

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    networks:
      - app-network

  web:
    build: .
    command: gunicorn --config gunicorn.conf.py social_media_api.wsgi:application
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - SECRET_KEY=${SECRET_KEY}
      - DB_NAME=${DB_NAME}
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_HOST=db
      - DB_PORT=5432
      - REDIS_URL=redis://redis:6379/1
    depends_on:
      - db
      - redis
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

### Option 3: Heroku Deployment

#### 1. Install Heroku CLI

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh
```

#### 2. Login and Create App

```bash
heroku login
heroku create your-app-name
```

#### 3. Configure Environment Variables

```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
```

#### 4. Add Database

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

#### 5. Deploy

```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### Option 4: AWS Elastic Beanstalk

#### 1. Install EB CLI

```bash
pip install awsebcli
```

#### 2. Initialize EB

```bash
eb init
eb create production
```

#### 3. Configure Environment Variables

```bash
eb setenv SECRET_KEY=your-secret-key DEBUG=False
```

#### 4. Deploy

```bash
eb deploy
```

## Configuration

### Static Files

For production, configure static file serving:

```bash
python manage.py collectstatic --settings=social_media_api.settings_production
```

### Media Files

For production, consider using AWS S3:

1. Set up S3 bucket
2. Configure AWS credentials in environment variables
3. Set `USE_S3=True` in environment variables

### SSL Certificate

#### Let's Encrypt (Free)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

#### Custom Certificate

Update nginx configuration with your certificate paths.

## Security

### 1. Firewall Configuration

```bash
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### 2. Database Security

- Use strong passwords
- Limit database access to application server only
- Regular security updates

### 3. Application Security

- Keep dependencies updated
- Use environment variables for secrets
- Enable HTTPS
- Configure security headers
- Regular backups

## Monitoring

### 1. Health Checks

The API includes health check endpoints:

- Basic: `GET /health/`
- Detailed: `GET /health/detailed/`

### 2. Logging

Logs are configured to write to:
- Console output
- File: `logs/django.log`

### 3. Monitoring Tools

Consider integrating:
- Sentry for error tracking
- New Relic for performance monitoring
- Prometheus + Grafana for metrics

## Maintenance

### 1. Regular Updates

```bash
# Update dependencies
pip install -r requirements_production.txt --upgrade

# Update system packages
sudo apt update && sudo apt upgrade
```

### 2. Database Maintenance

```bash
# Create backups
pg_dump social_media_api > backup_$(date +%Y%m%d).sql

# Run migrations
python manage.py migrate --settings=social_media_api.settings_production
```

### 3. Log Rotation

Configure logrotate for Django logs:

```bash
sudo nano /etc/logrotate.d/social-media-api
```

```
/path/to/social_media_api/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload social-media-api
    endscript
}
```

## Troubleshooting

### Common Issues

#### 1. Database Connection Errors

- Check database credentials
- Verify database server is running
- Check network connectivity

#### 2. Static Files Not Loading

```bash
python manage.py collectstatic --settings=social_media_api.settings_production
sudo chown -R www-data:www-data staticfiles/
```

#### 3. Permission Errors

```bash
sudo chown -R www-data:www-data /path/to/social_media_api
sudo chmod -R 755 /path/to/social_media_api
```

#### 4. SSL Certificate Issues

- Verify certificate files exist
- Check certificate expiration
- Ensure nginx configuration is correct

### Debugging

#### 1. Check Service Status

```bash
sudo systemctl status social-media-api
sudo systemctl status nginx
```

#### 2. View Logs

```bash
# Application logs
sudo journalctl -u social-media-api -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Django logs
tail -f logs/django.log
```

#### 3. Test Connectivity

```bash
# Test database
python manage.py dbshell --settings=social_media_api.settings_production

# Test Redis
redis-cli ping

# Test API endpoints
curl http://localhost:8000/health/
```

## Performance Optimization

### 1. Database Optimization

- Add database indexes
- Use connection pooling
- Optimize queries

### 2. Caching

- Enable Redis caching
- Use database query caching
- Implement API response caching

### 3. Load Balancing

- Use multiple application servers
- Configure load balancer
- Implement horizontal scaling

## Backup Strategy

### 1. Database Backups

```bash
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump social_media_api > /backups/db_backup_$DATE.sql
find /backups -name "db_backup_*.sql" -mtime +7 -delete
```

### 2. Media Files Backup

```bash
# Backup media files
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/
```

### 3. Configuration Backup

Keep backups of:
- Environment variables
- Nginx configuration
- SSL certificates
- Database credentials

## Scaling Considerations

### 1. Horizontal Scaling

- Use load balancer
- Multiple application servers
- Database replication
- Redis cluster

### 2. Vertical Scaling

- Increase server resources
- Optimize application code
- Database optimization

### 3. Microservices

Consider breaking down into:
- Authentication service
- Posts service
- Notifications service
- User management service

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review application logs
3. Check system resources
4. Consult Django documentation
5. Contact system administrator

---

**Note**: This deployment guide is comprehensive but should be adapted based on your specific infrastructure and requirements. Always test deployments in a staging environment before production deployment.
