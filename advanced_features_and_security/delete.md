
---

## `delete.md`
```markdown
# Delete the Book and confirm

```python
from bookshelf.models import Book

book = Book.objects.get(title="Nineteen Eighty-Four")
delete_result = book.delete()
delete_result
# Expected output (tuple): (1, {'bookshelf.Book': 1})

list(Book.objects.all())
# Expected output:
# []
