from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from .models import Tag, Article


@admin.register(Tag)
class TagAdmin(UnfoldModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    actions = ['delete_selected']


@admin.register(Article)
class ArticleAdmin(UnfoldModelAdmin):
    list_display = ['title', 'status', 'author', 'published_at', 'created_at']
    list_filter = ['status', 'tags', 'published_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    date_hierarchy = 'published_at'
    ordering = ['-published_at', '-created_at']
    actions = ['delete_selected']
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'tags', 'status')
        }),
        ('内容', {
            'fields': ('excerpt', 'content')
        }),
        ('时间', {
            'fields': ('published_at', 'created_at', 'updated_at')
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, UnfoldModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, UnfoldModelAdmin):
    pass
