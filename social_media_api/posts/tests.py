from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.authtoken.models import Token
from .models import Post, Comment

User = get_user_model()


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='This is a test post content'
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.content, 'This is a test post content')
        self.assertEqual(self.post.likes_count, 0)
        self.assertEqual(self.post.comments_count, 0)

    def test_post_likes(self):
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        self.post.likes.add(user2)
        self.assertEqual(self.post.likes_count, 1)

    def test_post_str(self):
        expected = f"{self.post.title} by {self.post.author.username}"
        self.assertEqual(str(self.post), expected)


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='This is a test post content'
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='This is a test comment'
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.content, 'This is a test comment')
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.likes_count, 0)

    def test_comment_str(self):
        expected = f"Comment by {self.comment.author.username} on {self.comment.post.title}"
        self.assertEqual(str(self.comment), expected)


class PostAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_post(self):
        url = reverse('post-list')
        data = {
            'title': 'New Post',
            'content': 'This is a new post content'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'New Post')

    def test_list_posts(self):
        Post.objects.create(
            author=self.user,
            title='Post 1',
            content='Content 1'
        )
        Post.objects.create(
            author=self.user,
            title='Post 2',
            content='Content 2'
        )
        
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_post(self):
        post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='Test content'
        )
        url = reverse('post-detail', kwargs={'pk': post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Post')

    def test_update_post(self):
        post = Post.objects.create(
            author=self.user,
            title='Original Title',
            content='Original content'
        )
        url = reverse('post-detail', kwargs={'pk': post.pk})
        data = {'title': 'Updated Title', 'content': 'Updated content'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, 'Updated Title')

    def test_delete_post(self):
        post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='Test content'
        )
        url = reverse('post-detail', kwargs={'pk': post.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_like_post(self):
        post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='Test content'
        )
        url = reverse('post-like', kwargs={'pk': post.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post.likes_count, 1)

    def test_my_posts(self):
        Post.objects.create(
            author=self.user,
            title='My Post',
            content='My content'
        )
        url = reverse('post-my-posts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class CommentAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='Test content'
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_comment(self):
        url = reverse('comment-list')
        data = {
            'post': self.post.id,
            'content': 'This is a test comment'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)

    def test_list_comments(self):
        Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Comment 1'
        )
        Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Comment 2'
        )
        
        url = reverse('comment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_comment(self):
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test comment'
        )
        url = reverse('comment-detail', kwargs={'pk': comment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Test comment')

    def test_update_comment(self):
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Original comment'
        )
        url = reverse('comment-detail', kwargs={'pk': comment.pk})
        data = {'content': 'Updated comment'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Updated comment')

    def test_delete_comment(self):
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test comment'
        )
        url = reverse('comment-detail', kwargs={'pk': comment.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    def test_like_comment(self):
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test comment'
        )
        url = reverse('comment-like', kwargs={'pk': comment.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(comment.likes_count, 1)


class PermissionTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
        
        self.post = Post.objects.create(
            author=self.user1,
            title='User1 Post',
            content='User1 content'
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user1,
            content='User1 comment'
        )

    def test_cannot_edit_others_post(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        data = {'title': 'Hacked Title'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_edit_others_comment(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        url = reverse('comment-detail', kwargs={'pk': self.comment.pk})
        data = {'content': 'Hacked comment'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_edit_own_post(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        data = {'title': 'Updated Title'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_edit_own_comment(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        url = reverse('comment-detail', kwargs={'pk': self.comment.pk})
        data = {'content': 'Updated comment'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)