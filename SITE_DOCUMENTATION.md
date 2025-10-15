# Daystareld.com Website Documentation

**Last Updated:** October 15, 2025  
**Site URL:** https://daystareld.com  
**GitHub Repository:** https://github.com/DaystarEld/daystareld.github.io

---

## Table of Contents

1. [Overview](#overview)
2. [Site Structure](#site-structure)
3. [Technology Stack](#technology-stack)
4. [Key Features](#key-features)
5. [File Organization](#file-organization)
6. [How to Make Changes](#how-to-make-changes)
7. [Common Tasks](#common-tasks)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)

---

## Overview

This is a static website hosted on GitHub Pages, migrated from WordPress. It contains:
- Personal blog posts (84 posts)
- Pokemon: The Origin of Species web serial (143 chapters)
- Rationally Writing podcast episodes (67 episodes)
- Other fiction stories (Guardian, Hearts and Minds, HPMOR Remix, etc.)

The site is built with pure HTML/CSS/JavaScript - no frameworks, no build process, just static files.

---

## Site Structure

```
daystareld.github.io/
├── index.html                 # Homepage
├── CNAME                      # Custom domain configuration
├── robots.txt                 # Search engine instructions
├── sitemap.xml                # Site map for SEO
├── search.js                  # Client-side search functionality
├── search.json                # Search index data
├── 404.html                   # Custom 404 page with smart redirects
├── COMMENTING_SETUP.md        # Guide for setting up Giscus comments
├── SITE_DOCUMENTATION.md      # This file
│
├── blog/                      # Blog posts
│   ├── index.html            # Blog index page
│   ├── [post-slug]/          # Individual blog posts
│   │   └── index.html
│   └── ...
│
├── pokemon/                   # Pokemon: The Origin of Species
│   ├── index.html            # Pokemon index/table of contents
│   ├── [chapter-number]/     # Individual chapters (1-143)
│   │   └── index.html
│   ├── pokemon-faq/          # FAQ page
│   ├── pokemon-team-roster/  # Team roster pages
│   ├── pokemon-fan-art/      # Fan art page
│   └── pokemon-goal-factoring/
│
├── rationally-writing/        # Podcast episodes
│   ├── index.html            # Episode index
│   └── [episode-number]/     # Individual episodes (0-66)
│       └── index.html
│
├── stories/                   # Other fiction
│   └── index.html            # Stories index
│
├── guardian/                  # Guardian story pages
├── guardian-1/
├── guardian-2/
├── hearts-and-minds/
├── hpmor-remix/
├── hpmor-remix-1/
├── hpmor-remix-2/
├── hpmor-remix-3/
├── hpmor-remix-4/
├── because-prophecy/
│
├── scripts/                   # Python utility scripts
│   ├── wordpress_parser.py   # Parse WordPress XML exports
│   ├── fix_pokemon_chapters.py
│   ├── fix_blog_posts.py
│   ├── update_blog_index.py
│   ├── update_blog_links.py
│   ├── update_search_json.py
│   ├── extract_pokemon_pages.py
│   ├── add_favicon.py
│   ├── add_lazy_loading.py
│   └── add_seo_enhancements.py
│
├── Original files/            # Backup files (not deployed)
│   ├── daystareld.WordPress.2025-10-07.xml
│   └── Disqus/
│       └── tmpyX23Tk         # Disqus export
│
└── .gitignore                 # Git ignore rules
```

---

## Technology Stack

### Core Technologies
- **HTML5** - Page structure
- **CSS3** - Styling with CSS variables for theming
- **Vanilla JavaScript** - Search functionality, no frameworks

### Hosting & Deployment
- **GitHub Pages** - Free static site hosting
- **Custom Domain** - daystareld.com via CNAME
- **Git** - Version control

### Development Tools
- **Python 3** - Utility scripts for content generation
- **Local Server** - `python -m http.server 8000` for testing

### External Services
- **Giscus** - GitHub Discussions-based commenting (optional, needs setup)

---

## Key Features

### 1. Design & Styling

**Color Scheme:**
- Dark theme with CSS variables
- Primary colors: `--bg`, `--text`, `--accent`, `--accent-2`
- Green gradient accents on titles: `linear-gradient(90deg, var(--accent), var(--accent-2))`

**Typography:**
- System font stack for performance
- Responsive font sizing with `clamp()`
- Line height optimized for readability (1.8 for content)

**Layout:**
- Responsive design (mobile-first)
- Max-width containers (800px for content)
- Flexbox for navigation and layout

### 2. Navigation

**Header Navigation:**
- Sticky header on all pages
- Links to: Home, Blog, Pokemon, Rationally Writing, Stories
- Search functionality (Ctrl+K or click search icon)

**Page Navigation:**
- Pokemon chapters: Previous/ToC/Next buttons
- Blog posts: Category-based organization
- Breadcrumb-style back links

### 3. Search Functionality

**Implementation:**
- Client-side search using `search.js`
- Search index in `search.json` (auto-generated)
- Searches titles, excerpts, and content
- Keyboard shortcut: Ctrl+K or Cmd+K
- Overlay UI with live results

**Updating Search Index:**
```bash
python scripts/update_search_json.py
```

### 4. Comments System

**Hybrid Approach:**
- **Old Comments:** 471 archived Disqus comments converted to static HTML
- **New Comments:** Giscus widget (GitHub Discussions-based)
- Comments appear after navigation buttons
- Styled to match site theme

**Pages with Comments:**
- 104 Pokemon chapters (chapters 6-142)
- 16 blog posts

**Setup Giscus:** See `COMMENTING_SETUP.md`

### 5. SEO Features

**Implemented:**
- `sitemap.xml` - All 312+ pages indexed
- `robots.txt` - Search engine instructions
- Meta tags on all pages (title, description)
- Canonical URLs
- Lazy loading images
- Favicon support (add `favicon.ico` to root)

**Smart 404 Redirects:**
- Old WordPress URLs automatically redirect to new structure
- Pokemon chapters: `/pokemon-8/` → `/pokemon/8/`
- RW episodes: `/rationally-writing-5/` → `/rationally-writing/5/`
- Blog posts: `/slug/` → `/blog/slug/`

### 6. Performance Optimizations

- No external CSS/JS frameworks
- Lazy loading for images
- Minimal HTTP requests
- Static files = fast loading
- No database queries

---

## File Organization

### HTML Page Structure

All pages follow a similar structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Title</title>
    <meta name="description" content="Page description">
    <link rel="canonical" href="https://daystareld.com/path/">
    <link rel="icon" href="/favicon.ico" type="image/x-icon">
    <style>
        /* Inline CSS for performance */
        :root {
            --bg: #0a0e1a;
            --text: #e8e8e8;
            --accent: #4ade80;
            --accent-2: #22d3ee;
            /* ... more variables ... */
        }
        /* Page-specific styles */
    </style>
</head>
<body>
    <header>
        <!-- Navigation -->
    </header>
    
    <main class="container">
        <article>
            <!-- Content -->
        </article>
    </main>
    
    <!-- Search Overlay -->
    <script src="/search.js"></script>
</body>
</html>
```

### CSS Class Naming Conventions

**Common Classes:**
- `.container` - Main content wrapper (max-width: 800px)
- `.chapter-title` / `.article-title` - Page titles with gradient
- `.chapter-content` / `.article-content` - Main content area
- `.chapter-nav` / `.story-nav` / `.episode-nav` - Navigation buttons
- `.comments-section` - Old archived comments
- `.new-comments-section` - Giscus widget area
- `.featured-image` - Header images on blog posts

**Styling Patterns:**
- Gradient text: `background: linear-gradient(...); -webkit-background-clip: text; color: transparent;`
- Responsive sizing: `font-size: clamp(min, preferred, max);`
- Dark theme: All colors use CSS variables

---

## How to Make Changes

### Prerequisites

1. **Git installed** - For version control
2. **Python 3** - For utility scripts
3. **Text editor** - VS Code, Cursor, or any editor
4. **GitHub account** - With access to the repository

### Basic Workflow

1. **Clone the repository** (first time only):
   ```bash
   git clone https://github.com/DaystarEld/daystareld.github.io.git
   cd daystareld.github.io
   ```

2. **Make your changes** to HTML/CSS/JS files

3. **Test locally**:
   ```bash
   python -m http.server 8000
   # Visit http://localhost:8000 in browser
   ```

4. **Stage changes**:
   ```bash
   git add -A
   # or specific files:
   git add path/to/file.html
   ```

5. **Commit changes**:
   ```bash
   git commit -m "Description of changes"
   ```

6. **Push to GitHub**:
   ```bash
   git push origin main
   ```

7. **Wait 1-2 minutes** for GitHub Pages to deploy

### Important Git Commands

```bash
# Check status of changes
git status

# See what changed
git diff

# View commit history
git log --oneline

# Undo uncommitted changes to a file
git restore path/to/file.html

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Pull latest changes from GitHub
git pull origin main
```

---

## Common Tasks

### 1. Add a New Blog Post

**Manual Method:**
1. Create folder: `blog/my-new-post/`
2. Create `index.html` based on existing post template
3. Update `blog/index.html` to add link
4. Update `search.json` or run `python scripts/update_search_json.py`

**Using WordPress Export:**
1. Export from WordPress as XML
2. Place in `Original files/`
3. Run `python scripts/wordpress_parser.py`
4. Update blog index and search

### 2. Add a New Pokemon Chapter

1. Create folder: `pokemon/144/` (next chapter number)
2. Create `index.html` based on existing chapter template
3. Update `pokemon/index.html` to add link
4. Update previous chapter's "Next" link
5. Update search index

**Or use the script:**
```bash
python scripts/fix_pokemon_chapters.py
```

### 3. Update Site Colors

Edit CSS variables in any page's `<style>` section:

```css
:root {
    --bg: #0a0e1a;           /* Background */
    --text: #e8e8e8;         /* Text color */
    --muted: #9ca3af;        /* Muted text */
    --accent: #4ade80;       /* Primary accent (green) */
    --accent-2: #22d3ee;     /* Secondary accent (cyan) */
    --link: #60a5fa;         /* Links */
    --border: #1e293b;       /* Borders */
}
```

To update all pages, use find-and-replace across files.

### 4. Change Navigation Links

Edit the `<header>` section in each page:

```html
<nav>
    <a href="/">Home</a>
    <a href="/blog/">Blog</a>
    <a href="/pokemon/">Pokemon</a>
    <a href="/rationally-writing/">Rationally Writing</a>
    <a href="/stories/">Stories</a>
</nav>
```

### 5. Add Images

1. Place images in `images/` folder
2. Reference in HTML:
   ```html
   <img src="/images/my-image.jpg" alt="Description" loading="lazy">
   ```
3. Use `loading="lazy"` for performance

### 6. Update Search Index

After adding/modifying content:

```bash
python scripts/update_search_json.py
```

This regenerates `search.json` with all searchable content.

### 7. Add Favicon

1. Create 16x16 or 32x32 PNG/ICO file
2. Name it `favicon.ico`
3. Place in root directory
4. Already linked in all pages via:
   ```html
   <link rel="icon" href="/favicon.ico" type="image/x-icon">
   ```

### 8. Setup Giscus Comments

See detailed instructions in `COMMENTING_SETUP.md`, but briefly:

1. Enable GitHub Discussions in repo settings
2. Install Giscus app: https://github.com/apps/giscus
3. Get config IDs from https://giscus.app
4. Replace placeholders in HTML:
   - `REPLACE_WITH_REPO_ID`
   - `REPLACE_WITH_CATEGORY_ID`

### 9. Add Green Gradient to Text

Use this CSS pattern:

```css
.my-title {
    background: linear-gradient(90deg, var(--accent), var(--accent-2));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    font-weight: 600;
}
```

Apply to any element with class `my-title`.

---

## Deployment

### GitHub Pages Configuration

**Settings:**
- Source: Deploy from `main` branch
- Custom domain: `daystareld.com` (configured via CNAME file)
- HTTPS: Enabled (automatic)

**DNS Configuration (at domain registrar):**
```
Type: CNAME
Name: @  (or www)
Value: daystareld.github.io
```

**Deployment Process:**
1. Push to `main` branch
2. GitHub Actions automatically builds
3. Site live in 1-2 minutes
4. Check: https://daystareld.com

**Build Status:**
- View at: https://github.com/DaystarEld/daystareld.github.io/actions

### Files Not Deployed

These are excluded via `.gitignore`:
- `scripts/` - Development scripts
- `__pycache__/` - Python cache
- `.DS_Store` - Mac system files
- `.vscode/`, `.idea/` - Editor configs
- `*.pyc`, `*.tmp`, `*.bak` - Temporary files

---

## Troubleshooting

### Issue: Changes not showing on live site

**Solutions:**
1. Wait 2-3 minutes for deployment
2. Hard refresh browser: Ctrl+Shift+R (Cmd+Shift+R on Mac)
3. Clear browser cache
4. Check GitHub Actions for build errors
5. Verify changes were pushed: `git log --oneline -5`

### Issue: 404 errors on live site

**Solutions:**
1. Check file paths are correct (case-sensitive)
2. Ensure `index.html` exists in folder
3. Verify CNAME file contains: `daystareld.com`
4. Check DNS settings at domain registrar
5. Review `404.html` redirect logic

### Issue: Search not working

**Solutions:**
1. Regenerate search index: `python scripts/update_search_json.py`
2. Check `search.json` is valid JSON
3. Verify `search.js` is loaded
4. Check browser console for errors

### Issue: Comments not showing

**Solutions:**
1. Verify Giscus is configured (IDs replaced)
2. Check GitHub Discussions is enabled
3. Ensure Giscus app is installed
4. Check browser console for errors
5. Test with different browser/incognito

### Issue: Styling looks broken

**Solutions:**
1. Check CSS syntax in `<style>` tags
2. Verify CSS variables are defined in `:root`
3. Test in different browsers
4. Check for unclosed HTML tags
5. Validate HTML: https://validator.w3.org/

### Issue: Local server not starting

**Solutions:**
1. Check Python is installed: `python --version`
2. Try: `python3 -m http.server 8000`
3. Check port 8000 isn't in use
4. Try different port: `python -m http.server 8080`

---

## Best Practices

### Content Management

1. **Always test locally** before pushing to GitHub
2. **Use descriptive commit messages**
3. **Keep backups** of WordPress exports and Disqus data
4. **Update search index** after content changes
5. **Maintain consistent file naming** (lowercase, hyphens)

### Code Quality

1. **Validate HTML** before committing
2. **Keep CSS organized** (variables at top, logical grouping)
3. **Comment complex code**
4. **Use semantic HTML** (article, nav, header, etc.)
5. **Optimize images** before uploading

### Performance

1. **Use lazy loading** for images
2. **Inline critical CSS** (already done)
3. **Minimize HTTP requests**
4. **Compress images** (use tools like TinyPNG)
5. **Keep pages under 1MB** when possible

### SEO

1. **Unique titles** for each page
2. **Meta descriptions** (150-160 characters)
3. **Canonical URLs** on all pages
4. **Update sitemap** when adding pages
5. **Use descriptive alt text** for images

---

## Quick Reference

### File Locations

| Content Type | Location | Index Page |
|-------------|----------|------------|
| Blog posts | `blog/[slug]/index.html` | `blog/index.html` |
| Pokemon chapters | `pokemon/[number]/index.html` | `pokemon/index.html` |
| RW episodes | `rationally-writing/[number]/index.html` | `rationally-writing/index.html` |
| Stories | Various folders | `stories/index.html` |

### Important URLs

| Purpose | URL |
|---------|-----|
| Live site | https://daystareld.com |
| GitHub repo | https://github.com/DaystarEld/daystareld.github.io |
| GitHub Pages settings | https://github.com/DaystarEld/daystareld.github.io/settings/pages |
| Giscus setup | https://giscus.app |

### Python Scripts

| Script | Purpose |
|--------|---------|
| `wordpress_parser.py` | Parse WordPress XML exports |
| `update_search_json.py` | Regenerate search index |
| `update_blog_index.py` | Update blog index page |
| `fix_pokemon_chapters.py` | Batch update Pokemon chapters |
| `add_favicon.py` | Add favicon links to all pages |
| `add_lazy_loading.py` | Add lazy loading to images |

### Git Cheat Sheet

```bash
# Daily workflow
git status                    # Check what changed
git add -A                    # Stage all changes
git commit -m "Message"       # Commit changes
git push origin main          # Push to GitHub

# Viewing history
git log --oneline -10         # Last 10 commits
git diff                      # See unstaged changes
git diff --staged             # See staged changes

# Undoing changes
git restore file.html         # Discard changes to file
git reset HEAD~1              # Undo last commit (keep changes)
git revert HEAD               # Create new commit undoing last

# Syncing
git pull origin main          # Get latest from GitHub
git fetch origin              # Check for updates
```

---

## Support & Resources

### Documentation
- **This file** - Complete site documentation
- **COMMENTING_SETUP.md** - Giscus setup guide
- **GitHub Pages Docs** - https://docs.github.com/en/pages
- **Git Documentation** - https://git-scm.com/doc

### Getting Help
- **GitHub Issues** - For bug reports
- **Git Basics** - https://git-scm.com/book/en/v2/Getting-Started-Git-Basics
- **HTML/CSS Reference** - https://developer.mozilla.org/en-US/

### Contact
- **Email:** daystar721@gmail.com
- **Website:** https://daystareld.com

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-10-15 | 1.0 | Initial documentation created |
| 2025-10-15 | 1.1 | Added commenting system documentation |

---

**End of Documentation**

*Keep this file updated as you make significant changes to the site structure or features.*

