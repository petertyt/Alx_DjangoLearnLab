from django.db import models

class Author(models.Model):
	"""Represents an author who can have many books"""
	name = models.CharField(max_length=255)

	def __str__(self) -> str:
		return self.name


class Book(models.Model):
	"""Represents a book linked to an Author via a ForeignKey"""
	title = models.CharField(max_length=255)
	publication_year = models.IntegerField()
	author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

	def __str__(self) -> str:
		return f"{self.title} ({self.publication_year})"
