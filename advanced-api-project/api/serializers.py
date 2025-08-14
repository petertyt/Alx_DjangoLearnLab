from rest_framework import serializers
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
	"""Serializes Book; validates publication_year not in the future."""

	class Meta:
		model = Book
		fields = ['id', 'title', 'publication_year', 'author']

	def validate_publication_year(self, value: int) -> int:
		from datetime import datetime
		current_year = datetime.utcnow().year
		if value > current_year:
			raise serializers.ValidationError("publication_year cannot be in the future")
		return value


class AuthorSerializer(serializers.ModelSerializer):
	"""Serializes Author with nested books using BookSerializer."""
	books = BookSerializer(many=True, read_only=True)

	class Meta:
		model = Author
		fields = ['id', 'name', 'books']


