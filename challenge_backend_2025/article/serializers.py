from rest_framework import serializers
from .models import Article
from user.serializers import UserSerializer

class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'thumbnail', 'thumbnail_url', 'author', 'created_at', 'updated_at')
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')
        extra_kwargs = {
            'thumbnail': {'required': False}
        }

    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            return self.context['request'].build_absolute_uri(obj.thumbnail.url)
        return None

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'thumbnail' in validated_data:
            if validated_data['thumbnail'] == '':
                if instance.thumbnail:
                    instance.thumbnail.delete(save=False)
                validated_data['thumbnail'] = None
        return super().update(instance, validated_data)

class ArticleListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comment_count = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'title', 'author', 'created_at', 'comment_count', 'thumbnail_url')

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            return self.context['request'].build_absolute_uri(obj.thumbnail.url)
        return None 