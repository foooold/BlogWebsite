from django.utils import timezone
from rest_framework import serializers
from .models import Article, Tag


class TagSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'count']

    def get_count(self, obj):
        return getattr(obj, 'article_count', obj.article_set.filter(status='published').count())


class ArticleListSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    word_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'excerpt', 'tags', 'author_name',
                  'date', 'published_at', 'word_count']

    def get_date(self, obj):
        if obj.published_at:
            return timezone.localtime(obj.published_at).strftime('%Y-%m-%d')
        return ''

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def get_author_name(self, obj):
        if obj.author:
            return obj.author.username
        return ''

    def get_word_count(self, obj):
        return len(obj.content)


class ArticleDetailSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'excerpt', 'content', 'tags',
                  'author_name', 'date', 'published_at']

    def get_date(self, obj):
        if obj.published_at:
            return timezone.localtime(obj.published_at).strftime('%Y-%m-%d')
        return ''

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def get_author_name(self, obj):
        if obj.author:
            return obj.author.username
        return ''
