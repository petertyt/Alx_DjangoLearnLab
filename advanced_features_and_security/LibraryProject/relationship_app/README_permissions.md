# Permissions and Groups Setup

This app defines custom permissions on the `Book` model to support group-based access:

- can_view: Can view books
- can_create: Can create books
- can_edit: Can edit books
- can_delete: Can delete books

## Assigning Permissions to Groups (via Admin)

1. In `/admin/`, create groups:
   - Viewers: assign `relationship_app | book | can view books (can_view)`
   - Editors: assign `can_view`, `can_create`, `can_edit`
   - Admins: assign `can_view`, `can_create`, `can_edit`, `can_delete`
2. Add users to these groups as needed.

## Enforced in Views

- `add_book` requires `permission_required('relationship_app.can_create')`
- `edit_book` requires `permission_required('relationship_app.can_edit')`
- `delete_book` requires `permission_required('relationship_app.can_delete')`

## Testing

- Create test users and assign them to the groups above.
- Log in as each user and attempt to POST to:
  - `/books/add/` (or `/add_book/`) to create
  - `/books/<id>/edit/` (or `/edit_book/<id>/`) to edit
  - `/books/<id>/delete/` to delete
- Confirm access is permitted or denied based on permissions.
