## v0.5.0 (2026-07-25)

### Features
- Added Django logging configuration and deployment support

### Bug Fixes
- Fixed incorrect package version number
- Corrected database file permission settings in the deployment script
- Removed `@ai-sdk/openai` dependency and updated the `lazy-changelog` patch to resolve a compatibility issue

### Improvements
- Simplified logging configuration to output exclusively to the console

## v0.4.0 (2026-07-24)

### Features
- Page title automatically updates when navigating between routes

### Bug Fixes
- Search highlight HTML-escapes original content to prevent article tags from being mistakenly rendered

### Improvements
- Integrated lazy-changelog with DeepSeek AI to auto-generate changelogs and commit messages
- Added dotenv-cli to automatically parse environment variables for build scripts
- Applied lazy-changelog patches with patch-package and localized prompts to Chinese
- Synced AGENTS.md configuration file for AI-assisted workflows

## v0.3.0 (2026-07-23)

### Features
- Article cards and detail pages now display the author name.
- About page rewritten with updated content and a link to the repository.

### Bug Fixes
- Admin: Replaced `filter_horizontal` with `autocomplete_fields` for article, user, and group tag fields, and removed the `user_permissions` field from the UserAdmin edit form to improve performance.
- Search: Fixed match display showing overly long prefix and suffix, now limited to a single line.
- Blog: Fixed pagination not resetting to page 1 after switching tags.
- Fixed code block copy button not working when the site is served over HTTP.

### Improvements
- Article excerpts are now rendered using markdown-it for richer summary formatting.
- Code block copy button is hidden on mobile devices for a cleaner interface.
- Updated the page `<title>` tag.

## v0.2.0 (2026-07-22)

### Features
- Added mobile responsive layout with hamburger menu and drawer navigation
- Made copy buttons visible on mobile screens
- Added global responsive breakpoints for consistent layout scaling
- Added a placeholder area for ICP filing number in the page footer

### Improvements
- Updated the page `<title>` to reflect current branding/content
- Removed unused files to clean up the project structure
- Deployment script now supports repeatable, idempotent execution

## v0.1.0 (2026-07-21)

- Here is the start