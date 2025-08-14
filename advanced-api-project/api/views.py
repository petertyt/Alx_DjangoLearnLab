from rest_framework import generics, permissions, filters
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer



class BookListView(generics.ListAPIView):
	"""Read-only list of all books. Accessible to anyone."""
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]
	# Enable filtering, searching, and ordering via DRF backends
	filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
	filterset_fields = ['title', 'author', 'publication_year']
	search_fields = ['title', 'author__name']
	ordering_fields = ['title', 'publication_year', 'id']



class BookDetailView(generics.RetrieveAPIView):
	"""Read-only detail view for a single book by id. Accessible to anyone."""
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]



class BookCreateView(generics.CreateAPIView):
	"""Create a new book. Requires authentication."""
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticated]



class BookUpdateView(generics.UpdateAPIView):
	"""Update an existing book. Requires authentication."""
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticated]



class BookDeleteView(generics.DestroyAPIView):
	"""Delete a book. Requires authentication."""
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticated]
