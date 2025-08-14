from relationship_app.models import Author, Book, Library, Librarian


def books_by_author(author_name: str):
    author = Author.objects.get(name=author_name)
    return list(Book.objects.filter(author=author))


def books_in_library(library_name: str):
    library = Library.objects.get(name=library_name)
    return list(Book.objects.filter(libraries=library))


def librarian_for_library(library_name: str):
    library = Library.objects.get(name=library_name)
    return Librarian.objects.get(library=library)


__all__ = [
    "books_by_author",
    "books_in_library",
    "librarian_for_library",
]

