<div align="center">

# BlogWebsite

基于 Django + Vue 3 的个人博客网站，支持 Markdown 写作、标签筛选、全文搜索、归档和响应式布局。

</div>

<div align="center">
    <img alt="Python" src="https://img.shields.io/badge/Python-3.14+-blue?logo=python&logoColor=white">
    <img alt="Node.js" src="https://img.shields.io/badge/Node.js-v24+-green?logo=nodedotjs&logoColor=white">
    <a href="#license"><img alt="GitHub License" src="https://img.shields.io/github/license/foooold/BlogWebsite"></a>
</div>

## 技术栈

| 层级 | 技术 | 版本 |
|------|------|------|
| **后端框架** | Django | 6.0.7 |
| **REST API** | Django REST Framework | 3.17.1 |
| **管理后台** | django-unfold | 0.101.0 |
| **前端框架** | Vue 3 (Composition API) | 3.5 |
| **构建工具** | Vite | 8.1 |
| **路由** | Vue Router | 4.6 |
| **状态管理** | Pinia | 4.0 |
| **HTTP 客户端** | Axios | 1.18 |
| **Markdown 渲染** | markdown-it + highlight.js | — |
| **WSGI 服务器** | Gunicorn | 26.0 |
| **反向代理** | Nginx | — |

## 功能

- **文章管理** — Django 管理后台创建/编辑文章，支持草稿/发布状态
- **Markdown 写作** — 文章内容使用 Markdown，前端渲染带语法高亮的代码块
- **文章插图** — 后台上传图片并自动插入正文，前台自适应显示并支持懒加载
- **标签系统** — 多标签分类，支持多标签联合筛选
- **全文搜索** — 搜索文章标题、内容、摘要和标签，带关键词高亮和上下文摘录
- **文章归档** — 按年月分组浏览所有文章
- **暗色主题** — GitHub-dark 风格配色
- **响应式布局** — 桌面端导航栏 + 移动端汉堡菜单 + 侧滑抽屉
- **国际化** — 支持中文（简体）和英文界面切换
- **一键部署** — 提供完整的 Nginx + Gunicorn + systemd 部署脚本

## 快速开始

### 本地开发

```bash
# 1. 克隆仓库
git clone git@github.com:foooold/BlogWebsite.git
cd BlogWebsite

# 2. 创建并激活 Python 虚拟环境
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. 安装 Python 依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env，至少设置 SECRET_KEY 和 DEBUG=True

# 5. 数据库迁移
python manage.py migrate

# 6. 创建管理员账户
python manage.py createsuperuser

# 7. 安装前端依赖
cd frontend
npm install
cd ..

# 8. 启动开发服务器（需要两个终端）

# 终端 1：Django 后端（端口 8000）
python manage.py runserver 0.0.0.0:8000

# 终端 2：Vite 前端开发服务器（端口 5173）
cd frontend
npm run dev
```

浏览器访问 `http://localhost:5173` 查看前端；若未在环境变量中修改路径，默认访问 `http://localhost:8000/zh-hans/admin/` 进入管理后台。

> **说明**：开发模式下，Vite 将 `/api` 请求代理到 Django `127.0.0.1:8000`，前端代码修改支持 HMR 热更新。

在后台新增或编辑文章时，点击正文输入框上方的“上传并插入图片”，选择 JPG、PNG、GIF 或 WebP 图片。上传成功后，图片的 Markdown 语法会自动插入当前光标位置；可直接修改方括号里的文字作为图片说明。单张图片上限为 10 MB。

## 项目结构

```
.
├── config/                 # Django 项目配置
│   ├── settings.py         # 设置（数据库、中间件、CORS、DRF、i18n）
│   ├── urls.py             # 根路由（API / i18n / admin / SPA 兜底）
│   └── wsgi.py             # WSGI 入口（生产环境用）
├── main/                   # Django 主应用
│   ├── models.py           # Article 和 Tag 数据模型
│   ├── serializers.py      # DRF 序列化器
│   ├── api.py              # REST API 视图函数
│   ├── urls.py             # API 路由
│   ├── admin.py            # django-unfold 管理后台配置
│   └── views.py            # SPA 兜底视图（Vite manifest 读取）
├── frontend/               # Vue 3 前端
│   ├── src/
│   │   ├── main.js         # Vue 入口
│   │   ├── App.vue         # 根组件（导航栏、抽屉、页脚）
│   │   ├── style.css       # 全局样式（暗色主题）
│   │   ├── api/index.js    # Axios API 封装
│   │   ├── router/index.js # Vue Router 路由配置
│   │   ├── stores/app.js   # Pinia 状态管理
│   │   ├── composables/    # 组合式函数
│   │   ├── components/     # 通用组件
│   │   └── views/          # 页面视图
│   └── vite.config.js      # Vite 配置
├── deploy/                 # 生产部署配置
│   ├── deploy.sh           # 一键部署脚本
│   ├── gunicorn.conf.py    # Gunicorn 配置
│   ├── nginx.conf          # 域名模式 Nginx 配置
│   ├── nginx.ip.conf       # IP 模式 Nginx 配置
│   └── systemd/            # systemd 服务单元
├── templates/              # Django 模板（SPA 入口）
├── static/                 # 静态文件（含 Vite 构建产物）
├── .env.example            # 环境变量模板
├── AGENTS.md               # AI 代理项目文档
├── CHANGELOG.md            # 更新日志（AI 自动生成）
├── requirements.txt        # Python 依赖
└── package.json            # 根级 Node 脚本（changelog 生成）
```

