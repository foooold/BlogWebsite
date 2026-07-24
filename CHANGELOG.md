## 1.0.0 (2026-07-24)

### Features
- [commits] Route switching now automatically updates the page title
- [commits] Article cards and detail pages display the author’s name
- [commits] Rewrote the About page and added a repository link
- [commits] Mobile responsive adaptation: added hamburger menu, drawer navigation, copy button visibility adjustments, and global breakpoints
- [commits] Added a footer placeholder for ICP filing number

### Bug Fixes
- [commits] Fixed search highlighting incorrectly rendering HTML tags by escaping article text
- [commits] Admin: replaced filter_horizontal with autocomplete_fields for article/user/group tags, and removed the user_permissions field from the UserAdmin edit form
- [commits] Fixed the search box showing excessively long matching content prefixes/suffixes; now displays only one line
- [commits] Fixed pagination not resetting to page 1 after switching tags on the blog page
- [commits] Fixed code block copy button not working under HTTP connections

### Improvements
- [commits] Integrated lazy-changelog with DeepSeek for AI-powered changelog generation and commit messages; added patch-package, dotenv-cli, and localized prompts to Chinese
- [commits] Article excerpts now rendered using markdown-it for proper Markdown formatting
- [commits] Deploy script made repeatable (idempotent)
- [commits] Improved page title display
- [commits] Removed Vite auto-generated dist directory from version control
- [commits] Updated ignore configuration
- [commits] Removed unnecessary files
