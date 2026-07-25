## 1.1.0 (2026-07-25)

### Features
- [commits] Automatically update the page title on route changes (34f8bc9)
- [commits] Display author names in article cards and detail pages (9d0c11b)
- [commits] Redesigned the About page with a repository link (218df02)
- [commits] Added a footer ICP filing placeholder (924e9f2)
- [commits] Mobile responsive layout: hamburger menu, drawer navigation, global breakpoints (eef8bf6)
- [commits] Django logging configuration with deployment-friendly settings (9ce61b7)

### Bug Fixes
- [commits] Fixed database file permission handling in the deploy script (60ab09e)
- [commits] Search highlighting now HTML-escapes original text to prevent incorrect tag rendering (bd55a50)
- [commits] Limited search match snippets to a single line with appropriate truncation (fe5bc79)
- [commits] Admin: replaced `filter_horizontal` with `autocomplete_fields` for article/user/group tags; removed `user_permissions` field from UserAdmin (baf1550)
- [commits] Pagination now resets to page 1 after switching tags (14e0b04)
- [commits] Fixed copy button not working in non‑HTTPS environments (89d875e)
- [commits] Hidden copy button on mobile to prevent layout conflicts (7587fc7)

### Improvements
- [commits] Article summaries are now rendered with `markdown-it` instead of previous method (a49c634)
- [commits] Simplified Django logging to console output only (a77ab2c)
- [commits] Removed the Vite‑generated `dist` directory from version control (f6e92cb)
- [commits] Made the deploy script idempotent for safe repeated runs (63c1ee1)
- [commits] Integrated `lazy-changelog` with DeepSeek for AI‑generated changelogs and commit messages, plus dotenv‑cli support, Chinese prompts, and patch updates (453fea0, ad5edfa, 3ecdeb3, 4a681ba)
- [commits] Updated AGENTS.md with AI tooling, deployment, and logging documentation (e825eae)
