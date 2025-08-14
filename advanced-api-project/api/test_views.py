from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Author, Book


class BookAPITests(APITestCase):
    def setUp(self) -> None:
        self.client: APIClient = APIClient()
        self.user = User.objects.create_user(username="tester", password="pass1234!")

        self.author_orwell = Author.objects.create(name="George Orwell")
        self.author_huxley = Author.objects.create(name="Aldous Huxley")

        self.book_1984 = Book.objects.create(
            title="1984", publication_year=1949, author=self.author_orwell
        )
        self.book_animal_farm = Book.objects.create(
            title="Animal Farm", publication_year=1945, author=self.author_orwell
        )
        self.book_bnw = Book.objects.create(
            title="Brave New World", publication_year=1932, author=self.author_huxley
        )

    def test_list_books(self):
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 3)

    def test_retrieve_book_detail(self):
        url = reverse("book-detail", kwargs={"pk": self.book_1984.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "1984")
        self.assertEqual(response.data["publication_year"], 1949)

    def test_create_requires_auth_and_succeeds_with_auth(self):
        url = reverse("book-create")
        # Unauthenticated should be forbidden
        response = self.client.post(
            url,
            {"title": "Test", "publication_year": 2000, "author": self.author_orwell.pk},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticated succeeds
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            url,
            {"title": "Homage to Catalonia", "publication_year": 1938, "author": self.author_orwell.pk},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Homage to Catalonia")

    def test_update_book(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("book-update", kwargs={"pk": self.book_1984.pk})
        response = self.client.patch(url, {"title": "Nineteen Eighty-Four"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book_1984.refresh_from_db()
        self.assertEqual(self.book_1984.title, "Nineteen Eighty-Four")

    def test_delete_book(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("book-delete", kwargs={"pk": self.book_bnw.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book_bnw.pk).exists())

    def test_filtering_by_publication_year(self):
        url = reverse("book-list")
        response = self.client.get(url, {"publication_year": 1945})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = {item["title"] for item in response.data}
        self.assertSetEqual(titles, {"Animal Farm"})

    def test_search_by_title(self):
        url = reverse("book-list")
        response = self.client.get(url, {"search": "Brave"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item["title"] for item in response.data]
        self.assertIn("Brave New World", titles)

    def test_ordering_desc_by_title(self):
        url = reverse("book-list")
        response = self.client.get(url, {"ordering": "-title"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item["title"] for item in response.data]
        self.assertEqual(titles, sorted(titles, reverse=True))

    def test_validation_publication_year_not_future(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("book-create")
        next_year = datetime.utcnow().year + 1
        response = self.client.post(
            url,
            {"title": "Future Book", "publication_year": next_year, "author": self.author_orwell.pk},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("publication_year", response.data)


