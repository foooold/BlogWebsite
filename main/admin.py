from pathlib import Path

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group, Permission
from django.http import JsonResponse
from django.urls import path, reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from .models import Tag, Article, ArticleImage


MAX_ARTICLE_IMAGE_SIZE = 10 * 1024 * 1024
ALLOWED_ARTICLE_IMAGE_FORMATS = {'JPEG', 'PNG', 'GIF', 'WEBP'}


class ArticleImageUploadForm(forms.ModelForm):
    class Meta:
        model = ArticleImage
        fields = ['image', 'alt_text']

    def clean_image(self):
        image = self.cleaned_data['image']
        if image.size > MAX_ARTICLE_IMAGE_SIZE:
            raise forms.ValidationError('图片大小不能超过 10 MB。')
        image_format = getattr(getattr(image, 'image', None), 'format', '').upper()
        if image_format not in ALLOWED_ARTICLE_IMAGE_FORMATS:
            raise forms.ValidationError('仅支持 JPG、PNG、GIF 或 WebP 图片。')
        return image


@admin.register(Tag)
class TagAdmin(UnfoldModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    actions = ['delete_selected']


@admin.register(Article)
class ArticleAdmin(UnfoldModelAdmin):
    class Media:
        css = {'all': ('main/admin/markdown_image_widget.css',)}
        js = ('main/admin/markdown_image_widget.js',)

    list_display = ['title', 'is_pinned', 'status', 'author', 'published_at', 'created_at']
    list_filter = ['is_pinned', 'status', 'tags', 'published_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['tags']
    date_hierarchy = 'published_at'
    ordering = ['-published_at', '-created_at']
    actions = ['delete_selected']
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'tags', 'is_pinned', 'status')
        }),
        ('内容', {
            'fields': ('excerpt', 'content')
        }),
        ('时间', {
            'fields': ('published_at', 'created_at', 'updated_at')
        }),
    )
    readonly_fields = ['created_at', 'updated_at']

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'content':
            formfield.widget.attrs.update({
                'data-image-upload-url': reverse('admin:main_article_upload_image'),
                'data-max-image-size': MAX_ARTICLE_IMAGE_SIZE,
            })
        return formfield

    def get_urls(self):
        custom_urls = [
            path(
                'upload-image/',
                self.admin_site.admin_view(self.upload_image),
                name='main_article_upload_image',
            ),
        ]
        return custom_urls + super().get_urls()

    def upload_image(self, request):
        if request.method != 'POST':
            return JsonResponse({'error': '仅支持 POST 请求。'}, status=405)
        if not (self.has_add_permission(request) or self.has_change_permission(request)):
            return JsonResponse({'error': '没有编辑文章的权限。'}, status=403)

        form = ArticleImageUploadForm(request.POST, request.FILES)
        if not form.is_valid():
            error = next(iter(form.errors.values()))[0]
            return JsonResponse({'error': str(error)}, status=400)

        article_image = form.save(commit=False)
        article_image.original_name = Path(request.FILES['image'].name).name
        article_image.uploaded_by = request.user
        article_image.save()
        return JsonResponse({
            'url': article_image.image.url,
            'alt_text': article_image.alt_text,
            'id': article_image.pk,
        })


@admin.register(ArticleImage)
class ArticleImageAdmin(UnfoldModelAdmin):
    form = ArticleImageUploadForm
    list_display = ['thumbnail', 'alt_text', 'original_name', 'uploaded_by', 'created_at']
    search_fields = ['alt_text', 'original_name', 'uploaded_by__username']
    list_filter = ['created_at', 'uploaded_by']
    readonly_fields = ['preview', 'original_name', 'uploaded_by', 'created_at']
    fields = ['image', 'preview', 'alt_text', 'original_name', 'uploaded_by', 'created_at']
    ordering = ['-created_at']
    actions = ['delete_selected']

    @admin.display(description='预览')
    def thumbnail(self, obj):
        if not obj.image:
            return '-'
        return format_html(
            '<img src="{}" alt="" style="width:64px;height:48px;object-fit:cover;border-radius:6px">',
            obj.image.url,
        )

    @admin.display(description='图片预览')
    def preview(self, obj):
        if not obj or not obj.image:
            return '-'
        return format_html(
            '<a href="{}" target="_blank" rel="noopener">'
            '<img src="{}" alt="" style="max-width:600px;max-height:400px;object-fit:contain">'
            '</a>',
            obj.image.url,
            obj.image.url,
        )

    def save_model(self, request, obj, form, change):
        if not change and obj.image:
            obj.original_name = Path(obj.image.name).name
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(Permission)
class PermissionAdmin(UnfoldModelAdmin):
    search_fields = ['name', 'codename']
    ordering = ['content_type__app_label', 'codename']

    def has_module_permission(self, request):
        return False


@admin.register(User)
class UserAdmin(BaseUserAdmin, UnfoldModelAdmin):
    autocomplete_fields = ['groups']
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('first_name', 'last_name', 'email')}),
        ('权限', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
            ),
        }),
        ('重要日期', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, UnfoldModelAdmin):
    autocomplete_fields = ['permissions']
