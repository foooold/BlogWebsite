from django.db import models
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Article, Tag
from .serializers import (
    ArticleListSerializer,
    ArticleDetailSerializer,
    TagSerializer,
)


@api_view(['GET'])
def hello(request):
    return Response({
        'message': 'Hello from Django REST API!',
        'status': 'ok',
    })


@api_view(['GET'])
def article_list(request):
    articles = Article.objects.filter(status=Article.STATUS_PUBLISHED)\
        .prefetch_related('tags')\
        .select_related('author')\
        .order_by('-published_at')
    return Response(ArticleListSerializer(articles, many=True).data)


@api_view(['GET'])
def article_detail(request, slug):
    try:
        article = Article.objects.prefetch_related('tags')\
            .select_related('author')\
            .get(slug=slug, status=Article.STATUS_PUBLISHED)
    except Article.DoesNotExist:
        return Response({'error': 'Article not found'}, status=404)
    return Response(ArticleDetailSerializer(article).data)


@api_view(['GET'])
def tag_list(request):
    tags = Tag.objects.annotate(
        article_count=models.Count(
            'article',
            filter=models.Q(article__status=Article.STATUS_PUBLISHED)
        )
    ).filter(article_count__gt=0).order_by('-article_count', 'name')
    return Response(TagSerializer(tags, many=True).data)


@api_view(['GET'])
def search(request):
    q = request.GET.get('q', '').strip()
    if not q:
        return Response({'articles': [], 'tags': []})

    articles = Article.objects.filter(
        status=Article.STATUS_PUBLISHED
    ).filter(
        Q(title__icontains=q) | Q(content__icontains=q) | Q(excerpt__icontains=q)
    ).prefetch_related('tags').select_related('author').order_by('-published_at')[:10]

    tags = Tag.objects.annotate(
        article_count=models.Count(
            'article',
            filter=models.Q(article__status=Article.STATUS_PUBLISHED)
        )
    ).filter(
        article_count__gt=0,
        name__icontains=q,
    ).order_by('-article_count', 'name')[:5]

    article_data = ArticleListSerializer(articles, many=True).data
    for i, article in enumerate(articles):
        article_data[i]['snippet'] = _extract_snippet(article, q)

    return Response({
        'articles': article_data,
        'tags': TagSerializer(tags, many=True).data,
    })


def _extract_snippet(article, query, context=20):
    """Extract a snippet around the first match of query, trying content then excerpt."""
    # Try content first
    text = article.content
    idx = text.lower().find(query.lower())

    # If not in content, try excerpt
    if idx == -1 and article.excerpt:
        text = article.excerpt
        idx = text.lower().find(query.lower())

    # If still no match (matched title only), return excerpt or content start
    if idx == -1:
        if article.excerpt:
            return article.excerpt
        end = min(len(text), context * 2)
        return text[:end] + ('…' if len(text) > end else '')

    start = max(0, idx - context)
    end = min(len(text), idx + len(query) + context)
    prefix = '…' if start > 0 else ''
    suffix = '…' if end < len(text) else ''
    return prefix + text[start:end] + suffix
