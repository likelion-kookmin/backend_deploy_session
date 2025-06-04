from django.db import models
from user.models import User

def article_thumbnail_path(instance, filename):
    # 파일명을 article_id와 timestamp로 구성
    return f'thumbnails/article_{instance.id}_{filename}'

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    thumbnail = models.ImageField(upload_to=article_thumbnail_path, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'articles'
        verbose_name = '게시글'
        verbose_name_plural = '게시글들'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
