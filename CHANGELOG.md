## v0.7.0 (2026-08-04)

### Features
- Added update changelog sidebar on the homepage (4062780)
- Redesigned homepage layout (bd6a437)

### Bug Fixes
- Fixed drawer and overlay positioning to be relative to the app container, preventing it from blocking the navigation bar (8cc6a28)
- Fixed homepage layout issues (ee87b16)

### Improvements
- Refactored homepage layout structure (3bbda9c)
- Refactored homepage content components (7b5e479)
- Removed hardcoded deploy path and replaced it with dynamic directory injection (0fa2dd2)
- Updated left-side component styling in the navigation bar (44ae599)

## v0.6.1 (2026-07-28)

### Features
- Modified navigation bar left component styling (c323eef)

### Improvements
- Changed favicon (48950e3)
- Updated about page content (0cb50e3)
- Added avatar image (c4205ae)
- Removed AGENTS.md file from the repository (299e13c)

## v0.6.0 (2026-07-27)

### Features
- Added article pinning feature (0a76de1)

### Improvements
- Refactored database migration files (6ef134b)
- Removed explicit `.order_by` declarations from API queries (e794fcc)
- Updated `.gitignore`: removed backup ignore rules, added `AGENTS.md` and `*.bak` (14a4ed6)

## v0.5.5 (2026-07-27)

### Features
- Updated lazy-changelog to use tag date, show v prefix, adjust AI temperature, and enable compatibility mode (4666506)

### Improvements
- Updated README.md documentation (1e1b211)

## v0.5.4 (2026-07-27)

### Features
- Prefixed version number with "v" (e1e3b81)
- Added short commit hash at the end of changelog entries (175f4c7)
- Enabled HTML rendering and heading anchor links in the frontend (ff563e8)
- Added `markdown-it-anchor` dependency to support heading anchors (fc04f2b)

### Improvements
- Removed unused files from the repository (a52ec83)

## v0.5.3 (2026-07-26)

### Features
- Added support for configurable Django admin URL path via the `ADMIN_PATH` environment variable (cbbd8c6)
- Implemented URL routing to use the configurable admin path and added a redirect from the old `/admin` path (7e0bf71)

### Improvements
- Included `ADMIN_PATH` in environment example template (1ad61ea)
- Set `ADMIN_PATH` environment variable in deployment configuration to ensure backward compatibility (2f37e23)
- Updated reference documentation (cff7305)
- Updated README with latest changes (34f6ce7, 5af796e)

## v0.5.2 (2026-07-26)

### Improvements
- Added LICENSE file (ba31699)
- Updated AGENTS.md documentation (a1e820b)
- Updated README.md documentation (f33db80)
- Bumped project version to 0.5.0 (d180707)
- Updated CHANGELOG.md (490a1b9)
- Optimized prompts and adjusted AI generation configuration for lazy-changelog (8cc8573)

## v0.5.1 (2026-07-25)

### Improvements
- Updated AGENTS.md with improved release process documentation (97ee836)
- Updated issue templates (18f2a03)
- Updated issue templates (ad664dd)

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