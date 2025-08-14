from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
	"""Read-only list of all books. Accessible to anyone."""
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.AllowAny]


class BookDetailView(generics.RetrieveAPIView):
	"""Read-only detail view for a single book by id. Accessible to anyone."""
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
	"""Create a new book. Requires authentication."""
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
	"""Update an existing book. Requires authentication."""
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
	"""Delete a book. Requires authentication."""
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.IsAuthenticated]
