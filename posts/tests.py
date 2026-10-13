import io
from PIL import Image
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from posts.models import Post


def create_test_image():
    """Helper function to create an in-memory test image."""
    file = io.BytesIO()
    image = Image.new('RGB', (100, 100), color='blue')
    image.save(file, 'PNG')
    file.seek(0)
    return SimpleUploadedFile('test_photo.png', file.getvalue(), content_type='image/png')


class PostCRUDTests(TestCase):
    """
    Test suite for Post creation, retrieval, updates, deletions, and security authorization.
    """

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='password123'
        )

        self.feed_url = reverse('feed')
        self.post_create_url = reverse('post_create')

        # Create a sample post for user1
        self.post1 = Post.objects.create(
            user=self.user1,
            content="Hello from User 1!"
        )

    def test_feed_requires_login(self):
        """Unauthenticated user accessing feed should redirect to login."""
        response = self.client.get(self.feed_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(reverse('login') in response.url)

    def test_feed_shows_posts(self):
        """Authenticated user can view feed with posts from multiple users."""
        Post.objects.create(user=self.user2, content="Post from User 2")

        self.client.login(username='user1', password='password123')
        response = self.client.get(self.feed_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello from User 1!")
        self.assertContains(response, "Post from User 2")

    def test_create_text_only_post(self):
        """Test creating a post with text only."""
        self.client.login(username='user1', password='password123')
        response = self.client.post(self.post_create_url, {
            'content': 'This is a text-only test post.'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(content='This is a text-only test post.').exists())

    def test_create_image_only_post(self):
        """Test creating a post with only an image."""
        self.client.login(username='user1', password='password123')
        img = create_test_image()
        response = self.client.post(self.post_create_url, {
            'content': '',
            'image': img
        })
        self.assertEqual(response.status_code, 302)
        created_post = Post.objects.filter(user=self.user1, content='').first()
        self.assertIsNotNone(created_post)
        self.assertTrue(bool(created_post.image))

    def test_create_text_and_image_post(self):
        """Test creating a post with both text and an image."""
        self.client.login(username='user1', password='password123')
        img = create_test_image()
        response = self.client.post(self.post_create_url, {
            'content': 'Text with image post.',
            'image': img
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(content='Text with image post.').exists())

    def test_create_empty_post_validation(self):
        """Test that submitting an empty post fails validation."""
        self.client.login(username='user1', password='password123')
        response = self.client.post(self.post_create_url, {
            'content': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Post.objects.filter(content='', image='').exists())

    def test_post_detail_view(self):
        """Test viewing an individual post."""
        detail_url = reverse('post_detail', kwargs={'pk': self.post1.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post1.content)

    def test_owner_can_edit_post(self):
        """Test that the owner of a post can edit its content."""
        self.client.login(username='user1', password='password123')
        edit_url = reverse('post_edit', kwargs={'pk': self.post1.pk})
        response = self.client.post(edit_url, {
            'content': 'Updated content by owner!'
        })
        self.assertEqual(response.status_code, 302)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.content, 'Updated content by owner!')

    def test_non_owner_cannot_edit_post(self):
        """Test that a user cannot edit someone else's post."""
        self.client.login(username='user2', password='password123')
        edit_url = reverse('post_edit', kwargs={'pk': self.post1.pk})
        response = self.client.post(edit_url, {
            'content': 'Malicious update attempt'
        })
        # Should return 403 Forbidden
        self.assertEqual(response.status_code, 403)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.content, "Hello from User 1!")

    def test_owner_can_delete_post(self):
        """Test that the owner of a post can delete it."""
        self.client.login(username='user1', password='password123')
        delete_url = reverse('post_delete', kwargs={'pk': self.post1.pk})
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post1.pk).exists())

    def test_non_owner_cannot_delete_post(self):
        """Test that a user cannot delete someone else's post."""
        self.client.login(username='user2', password='password123')
        delete_url = reverse('post_delete', kwargs={'pk': self.post1.pk})
        response = self.client.post(delete_url)
        # Should return 403 Forbidden
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Post.objects.filter(pk=self.post1.pk).exists())
