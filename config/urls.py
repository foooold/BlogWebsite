from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path, re_path
from main.views import index

urlpatterns = [
    path('api/', include('main.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path(settings.ADMIN_PATH, lambda req: redirect(f'/zh-hans/{settings.ADMIN_PATH}')),
]

urlpatterns += i18n_patterns(
    path(settings.ADMIN_PATH, admin.site.urls),
)

urlpatterns += [
    re_path(r'^.*$', index, name='index'),
]
