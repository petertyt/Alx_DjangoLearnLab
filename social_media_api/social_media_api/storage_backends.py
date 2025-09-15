"""
Storage backends for production deployment.
"""

from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    """
    Custom storage class for media files.
    """
    location = 'media'
    file_overwrite = False
