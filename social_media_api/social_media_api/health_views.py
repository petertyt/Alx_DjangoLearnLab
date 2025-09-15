"""
Health check views for monitoring and load balancers.
"""

from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from django.contrib.auth import get_user_model
import os

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

User = get_user_model()


def health_check(request):
    """
    Basic health check endpoint.
    """
    return JsonResponse({
        'status': 'healthy',
        'service': 'Social Media API',
        'version': '1.0.0'
    })


def detailed_health_check(request):
    """
    Detailed health check with database and cache connectivity.
    """
    health_status = {
        'status': 'healthy',
        'service': 'Social Media API',
        'version': '1.0.0',
        'checks': {}
    }
    
    overall_healthy = True
    
    # Database check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            health_status['checks']['database'] = {
                'status': 'healthy',
                'message': 'Database connection successful'
            }
    except Exception as e:
        health_status['checks']['database'] = {
            'status': 'unhealthy',
            'message': f'Database connection failed: {str(e)}'
        }
        overall_healthy = False
    
    # Cache check
    try:
        cache.set('health_check', 'test', 10)
        cache.get('health_check')
        health_status['checks']['cache'] = {
            'status': 'healthy',
            'message': 'Cache connection successful'
        }
    except Exception as e:
        health_status['checks']['cache'] = {
            'status': 'unhealthy',
            'message': f'Cache connection failed: {str(e)}'
        }
        overall_healthy = False
    
    # Redis check (if Redis is configured)
    try:
        if not REDIS_AVAILABLE:
            health_status['checks']['redis'] = {
                'status': 'not_available',
                'message': 'Redis module not installed'
            }
        else:
            redis_url = os.environ.get('REDIS_URL')
            if redis_url:
                r = redis.from_url(redis_url)
                r.ping()
                health_status['checks']['redis'] = {
                    'status': 'healthy',
                    'message': 'Redis connection successful'
                }
            else:
                health_status['checks']['redis'] = {
                    'status': 'not_configured',
                    'message': 'Redis not configured'
                }
    except Exception as e:
        health_status['checks']['redis'] = {
            'status': 'unhealthy',
            'message': f'Redis connection failed: {str(e)}'
        }
        overall_healthy = False
    
    # User count check
    try:
        user_count = User.objects.count()
        health_status['checks']['users'] = {
            'status': 'healthy',
            'message': f'User table accessible, {user_count} users found'
        }
    except Exception as e:
        health_status['checks']['users'] = {
            'status': 'unhealthy',
            'message': f'User table check failed: {str(e)}'
        }
        overall_healthy = False
    
    if not overall_healthy:
        health_status['status'] = 'unhealthy'
        return JsonResponse(health_status, status=503)
    
    return JsonResponse(health_status)
