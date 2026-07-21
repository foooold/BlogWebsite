from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone


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
        ordering = ['-published_at', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        if self.status == self.STATUS_PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
