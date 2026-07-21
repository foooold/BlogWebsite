import json

from django.conf import settings
from django.shortcuts import render


def index(request):
    context = {'debug': settings.DEBUG}
    manifest_path = settings.BASE_DIR / 'static' / 'dist' / '.vite' / 'manifest.json'
    try:
        manifest = json.loads(manifest_path.read_text())
        entry = manifest.get('index.html', {})
        context['vite_css'] = entry.get('css', [])
        context['vite_js'] = [entry.get('file', '')] if entry.get('file') else []
    except (FileNotFoundError, json.JSONDecodeError):
        context['vite_css'] = []
        context['vite_js'] = []
    return render(request, 'index.html', context)

