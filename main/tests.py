import base64
import tempfile
from pathlib import Path

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse
from unfold.widgets import UnfoldAdminTextareaWidget

from .models import Article, ArticleImage


ONE_PIXEL_PNG = base64.b64decode(
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII='
)


class ArticleImageUploadTests(TestCase):
    def setUp(self):
        self.media_dir = tempfile.TemporaryDirectory()
        self.override = override_settings(MEDIA_ROOT=self.media_dir.name)
        self.override.enable()
        self.user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='test-password',
        )
        self.client.force_login(self.user)
        self.url = reverse('admin:main_article_upload_image')

    def tearDown(self):
        self.override.disable()
        self.media_dir.cleanup()

    def test_staff_can_upload_an_image(self):
        image = SimpleUploadedFile('示例图片.png', ONE_PIXEL_PNG, content_type='image/png')

        response = self.client.post(
            self.url,
            {'image': image, 'alt_text': '示例图片'},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload['url'].startswith('/media/article-images/'))
        uploaded = ArticleImage.objects.get(pk=payload['id'])
        self.assertEqual(uploaded.alt_text, '示例图片')
        self.assertEqual(uploaded.original_name, '示例图片.png')
        self.assertEqual(uploaded.uploaded_by, self.user)
        self.assertTrue(Path(uploaded.image.path).exists())

    def test_invalid_file_is_rejected(self):
        invalid = SimpleUploadedFile('not-image.txt', b'not an image', content_type='text/plain')

        response = self.client.post(self.url, {'image': invalid})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(ArticleImage.objects.count(), 0)

    def test_upload_endpoint_only_accepts_post(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)

    def test_article_editor_loads_image_upload_widget(self):
        response = self.client.get(reverse('admin:main_article_add'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-image-upload-url')
        self.assertContains(response, 'main/admin/markdown_image_widget.js')
        self.assertContains(response, 'main/admin/markdown_image_widget.css')

    def test_article_editor_keeps_unfold_textarea(self):
        request = RequestFactory().get(reverse('admin:main_article_add'))
        request.user = self.user
        model_admin = admin.site._registry[Article]
        form = model_admin.get_form(request)
        widget = form.base_fields['content'].widget

        self.assertIsInstance(widget, UnfoldAdminTextareaWidget)
        self.assertIn('vLargeTextField', widget.attrs['class'])
        self.assertEqual(widget.attrs['data-image-upload-url'], self.url)

    def test_article_image_has_standalone_admin_entry(self):
        self.assertIn(ArticleImage, admin.site._registry)

        response = self.client.get(reverse('admin:main_articleimage_changelist'))

        self.assertEqual(response.status_code, 200)

# Create your tests here.
