from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from user.models import User
from article.models import Article
from .models import Comment

class CommentAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.article = Article.objects.create(
            title='Test Article',
            content='This is a test article.',
            author=self.user
        )
        self.comment_data = {
            'content': 'Test comment'
        }
        self.comment = Comment.objects.create(
            content='Existing comment',
            article=self.article,
            author=self.user
        )

    def test_create_comment(self):
        response = self.client.post(
            f'/api/articles/{self.article.id}/comments/',
            self.comment_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(Comment.objects.get(content='Test comment').author, self.user)

    def test_list_comments(self):
        response = self.client.get(f'/api/articles/{self.article.id}/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['content'], 'Existing comment')

    def test_update_comment(self):
        update_data = {
            'content': 'Updated comment'
        }
        response = self.client.put(
            f'/api/articles/{self.article.id}/comments/{self.comment.id}/',
            update_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.get(id=self.comment.id).content, 'Updated comment')

    def test_delete_comment(self):
        response = self.client.delete(
            f'/api/articles/{self.article.id}/comments/{self.comment.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)
