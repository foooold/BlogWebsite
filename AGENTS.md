# AGENTS.md

## Environment

- **OS**: Windows, shell is PowerShell 5.1
- **Python**: 3.14, venv at `venv/`
- **Node.js**: v24+, installed globally
- **Activate venv**: `& "venv\Scripts\Activate.ps1"` (must run from project root)

## AI Tools

### lazy-changelog + DeepSeek

The project uses [lazy-changelog](https://github.com/nicepkg/lazy-changelog) with DeepSeek (via OpenAI-compatible API) for AI-generated changelogs and commit messages. Requires `OPENAI_API_KEY` in `.env` (set to a DeepSeek API key).

| Script | Purpose |
|--------|---------|
| `npm run log` | Generate changelog (latest tag → HEAD) and prepend to `CHANGELOG.md` |
| `npm run log:diff` | Generate changelog with full code diffs for better context |
| `npm run log:dry` | Dry-run changelog generation (print only, don't write) |
| `npm run commit` | Generate commit message from staged changes, with `-e` (opens editor for review) |
| `npm run commit:msg` | Generate commit message only (no editor), print to stdout |

All scripts use `dotenv-cli` to load `.env` before running, and connect to `https://api.deepseek.com` with model `deepseek-v4-pro`.

**`log:diff` / `log` 默认只覆盖最新 tag → HEAD**。要为特定区间生成 changelog，通过 `--` 传递额外参数：

```bash
# 为 v1.0.0 → v1.1.0 区间生成 changelog（打 tag 后补生成）
npm run log:diff -- --from v1.0.0 --to v1.1.0 --tag v1.1.0

# 为整个项目历史生成 changelog（无 tag 时）
npm run log:diff -- --from $(git rev-list --max-parents=0 HEAD) --tag v1.0.0

# 预览将要生成的内容（不写入文件）
npm run log:dry -- --from v1.0.0 --to v1.1.0
```

**版本号来源**：changelog header 的版本号按以下优先级确定：
1. `--tag <version>` 显式指定
2. `package.json` 中的 `version` 字段
3. `git describe --tags --abbrev=0`（最新 tag）
4. `"Unreleased"`

**发布新版本**：不要手动 `git tag`，使用 `npm version <版本号>`（支持两位版号如 `1.2`），一条命令自动完成：更新 `package.json` → git commit → 打 tag。

```bash
npm version 1.2          # 发布 1.2 版本
npm run log:diff         # 生成 changelog（从最新 tag 到 HEAD）
git push && git push --tags
```

### patch-package

`patch-package` runs on `postinstall` and applies `patches/lazy-changelog+1.3.0.patch`. The patch:
- Changelog prompt: English output, no `[commits]`/`[code]` source prefixes, emoji → plain text
- Commit prompt: English instructions, rule 2 specifies `Make the description in Chinese`
- SDK compatibility: `openai(model)` → `openai.chat(model)`, adds `compatibility: "strict"` for `@ai-sdk/openai` v4+
- Token limits: changelog 8192, commit message 4096

If `npm install` output shows patch failures, the patch may need to be regenerated after upgrading `lazy-changelog`.

## Stack

- **Backend**: Django 6.0.7 + Django REST Framework 3.17.1 + django-cors-headers
- **Database**: SQLite (`db.sqlite3`)
- **Admin**: django-unfold 0.101.0 (must be first in `INSTALLED_APPS`, before `django.contrib.admin`)
- **Frontend**: Vue 3 + Vite 8 + Vue Router 4 + Pinia 4 + Axios (in `frontend/`)
- **Django project**: named `config` (settings at `config/settings.py`, not `website/settings.py`)
- Single Django app: `main`
- **Config**: uses `python-decouple` — most settings (SECRET_KEY, DEBUG, ALLOWED_HOSTS, CORS) come from `.env`

## Architecture

```
frontend (Vite :5173)  ──proxy /api──►  Django (:8000)
       │                                      │
  Vue SPA (dev)                          DRF API (/api/*)
       │                                      │
  build → static/dist/                  Admin (/zh-hans/admin/)
                                                │
                                     SPA fallback (/*) → templates/index.html
```

### URL routing (in order)

| Pattern | Target |
|---------|--------|
| `/api/*` | DRF endpoints (`main/urls.py` → `main/api.py`) |
| `/i18n/*` | Language switching |
| `/zh-hans/admin/`, `/en/admin/` | django-unfold admin |
| `/*` | SPA index (serves Vue app from `templates/index.html`) |

Route priority is critical: API and admin are matched before the SPA catch-all via Django's ordered URL dispatch. **Do not** put the catch-all before API routes.

### API endpoints

| Endpoint | Purpose | File |
|----------|---------|------|
| `GET /api/hello/` | Health check | `main/api.py` |
| `GET /api/articles/` | Published articles (list) | `main/api.py` |
| `GET /api/articles/<slug>/` | Single article (detail) | `main/api.py` |
| `GET /api/tags/` | Tags with article counts | `main/api.py` |
| `GET /api/search/?q=` | Search articles + tags | `main/api.py` |

### `/api/search/` response

```json
{
  "articles": [{ ...ArticleListSerializer, "snippet": "匹配上下文片段" }],
  "tags": [{ ...TagSerializer }]
}
```

- Searches articles by `title`, `content`, `excerpt` (icontains, OR logic)
- Searches tags by `name` (icontains)
- Each article includes a `snippet` field: the first match in content (or excerpt) with asymmetric context — 15 chars before, 40 chars after the match. Falls back to the start of text (or excerpt) if no match is found.
- `snippet` is computed by `_extract_snippet(article, query, prefix_len=15, suffix_len=40)` in `main/api.py`

### Serving modes

- **Development** (`DEBUG=True`): `templates/index.html` loads Vue from Vite dev server (`localhost:5173`), with HMR. Access `http://localhost:5173` directly.
- **Production** (`DEBUG=False`): Django serves built Vue assets from `static/dist/`, reading paths from `.vite/manifest.json`. Access via Nginx on port 80 only (5173 is dev-only).

### Website title

The HTML `<title>` must be kept in sync between two files:

| File | Used by |
|------|---------|
| `templates/index.html` | Django (dev via :8000, production via Nginx) |
| `frontend/index.html` | Vite dev server (:5173 direct access) |

Current title: `Frank Du 的个人空间`. Template changes take effect immediately — no server restart needed.

## Django Backend

### Models

- **Article**: `title`, `slug` (unicode, auto), `excerpt`, `content` (Markdown), `author` (FK→User), `tags` (M2M→Tag), `status` (draft/published), `published_at`, `created_at`, `updated_at`
- **Tag**: `name` (unique), `slug` (unicode)

### Key files

| File | Purpose |
|------|---------|
| `main/models.py` | Article + Tag models |
| `main/admin.py` | django-unfold admin registration. Article/User/Group use `autocomplete_fields` (not `filter_horizontal`). PermissionAdmin registered but hidden. |
| `main/serializers.py` | DRF serializers. Both list and detail include `author_name` (from `obj.author.username`), `date`, `tags`. List has `word_count`, detail has `content`. |
| `main/api.py` | DRF function-based API views + `_extract_snippet()` helper |
| `main/urls.py` | API route registration (`<str:slug>` for Chinese slug support) |
| `main/views.py` | SPA fallback `index()` view with Vite manifest |
| `main/apps.py` | App config (`MainConfig`, `verbose_name = 'MyBlog'`) |
| `config/settings.py` | Django project settings (env-based via `python-decouple`) |

### Critical: Chinese slugs

Slug fields in both Article and Tag use `allow_unicode=True`. API URL must use `<str:slug>` (not `<slug:slug>`) in `main/urls.py`, because Django's built-in slug path converter only matches `[-a-zA-Z0-9_]`.

### Critical: Admin must inherit from unfold

`main/admin.py` must use `unfold.admin.ModelAdmin` (not `django.contrib.admin.ModelAdmin`). Using Django's default `ModelAdmin` causes batch actions (delete, etc.) to not render the "执行" button in unfold's UI. See [unfold#1110](https://github.com/unfoldadmin/django-unfold/issues/1110).

### Critical: Timezone-aware date formatting

`published_at` is stored in UTC. Always use `timezone.localtime()` before formatting dates, otherwise the displayed date may be off by one day for articles published late at night (Shanghai is UTC+8). Both `ArticleListSerializer` and `ArticleDetailSerializer` use `timezone.localtime(obj.published_at)` in `get_date()`.

### Critical: Admin autocomplete for M2M fields

Article, User, and Group admin all use `autocomplete_fields` instead of `filter_horizontal` for many-to-many widgets:

- **ArticleAdmin**: `autocomplete_fields = ['tags']` (was `filter_horizontal`)
- **UserAdmin**: custom `fieldsets` (removed `user_permissions` from the edit form), `autocomplete_fields = ['groups']`, `filter_horizontal = ()` (must be set to empty tuple since `fieldsets` doesn't include any M2M that would need it)
- **GroupAdmin**: `autocomplete_fields = ['permissions']`
- **PermissionAdmin**: registered at `admin.py` level with `search_fields = ['name', 'codename']` to serve autocomplete lookups, but hidden from admin index (`has_module_permission` returns `False`)

This replaces horizontal filter widgets with search-as-you-type select2 widgets, which scale much better with many records.

## Frontend

### Source structure

```
frontend/src/
├── api/index.js          # Axios client: getArticles(), getArticle(slug), getTags(), searchArticles(q)
├── assets/
│   ├── hero.png          # Hero image used in Home.vue
│   └── vite.svg          # Vite boilerplate
├── components/
│   ├── BlogCard.vue      # Card shows author_name, date, read time (from word_count), tags
│   ├── PageHeader.vue
│   ├── Pagination.vue
│   ├── SearchBar.vue     # GitHub-style search bar with dropdown, keyboard nav, match highlighting
│   └── TagBadge.vue
├── composables/
│   └── useMediaQuery.js  # Reactive media query hook (e.g., mobile detection)
├── router/index.js       # 5 routes (see below)
├── stores/app.js         # Pinia store
├── views/
│   ├── Home.vue          # `/` — hero with avatar, latest articles
│   ├── Blog.vue          # `/blog` — multi-select tag chips, pagination, ?tag= query support
│   ├── PostDetail.vue    # `/blog/:slug` — author/date/read-time meta, Markdown rendering, excerpt callout, copy buttons
│   ├── Archive.vue       # `/archive` — fetches all, groups client-side
│   ├── Tags.vue          # Orphan — standalone tag page, NOT registered in router (/tags route was removed)
│   └── About.vue         # `/about` — personal bio, blog creation story, tech stack, contact sidebar with site stats
├── App.vue               # Root layout: full-width navbar (brand left, search+links right with separator)
├── main.js               # Entry point
└── style.css             # Global styles (GitHub-inspired dark theme)
```

Note: `Tags.vue` is an orphan component — the `/tags` route was removed in favor of tag filtering on `/blog`. It is kept for reference but is not imported or routed.

### Blog routes

| Route | Page | Title |
|-------|------|-------|
| `/` | Home | `Frank Du 的个人空间` |
| `/blog` | Blog list | `博客` |
| `/blog/:slug` | Post detail | `{article.title} - Frank Du 的个人空间` (dynamic) |
| `/archive` | Archive | `归档` |
| `/about` | About | `关于 - Frank Du 的个人空间` |

Note: `/tags` route was removed. Tag filtering is done via `/blog` page (tag chips + `?tag=` query param). Search bar tag results navigate to `/blog?tag=xxx`.

### Page titles

Route `meta.title` is set in `router/index.js`, and `router.afterEach()` sets `document.title` on every navigation. For the post detail page, the title is set dynamically in `PostDetail.vue`'s `fetchPost()`: `document.title = post.value.title + ' - Frank Du 的个人空间'` — this overrides the static route meta since the post title isn't known at route definition time.

### Navbar layout

- Full-width (no `max-width` centering), `padding: 0 2rem`
- **Left**: brand logo + "Frank's Blog"
- **Right**: SearchBar `|` 首页 博客 归档 关于 (vertical separator between search and links)
- Sticky, `z-index: 10`, background `#161b22`

### Data flow

All views fetch data from API on mount via `ref([])` + `onMounted(async () => ...)`. Client-side filtering (tag, pagination) works on the fetched array. `BlogCard` computes read time from `post.word_count` and displays `post.author_name` — both available in the list API.

### Blog.vue tag filtering

- Tag cloud (`.tags-cloud`) is always visible.
- **Multi-select**: click any tag to toggle it on/off. `tagFilters` is an array, not a string.
- **AND filtering**: articles must have ALL selected tags (`tagFilters.every(t => p.tags.includes(t))`).
- When tags are active, a `.tagged-header` shows ` tags「A + B」下的文章（N 篇）` with "清除筛选" button.
- Selecting a tag resets pagination to page 1.
- **`?tag=` query param**: `watch(() => route.query.tag)` auto-sets `tagFilters` from URL. Used by search bar tag navigation.

### SearchBar component (`SearchBar.vue`)

- **Appearance**: GitHub-style, search icon left, `/` shortcut hint right, blue border on focus
- **Keyboard**: `/` to focus, `↑↓` to navigate results, `Enter` to go, `Esc` to close
- **Debounce**: 300ms on input before API call
- **Results**: dropdown with "标签" section (tag name + article count) and "文章" section (title + match snippet)
- **Highlight**: matching text wrapped in `<mark class="search-highlight">` (blue: `rgba(88,166,255,0.22)` bg, `#79c0ff` text)
- **Tag click**: navigates to `/blog?tag=xxx`
- **Article click**: navigates to `/blog/:slug`

### PostDetail.vue excerpt

Article detail page shows `post.excerpt` between the meta line (author/date/read time/char count) and the tag cloud, styled as a subtle callout block with left border.

### Home.vue avatar

- Reference: `const avatarUrl = '/static/avatar.png'` (hardcoded URL string, not a Vite asset import)
- Fallback: inline SVG placeholder (gray circle + figure), shown via `@error` handler if image fails to load
- Avatar image: `static/avatar.png` (served by Django at `/static/avatar.png`)

### Critical: Markdown rendering (`PostDetail.vue`)

Uses **`markdown-it`** (v14). Do NOT add `marked` or `marked-highlight` — `markdown-it` is the only renderer.

```js
// frontend/src/views/PostDetail.vue
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'

const md = new MarkdownIt({
  breaks: true,
  linkify: true,
  typographer: true,
  highlight(str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        const highlighted = hljs.highlight(str, { language: lang }).value
        return `<pre class="code-block hljs"><code class="language-${lang}">${highlighted}</code></pre>\n`
      } catch (e) {}
    }
    const highlighted = hljs.highlightAuto(str).value
    return `<pre class="code-block hljs"><code>${highlighted}</code></pre>\n`
  },
})

// REQUIRED: prevents "<str:slug>" from being rendered as an autolink
md.inline.ruler.disable('autolink')

// Custom inline code renderer (.inline-code class for CSS styling)
md.renderer.rules.code_inline = (tokens, idx) => {
  const token = tokens[idx]
  return `<code class="inline-code">${md.utils.escapeHtml(token.content)}</code>`
}
```

Key points:
- `md.inline.ruler.disable('autolink')` is **critical**. Without it, text like `<str:slug>` in articles gets treated as an autolink (`<a href="str:slug">`) instead of literal text. This is NOT related to the `linkify` option.
- `highlight` option integrates highlight.js **during parsing** (no post-render `hljs.highlightAll()` needed).
- `.code-block` and `.inline-code` CSS classes are injected here; CSS selectors in `<style scoped>` depend on them.
- markdown-it defaults to `html: false` — angle-bracket text is escaped, not treated as raw HTML.

## Critical: Dev Server

Running `python manage.py runserver` directly in a timeout-limited shell will kill the process when the timeout fires. Always use `Start-Process` for background persistence:

```powershell
Start-Process -FilePath "venv\Scripts\python.exe" `
  -ArgumentList "manage.py", "runserver", "0.0.0.0:8000" `
  -WorkingDirectory (Get-Location) -WindowStyle Hidden
Start-Sleep 3
```

Same for Vite (uses `cmd.exe /c` because `Start-Process` with npm can fail):

```powershell
Start-Process -FilePath "cmd.exe" -ArgumentList "/c", `
  "cd /d D:\Programing\website\frontend && npm run dev" -WindowStyle Hidden
Start-Sleep 4
```

### Critical: Vite dependency cache must be cleared after npm install

After installing or upgrading npm packages, the Vite dev server's pre-bundling cache (`frontend/node_modules/.vite/`) may be stale. If the browser shows a blank page after `npm install`, clear the cache and restart Vite:

```powershell
Stop-Process -Name "node" -Force                # kill Vite (or find PID via netstat -ano | findstr 5173)
Remove-Item -LiteralPath "frontend\node_modules\.vite" -Recurse -Force
# Then restart Vite with the Start-Process command above
```

## Commands

```powershell
# Root: install AI tools (lazy-changelog, patch-package)
npm install                     # root package.json — installs dotenv-cli, lazy-changelog, patch-package

# Activate venv first, then:
python manage.py migrate
python manage.py startapp <name>
python manage.py collectstatic

# Frontend (from frontend/ dir):
npm install                     # install Vue dependencies
npm run dev                     # Vite dev server (:5173)
npm run build                   # production build → ../static/dist/

# Production deployment:
cd frontend; npm run build; cd ..
python manage.py collectstatic

# Release (root):
npm version 1.2                 # bump version → commit → tag v1.2 (three-in-one)

# AI changelog (root):
npm run log                     # generate changelog → CHANGELOG.md
npm run log:diff                # generate changelog with code diffs
npm run log:dry                 # dry-run (print only)
npm run commit                  # AI-generated commit message
```

## Key Configuration

All settings are read from `.env` via `python-decouple`. See `.env.example` for the template.

| Setting | Default / dev value |
|---------|---------------------|
| `LANGUAGE_CODE` | `zh-hans` |
| `TIME_ZONE` | `Asia/Shanghai` |
| `DEBUG` | env (`DEBUG=True` in dev) |
| `SECRET_KEY` | env (required) |
| `ALLOWED_HOSTS` | env (`*` in dev) |
| `CSRF_TRUSTED_ORIGINS` | env |
| `STATICFILES_DIRS` | `BASE_DIR / 'static'` |
| `STATIC_ROOT` | `BASE_DIR / 'staticfiles'` |
| `CORS_ALLOWED_ORIGINS` | env (`http://localhost:5173,http://127.0.0.1:5173` in dev) |
| `CORS_ALLOW_CREDENTIALS` | `True` |
| `LANGUAGES` | `zh-hans` (简体中文), `en` (English) |
| `UNFOLD.SHOW_LANGUAGES` | `True` |
| `REST_FRAMEWORK.DEFAULT_PERMISSION_CLASSES` | `AllowAny` |

### Logging

Django logging is configured in `config/settings.py` — all output goes to console (stdout/stderr), captured by gunicorn in production to `/var/log/gunicorn/error.log`:

| Logger | Level | Notes |
|--------|-------|-------|
| Root | `WARNING` | Catch-all for third-party libraries |
| `django` | `INFO` | Django framework messages |
| `django.request` | `ERROR` | Request errors only |

Format: `[{asctime}] {levelname} {module} {message}`

## Deployment

The `deploy/` directory contains production deployment configuration for Ubuntu + Nginx + Gunicorn.

| File | Purpose |
|------|---------|
| `deploy/deploy.sh` | One-shot deployment script — sets up venv, runs migrations, collectstatic, restarts services |
| `deploy/gunicorn.conf.py` | Gunicorn config: binds `127.0.0.1:8000`, workers = `cpu * 2 + 1`, logs to `/var/log/gunicorn/` |
| `deploy/nginx.conf` | Nginx reverse proxy — serves static files, proxies `/` to gunicorn |
| `deploy/systemd/gunicorn.service` | systemd unit for gunicorn, runs as `www-data` |

### Deploy script steps

1. Git pull from main
2. Create directories (`/var/log/gunicorn`, `media/`, `logs/`)
3. Set up Python venv (skip if exists)
4. Install pip + frontend npm dependencies
5. Run Django migrations
6. Build frontend, collectstatic, restart nginx
7. Fix permissions (`www-data` owns project dir, `staticfiles/`, `db.sqlite3*`)

### Production access

| Page | URL |
|------|-----|
| Frontend | `http://<server-ip>/` |
| Admin | `http://<server-ip>/zh-hans/admin/` |

## Superuser

- 通过 python manage.py createsuperuser 交互式设置
- Access admin at `/zh-hans/admin/` or `/en/admin/`

## Author / Personal Info

Author details are hardcoded in two files:

- `frontend/src/views/Home.vue` — name, bio, GitHub, email, avatar (img + SVG fallback)
- `frontend/src/views/About.vue` — personal bio, blog creation story (DeepSeek-V4 + Claude Code), tech stack, contact info (email, GitHub, repository link), site stats (article/tag counts, latest update)
- Avatar image: `static/avatar.png` (served at `/static/avatar.png`)

No backend settings for these yet.

## Notes

- `backup/` contains pre-blog rollback snapshot, removed management commands (`import_posts.py`, `_check.py`), and `backup_marked/` / `backup_marked_v2/` snapshots.
- `backup/backup_20260718/`, `backup/backup_20260718_2/`, `backup/backup_20260718_3/`, `backup/backup_20260718_4/` are earlier snapshots (all nested inside `backup/`).
- `backup/backup_20260720/` and `backup/backup_20260721/` contain more recent backup snapshots.
- `backup/backup_1/` and `backup/management/` are additional backup artifacts.
- Use `gettext_lazy` (`_()`) for translatable strings in `UNFOLD` config (e.g., sidebar titles).
- i18n routes (`/zh-hans/admin/`, `/en/admin/`) are auto-prefixed via `i18n_patterns`.
- DRF API views go in `main/api.py` (not `views.py`). Regular Django views go in `main/views.py`.
- `npm install` must be run from `frontend/` before first use.
- Vite build manifest at `static/dist/.vite/manifest.json` — Django template reads this at runtime (production only).
- `frontend/src/style.css` sets `scrollbar-gutter: stable` on `html` to prevent horizontal layout shift when scrollbar appears/disappears.
- **Always run `npm run build` after editing frontend files** to verify compilation. The dev server may not catch errors.
- npm 11+ includes `libc` fields in `package-lock.json` on all platforms (not just Linux). This is normal — no action needed.
