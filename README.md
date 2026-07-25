# BlogWebsite

个人博客系统 — 基于 Django + Vue 3 的全栈博客应用，支持 Markdown 写作、标签筛选、全文搜索、归档、多语言、暗色主题和响应式布局。

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
- **标签系统** — 多标签分类，支持多标签联合筛选
- **全文搜索** — 搜索文章标题、内容、摘要和标签，带关键词高亮和上下文摘录
- **文章归档** — 按年月分组浏览所有文章
- **暗色主题** — GitHub-dark 风格配色
- **响应式布局** — 桌面端导航栏 + 移动端汉堡菜单 + 侧滑抽屉
- **国际化** — 支持中文（简体）和英文界面切换
- **一键部署** — 提供完整的 Nginx + Gunicorn + systemd 部署脚本

## 快速开始

### 环境要求

- Python 3.14+
- Node.js v24+

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

浏览器访问 `http://localhost:5173` 查看前端，访问 `http://localhost:8000/zh-hans/admin/` 进入管理后台。

> **说明**：开发模式下，Vite 将 `/api` 请求代理到 Django `127.0.0.1:8000`，前端代码修改支持 HMR 热更新。

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
│   ├── nginx.conf          # Nginx 反向代理配置
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
| `ALLOWED_HOSTS` | 允许的主机名 | `*,localhost` |
| `CORS_ALLOWED_ORIGINS` | CORS 允许的源 | `http://localhost:5173` |
| `OPENAI_API_KEY` | DeepSeek API 密钥（AI changelog 用） | `sk-...` |

## 部署

项目包含完整的生产环境部署方案（Ubuntu + Nginx + Gunicorn）：

```bash
# 在目标服务器上以 root 执行
sudo bash deploy/deploy.sh
```

部署脚本会自动完成：
- 安装系统依赖（nginx, Python, Node.js）
- 创建 Python 虚拟环境并安装依赖
- 构建前端静态资源
- 生成 `.env` 配置文件
- 运行数据库迁移和静态文件收集
- 配置 Gunicorn systemd 服务
- 配置 Nginx 反向代理

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

## 许可

本项目未指定许可证。如有需要请联系作者。

## 作者

**Frank Du** — [GitHub @foooold](https://github.com/foooold)
