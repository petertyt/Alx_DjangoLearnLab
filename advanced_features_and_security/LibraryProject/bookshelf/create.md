# Create a Book

```python
# Open the shell with: python manage.py shell
from bookshelf.models import Book

b = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)
b
# Expected output (repr may vary depending on __str__):
# <Book: 1984 by George Orwell (1949)>

b.id
# Expected output: 1  # (The exact id may vary)
```
