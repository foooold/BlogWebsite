import uuid
from pathlib import Path

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone


def article_image_upload_to(instance, filename):
    """Store article images under a date-based path with collision-free names."""
    extension = Path(filename).suffix.lower()
    return f'article-images/{timezone.now():%Y/%m}/{uuid.uuid4().hex}{extension}'


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='名称')
    slug = models.SlugField(max_length=60, unique=True, allow_unicode=True, verbose_name='Slug')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'
    STATUS_CHOICES = [
        (STATUS_DRAFT, '草稿'),
        (STATUS_PUBLISHED, '已发布'),
    ]

    title = models.CharField(max_length=200, verbose_name='标题')
    slug = models.SlugField(max_length=250, unique=True, allow_unicode=True, verbose_name='Slug')
    excerpt = models.TextField(max_length=500, blank=True, verbose_name='摘要')
    content = models.TextField(verbose_name='正文')
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='作者'
    )
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')
    is_pinned = models.BooleanField(default=False, verbose_name='置顶')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT,
        verbose_name='状态'
    )
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='发布时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-is_pinned', '-published_at', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        if self.status == self.STATUS_PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ArticleImage(models.Model):
    image = models.ImageField(upload_to=article_image_upload_to, verbose_name='图片')
    alt_text = models.CharField(max_length=200, blank=True, verbose_name='替代文字')
    original_name = models.CharField(max_length=255, blank=True, verbose_name='原始文件名')
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='上传者',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')

    class Meta:
        verbose_name = '文章图片'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.alt_text or self.original_name or self.image.name
