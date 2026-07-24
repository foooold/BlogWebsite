## 1.0.0 (2026-07-24)

### ✨ Features
- [commits] Added automatic page title updates on route changes for improved navigation context
- [commits] Display author names on article cards and detail pages
- [commits] Rewrote About page content and added repository link

### 🐛 Bug Fixes
- [commits] Fixed HTML escaping on search highlights to prevent tag text from being incorrectly rendered
- [commits] Fixed search box displaying excessively long match prefixes/suffixes; now limited to single-line display
- [commits] Fixed pagination not resetting to page 1 when switching tags in the blog view
- [commits] Fixed code block copy button not working under HTTP environment
- [commits] Fixed missing responsive adaptation for mobile devices; added hamburger menu + drawer navigation, adjusted copy button visibility, and global breakpoints
- [commits] Fixed Vite auto-generated `dist` build directory not being excluded from version control

### 🛠️ Improvements
- [commits] Replaced `filter_horizontal` with `autocomplete_fields` for article/user/group tag fields in admin; removed `user_permissions` field from UserAdmin edit interface
- [commits] Replaced article summary rendering with `markdown-it` for better markdown support
- [commits] Hid code block copy button on mobile devices
- [commits] Added reserved placeholder for footer (ICP/filing info)
- [commits] Updated deployment script to be idempotent (safe to run multiple times)
- [commits] Removed unnecessary files from the project
- [commits] Updated various ignore configuration files
- [commits] Changed default `<title>` element content
- [commits] Synced AGENTS.md documentation
