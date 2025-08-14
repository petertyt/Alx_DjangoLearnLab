## CRUD Operations via Django Shell

### Environment

- Run from `Introduction_to_Django/LibraryProject`
- Command: `python manage.py shell`

### 1) Create

```python
from bookshelf.models import Book
b = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(str(b))
# Expected: 1984 by George Orwell (1949)
print(b.id)
# Expected: 1  # (id may vary)
```

### 2) Retrieve

```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)
# Expected: 1984 George Orwell 1949

print(Book.objects.filter(title="1984").values().first())
# Expected (keys/order may vary):
# {"id": 1, "title": "1984", "author": "George Orwell", "publication_year": 1949}
```

### 3) Update

```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

print(Book.objects.get(pk=book.pk).title)
# Expected: Nineteen Eighty-Four
```

### 4) Delete

```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
print(book.delete())
# Expected: (1, {"bookshelf.Book": 1})

print(list(Book.objects.all()))
# Expected: []
```
