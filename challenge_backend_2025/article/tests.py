from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from user.models import User
from .models import Article
import os

class ArticleAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.article_data = {
            'title': 'Test Article',
            'content': 'This is a test article content.'
        }
        self.article = Article.objects.create(
            title='Existing Article',
            content='This is an existing article.',
            author=self.user
        )
        # 테스트용 이미지 파일 생성 (실제 JPEG 이미지 데이터)
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b',
            content_type='image/jpeg'
        )

    def tearDown(self):
        # 테스트 후 생성된 이미지 파일 정리
        for article in Article.objects.all():
            if article.thumbnail:
                if os.path.isfile(article.thumbnail.path):
                    os.remove(article.thumbnail.path)

    def test_create_article_with_thumbnail(self):
        self.article_data['thumbnail'] = self.test_image
        response = self.client.post('/api/articles/', self.article_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 2)
        article = Article.objects.get(title='Test Article')
        self.assertTrue(article.thumbnail)
        self.assertIn('thumbnail_url', response.data)

    def test_create_article_without_thumbnail(self):
        response = self.client.post('/api/articles/', self.article_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 2)
        article = Article.objects.get(title='Test Article')
        self.assertFalse(article.thumbnail)
        self.assertIsNone(response.data.get('thumbnail_url'))

    def test_update_article_with_thumbnail(self):
        update_data = {
            'title': 'Updated Article',
            'content': 'This is an updated article.',
            'thumbnail': self.test_image
        }
        response = self.client.put(
            f'/api/articles/{self.article.id}/',
            update_data,
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article.refresh_from_db()
        self.assertTrue(self.article.thumbnail)
        self.assertIn('thumbnail_url', response.data)

    def test_update_article_remove_thumbnail(self):
        # 먼저 썸네일 추가
        self.article.thumbnail = self.test_image
        self.article.save()

        # 썸네일 제거 (빈 문자열로 설정)
        update_data = {
            'title': 'Updated Article',
            'content': 'This is an updated article.',
            'thumbnail': ''
        }
        response = self.client.put(
            f'/api/articles/{self.article.id}/',
            update_data,
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article.refresh_from_db()
        self.assertFalse(self.article.thumbnail)
        self.assertIsNone(response.data.get('thumbnail_url'))

    def test_list_articles_with_thumbnails(self):
        # 썸네일이 있는 게시글 생성
        self.article.thumbnail = self.test_image
        self.article.save()

        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertIn('thumbnail_url', response.data['results'][0])

    def test_retrieve_article_with_thumbnail(self):
        # 썸네일이 있는 게시글 생성
        self.article.thumbnail = self.test_image
        self.article.save()

        response = self.client.get(f'/api/articles/{self.article.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Existing Article')
        self.assertIn('thumbnail_url', response.data)

    def test_create_article(self):
        response = self.client.post('/api/articles/', self.article_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 2)
        self.assertEqual(Article.objects.get(title='Test Article').author, self.user)

    def test_list_articles(self):
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_article(self):
        response = self.client.get(f'/api/articles/{self.article.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Existing Article')

    def test_update_article(self):
        update_data = {
            'title': 'Updated Article',
            'content': 'This is an updated article.'
        }
        response = self.client.put(f'/api/articles/{self.article.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Article.objects.get(id=self.article.id).title, 'Updated Article')

    def test_delete_article(self):
        response = self.client.delete(f'/api/articles/{self.article.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Article.objects.count(), 0)
