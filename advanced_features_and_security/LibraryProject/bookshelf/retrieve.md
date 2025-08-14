# Retrieve the created Book

```python
from bookshelf.models import Book

book = Book.objects.get(title="1984")
book.title, book.author, book.publication_year
# Expected output:
# ('1984', 'George Orwell', 1949)

# Optionally view as a dict:
Book.objects.filter(title="1984").values().first()
# Expected output (keys/order may vary):
# {'id': 1, 'title': '1984', 'author': 'George Orwell', 'publication_year': 1949}
```
