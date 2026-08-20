<div align="center">

# BlogWebsite

基于 Django + Vue 3 的个人博客网站，支持 Markdown 写作、标签筛选、全文搜索、文章归档、明暗主题和响应式布局。

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white">
  <img alt="Node.js" src="https://img.shields.io/badge/Node.js-%5E20.19.0%20%7C%20%3E%3D22.12.0-green?logo=nodedotjs&logoColor=white">
  <a href="#许可证"><img alt="GitHub License" src="https://img.shields.io/github/license/foooold/BlogWebsite"></a>
</p>

</div>

## 目录

- [功能特性](#功能特性)
- [技术栈](#技术栈)
- [快速开始](#快速开始)
- [项目配置](#项目配置)
- [项目结构](#项目结构)
- [接口参考](#接口参考)
- [生产部署](#生产部署)
- [开发与发布](#开发与发布)
- [许可证](#许可证)

## 功能特性

- **文章管理** — 通过 Django 管理后台创建和编辑文章，支持草稿、发布和置顶
- **Markdown 写作** — 前端渲染 Markdown，并为代码块提供语法高亮
- **文章插图** — 后台上传图片并插入正文，支持 JPG、PNG、GIF 和 WebP
- **标签与搜索** — 支持多标签联合筛选以及标题、正文、摘要和标签搜索
- **归档浏览** — 按年月分组展示已发布文章
- **明暗主题** — 支持主题切换、偏好记忆和 View Transition 过渡动画
- **响应式布局** — 适配桌面端和移动端，提供汉堡菜单与侧滑抽屉
- **国际化** — 支持简体中文和英文界面
- **一键部署** — 提供 Nginx、Gunicorn 和 systemd 配置，支持域名 HTTPS 与纯 IP 模式

## 技术栈

| 层级 | 技术 | 版本 |
|------|------|------|
| 后端框架 | Django | 5.2 LTS |
| REST API | Django REST Framework | 3.17.1 |
| 管理后台 | django-unfold | 0.81.0 |
| 前端框架 | Vue 3（Composition API） | 3.5 |
| 构建工具 | Vite | 8.1 |
| 路由 | Vue Router | 4.6 |
| 状态管理 | Pinia | 4.0 |
| HTTP 客户端 | Axios | 1.18 |
| Markdown 渲染 | markdown-it + highlight.js | — |
| WSGI 服务器 | Gunicorn | 26.0 |
| 反向代理 | Nginx | — |

## 快速开始

### 1. 环境要求

| 工具 | 要求 |
|------|------|
| Python | 3.10+ |
| Node.js | `^20.19.0` 或 `>=22.12.0` |
| npm | 随 Node.js 安装 |

Node.js 版本要求来自 Vite 8；满足其中一个版本范围即可。

### 2. 克隆项目

```bash
git clone https://github.com/foooold/BlogWebsite.git
cd BlogWebsite
```

### 3. 配置后端

```bash
python -m venv venv
```

激活虚拟环境：

```bash
# Linux / macOS
source venv/bin/activate
```

```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1
```

安装依赖并创建本地环境变量文件：

```bash
pip install -r requirements.txt

# Linux / macOS
cp .env.example .env
```

```powershell
# Windows PowerShell
Copy-Item .env.example .env
```

编辑 `.env`，至少设置：

```dotenv
SECRET_KEY=替换为随机生成的密钥
DEBUG=True
```

初始化数据库并创建管理员：

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. 配置前端

```bash
cd frontend
npm ci
cd ..
```

`npm ci` 会严格按照 `frontend/package-lock.json` 安装依赖，适合首次安装和可复现构建。添加或升级依赖时应使用 `npm install`。

### 5. 启动开发服务

打开两个终端，并确保后端终端已激活 Python 虚拟环境。

终端 1，在项目根目录启动 Django：

```bash
python manage.py runserver 0.0.0.0:8000
```

终端 2，启动 Vite：

```bash
cd frontend
npm run dev
```

| 地址 | 用途 |
|------|------|
| `http://localhost:5173` | 博客前端 |
| `http://localhost:8000/zh-hans/admin/` | 管理后台（默认 `ADMIN_PATH=admin/`） |
| `http://localhost:8000/api/hello/` | API 健康检查 |

开发模式下，Vite 会把 `/api` 和 `/media` 请求代理到 `127.0.0.1:8000`，并为前端代码启用热更新。

### 6. 发布文章

登录管理后台后即可创建标签和文章。新增或编辑文章时，可点击正文输入框上方的“上传并插入图片”，上传不超过 10 MB 的 JPG、PNG、GIF 或 WebP 图片。上传成功后，图片对应的 Markdown 会插入当前光标位置。

### 7. 验证项目

```bash
# 后端配置检查与自动化测试
python manage.py check
python manage.py test

# 前端生产构建
cd frontend
npm run build
```

建议在首次配置、修改代码以及部署前执行这些检查。

## 项目配置

环境变量定义在项目根目录的 `.env` 中，可参考 `.env.example`：

| 变量 | 说明 | 示例 |
|------|------|------|
| `SECRET_KEY` | Django 密钥；生产环境必须随机生成并保密 | `django-insecure-...` |
| `DEBUG` | 调试模式；生产环境必须为 `False` | `True` / `False` |
| `ALLOWED_HOSTS` | 允许访问的主机名或 IP | `example.com,www.example.com` |
| `CSRF_TRUSTED_ORIGINS` | CSRF 信任来源，必须包含协议 | `https://example.com,https://www.example.com` |
| `CORS_ALLOWED_ORIGINS` | CORS 允许来源，必须包含协议 | `https://example.com,https://www.example.com` |
| `ADMIN_PATH` | 管理后台路径 | `admin/` |
| `OPENAI_API_KEY` | DeepSeek API 密钥，仅用于 AI changelog | `sk-...` |

`203.0.113.10` 等 IP 仅用于文档示例。部署时必须替换为服务器的真实公网 IPv4 地址。

## 项目结构

```text
.
├── config/                 # Django 项目配置、根路由与 WSGI 入口
├── main/                   # 数据模型、REST API、后台管理与测试
│   └── static/main/admin/  # 后台 Markdown 图片上传组件
├── frontend/               # Vue 3 前端
│   ├── src/
│   │   ├── api/            # Axios API 封装
│   │   ├── components/     # 通用组件
│   │   ├── composables/    # 组合式函数
│   │   ├── router/         # Vue Router 配置
│   │   ├── stores/         # Pinia 状态
│   │   └── views/          # 页面视图
│   └── vite.config.js      # 开发代理与生产构建配置
├── deploy/                 # Nginx、Gunicorn、systemd 与部署脚本
├── media/                  # 用户上传文件
├── static/                 # 前端构建产物与项目静态资源
├── staticfiles/            # collectstatic 输出
├── templates/              # Django SPA 入口模板
├── .env.example            # 环境变量模板
├── CHANGELOG.md            # 版本更新日志
├── manage.py               # Django 管理入口
├── requirements.txt        # Python 依赖
└── package.json            # changelog 与版本发布脚本
```

## 接口参考

### REST API

| 方法 | 端点 | 说明 |
|------|------|------|
| `GET` | `/api/hello/` | 健康检查 |
| `GET` | `/api/articles/` | 已发布文章列表 |
| `GET` | `/api/articles/<slug>/` | 单篇文章详情 |
| `GET` | `/api/tags/` | 标签列表及文章数量 |
| `GET` | `/api/search/?q=<keyword>` | 搜索文章和标签 |
| `GET` | `/api/changelog/` | 最近五个版本的更新日志 |

### 前端路由

| 路径 | 页面 | 说明 |
|------|------|------|
| `/` | 首页 | 个人简介与最新文章 |
| `/blog` | 博客列表 | 标签筛选与分页 |
| `/blog/:slug` | 文章详情 | Markdown 渲染与代码高亮 |
| `/archive` | 归档 | 按年月浏览文章 |
| `/about` | 关于 | 个人介绍与站点统计 |

## 生产部署

项目提供面向 Ubuntu 的 Nginx + Gunicorn + systemd 一键部署脚本，必须以 root 权限运行。

### 部署准备

- **域名模式**：将裸域名和 `www` 域名解析到服务器，并准备同时覆盖二者的 TLS 证书。
- **IP 模式**：准备服务器真实公网 IPv4 地址；该模式使用 HTTP。

域名模式默认读取以下证书文件：

```text
/etc/letsencrypt/live/example.com/fullchain.pem
/etc/letsencrypt/live/example.com/privkey.pem
```

部署脚本不会自动申请证书。证书不存在时，域名模式的 Nginx 配置检查将失败；暂不使用 TLS 时请选择 IP 模式。

### 执行部署

```bash
cd /home/www
git clone https://github.com/foooold/BlogWebsite.git
cd BlogWebsite
sudo bash deploy/deploy.sh
```

脚本会交互式询问部署模式和域名或 IP，并自动完成：

- 安装 Nginx、Python 和 Node.js
- 创建 Python 虚拟环境并安装依赖
- 构建前端并收集 Django 静态文件
- 创建或更新 `.env` 中的主机和来源配置
- 执行数据库迁移
- 配置并启动 Gunicorn 与 Nginx
- 拒绝未配置的 Host

域名模式会启用 HTTPS，并把裸域名重定向到 `https://www.example.com`；IP 模式通过 `http://服务器IP` 直接访问。

再次运行部署脚本时，`ALLOWED_HOSTS`、`CSRF_TRUSTED_ORIGINS` 和 `CORS_ALLOWED_ORIGINS` 会按本次输入更新，已有的 `SECRET_KEY`、`ADMIN_PATH` 和 `OPENAI_API_KEY` 会保留。

如果生产环境登录后台时出现 HTTP 500，请检查项目目录和 `db.sqlite3` 是否允许 Gunicorn 的 `www-data` 用户写入。部署脚本会自动设置相关权限。

## 开发与发布

### 生成更新日志和提交信息

项目使用 [lazy-changelog](https://github.com/nicepkg/lazy-changelog) 和 DeepSeek 生成 CHANGELOG 与提交信息。先在项目根目录安装工具依赖，并在 `.env` 中设置有效的 `OPENAI_API_KEY`：

```bash
npm ci

npm run log          # 生成 CHANGELOG
npm run log:diff     # 生成包含代码差异的 CHANGELOG
npm run log:dry      # 预览，不写入文件
npm run commit       # 交互式生成提交信息
npm run commit:msg   # 仅输出提交信息
```

`log` 和 `log:diff` 默认处理最新 tag 到 `HEAD` 的提交。指定区间时，通过 `--` 传递参数：

```bash
npm run log:diff -- --from v1.0.0 --to v1.1.0 --tag v1.1.0
npm run log:dry -- --from v1.0.0 --to v1.1.0
```

### 发布版本

```bash
# 更新 package.json、创建提交并添加 Git tag
npm version 1.2.3

git push
git push --tags
```

## 许可证

本项目采用 [MIT License](LICENSE)。

## 作者

**Frank Du** — [GitHub @foooold](https://github.com/foooold)