## API 接口

| 方法 | 端点 | 说明 |
|------|------|------|
| `GET` | `/api/hello/` | 健康检查 |
| `GET` | `/api/articles/` | 已发布文章列表 |
| `GET` | `/api/articles/<slug>/` | 单篇文章详情 |
| `GET` | `/api/tags/` | 标签列表（含文章计数） |
| `GET` | `/api/search/?q=<keyword>` | 搜索文章和标签 |

## 前端路由

| 路径 | 页面 | 说明 |
|------|------|------|
| `/` | 首页 | 个人简介 + 最新文章 |
| `/blog` | 博客列表 | 标签筛选 + 分页 |
| `/blog/:slug` | 文章详情 | Markdown 渲染 + 代码高亮 |
| `/archive` | 归档 | 按年月分组浏览 |
| `/about` | 关于 | 个人介绍 + 站点统计 |

## 环境变量

参考 `.env.example`：

| 变量 | 说明 | 示例 |
|------|------|------|
| `SECRET_KEY` | Django 密钥 | `django-insecure-...` |
| `DEBUG` | 调试模式 | `True` / `False` |
| `ALLOWED_HOSTS` | 允许的主机名 | `example.com,www.example.com` 或 `203.0.113.10` |
| `CSRF_TRUSTED_ORIGINS` | CSRF 信任的来源 | `http://example.com,http://www.example.com` 或 `http://203.0.113.10` |
| `CORS_ALLOWED_ORIGINS` | CORS 允许的源 | `http://example.com,http://www.example.com` 或 `http://203.0.113.10` |
| `ADMIN_PATH` | django后台路径 | 默认 `admin/`（可改为自定义路径防扫描） |
| `OPENAI_API_KEY` | DeepSeek API 密钥（AI changelog 用） | `sk-...` |

## 部署

项目包含完整的生产环境部署方案（Ubuntu + Nginx + Gunicorn）：

如果使用域名，部署前请先在 DNS 服务商处将裸域名和对应的 `www` 域名解析到服务器。例如输入 `example.com` 时，需要确保 `example.com` 和 `www.example.com` 都已指向服务器。没有域名时可以直接选择 IP 模式。

```bash
# 在目标服务器上以 root 执行
sudo bash deploy/deploy.sh
# 域名模式
# Do you have a domain? [y/n]: y
# Enter root domain (e.g. example.com)

# IP 模式
# Do you have a domain? [y/n]: n
# Enter server IPv4 address (e.g. 203.0.113.10): 203.0.113.10
```

部署脚本会自动完成：
- 安装系统依赖（nginx, Python, Node.js）
- 创建 Python 虚拟环境并安装依赖
- 构建前端静态资源
- 生成 `.env` 配置文件
- 运行数据库迁移和静态文件收集
- 配置 Gunicorn systemd 服务
- 根据域名或 IP 模式配置 Nginx 反向代理；域名模式会将裸域名永久重定向到 `www` 域名

部署脚本会在每次运行时根据所选模式同步 `.env` 中的主机配置，但会保留 `SECRET_KEY`、`ADMIN_PATH`、`OPENAI_API_KEY` 等其他已有配置。当前部署仅启用 HTTP：域名模式下，访问 `http://example.com/path` 会重定向到 `http://www.example.com/path`；IP 模式下，博客通过输入的 IPv4 地址直接访问。两种模式都会拒绝未配置的 Host。

## AI 辅助开发

项目集成了 [lazy-changelog](https://github.com/nicepkg/lazy-changelog) + DeepSeek，用于自动生成 CHANGELOG 和提交信息：

```bash
npm run log          # 生成 CHANGELOG
npm run log:diff     # 生成含代码差异的 CHANGELOG
npm run log:dry      # 预览 CHANGELOG（不写入文件）
npm run commit       # 生成提交信息（交互式）
npm run commit:msg   # 生成提交信息（仅输出）
```

> 需要设置 `OPENAI_API_KEY` 为有效的 DeepSeek API 密钥。

**`log:diff` / `log` 默认只覆盖最新 tag → HEAD**。要为特定区间生成 changelog，通过 `--` 传递额外参数：

```bash
# 为 v1.0.0 → v1.1.0 区间生成 changelog（打 tag 后补生成）
npm run log:diff -- --from v1.0.0 --to v1.1.0 --tag v1.1.0

# 为整个项目历史生成 changelog（无 tag 时）
npm run log:diff -- --from $(git rev-list --max-parents=0 HEAD) --tag v1.0.0

# 预览将要生成的内容（不写入文件）
npm run log:dry -- --from v1.0.0 --to v1.1.0
```

## 更新版本号

**发布新版本**：使用 `npm version <版本号>` ，自动完成：更新 `package.json` → git commit → git tag 。

```bash
npm version v1.2.3       # 发布 v1.2.3 版

git push && git push --tags
```

## LICENSE

Copyright (c) 2026 Frank Du

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Author

**Frank Du** — [GitHub @foooold](https://github.com/foooold)
