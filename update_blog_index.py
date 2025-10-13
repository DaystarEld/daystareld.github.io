#!/usr/bin/env python3
"""
Update blog/index.html with proper links to all migrated blog posts
"""

import json
from pathlib import Path
from collections import defaultdict

# Load blog manifest
with open('blog-manifest.json', 'r', encoding='utf-8') as f:
    all_posts = json.load(f)

# Filter out Pokemon chapters, Rationally Writing, stories (they have their own pages)
EXCLUDE_SLUGS = {'hpmor-remix', 'rationally-writing', 'guardian', 'because-prophecy', 'hearts-and-minds'}

blog_posts = []
for post in all_posts:
    slug = post['slug']
    categories = post.get('categories', [])
    
    # Skip Pokemon chapters
    if slug.startswith('pokemon-') and slug[8:].isdigit():
        continue
    
    # Skip if in excluded categories
    if any(cat in ['pokemon: the origin of species', 'rationally-writing', 'hpmor-remix'] for cat in categories):
        continue
    
    # Skip if slug matches excluded  
    if any(slug.startswith(exc) for exc in EXCLUDE_SLUGS):
        continue
    
    blog_posts.append(post)

print(f"Found {len(blog_posts)} actual blog posts (filtered from {len(all_posts)} total)")

# Organize posts by category
category_map = {
    'personal': 'Personal',
    'therapy-and-psychology': 'Therapy and Psychology', 
    'romantic-relationships': 'Romantic Relationships',
    'knowledge-and-epistemology': 'Knowledge and Epistemology',
    'politics-and-society-articles': 'Politics and Society',
    'storytelling': 'Storytelling',
    'game-reviews': 'Game Reviews',
    'book-reviews': 'Book Reviews',
    'movie-reviews': 'Movie Reviews',
    'blog': 'General'
}

# Group posts by primary category
categorized_posts = defaultdict(list)

for post in blog_posts:
    categories = post.get('categories', [])
    
    # Determine primary category
    primary_cat = 'General'
    
    if 'therapy-and-psychology' in categories or 'therapy and psychology' in categories:
        primary_cat = 'Therapy and Psychology'
    elif 'romantic-relationships' in categories or 'romantic relationships' in categories:
        primary_cat = 'Romantic Relationships'
    elif 'knowledge-and-epistemology' in categories or 'knowledge and epistemology' in categories:
        primary_cat = 'Knowledge and Epistemology'
    elif 'politics-and-society-articles' in categories or 'politics and society' in categories:
        primary_cat = 'Politics and Society'
    elif 'storytelling' in categories:
        primary_cat = 'Storytelling'
    elif 'game-reviews' in categories or 'game reviews' in categories or 'games' in categories:
        primary_cat = 'Game Reviews'
    elif 'book-reviews' in categories or 'book reviews' in categories:
        primary_cat = 'Book Reviews'
    elif 'movie-reviews' in categories or 'movie reviews' in categories:
        primary_cat = 'Movie Reviews'
    elif 'personal' in categories:
        primary_cat = 'Personal'
    
    categorized_posts[primary_cat].append(post)

# Generate HTML for each category section
html_sections = []

category_order = [
    'Personal',
    'Therapy and Psychology',
    'Romantic Relationships',
    'Knowledge and Epistemology',
    'Politics and Society',
    'Storytelling',
    'Game Reviews',
    'Book Reviews',
    'Movie Reviews',
    'General'
]

for category in category_order:
    posts = categorized_posts.get(category, [])
    if not posts:
        continue
    
    # Sort by title
    posts.sort(key=lambda p: p['title'])
    
    # Generate list items
    list_items = '\n'.join([
        f'                <li><a href="/blog/{post["slug"]}/">{post["title"]}</a></li>'
        for post in posts
    ])
    
    html_section = f'''        <div class="panel">
            <h2>{category}</h2>
            <ul>
{list_items}
            </ul>
        </div>'''
    
    html_sections.append(html_section)

# Build the complete blog index HTML
blog_index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog - Daystar</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0a0a0a;
            --panel: #0f0f0f;
            --text: #e5e7eb;
            --muted: #9ca3af;
            --accent: #047857;
            --accent-2: #10b981;
            --border: #1a1a1a;
            --link: #34d399;
            --phthalo: #123524;
        }

        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
            color: var(--text);
            background: radial-gradient(1200px 800px at 80% -200px, rgba(18, 53, 36, 0.15), transparent 60%),
                        radial-gradient(900px 600px at -200px 20%, rgba(16, 185, 129, 0.08), transparent 60%),
                        var(--bg);
            line-height: 1.65;
        }

        .container {
            max-width: 960px;
            margin: 0 auto;
            padding: 24px;
        }

        header {
            position: sticky;
            top: 0;
            backdrop-filter: blur(8px);
            background: linear-gradient(to bottom, rgba(10, 10, 10, 0.85), rgba(10, 10, 10, 0.45));
            border-bottom: 1px solid var(--border);
            z-index: 10;
        }

        .nav {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
        }

        .brand {
            font-weight: 800;
            letter-spacing: 0.4px;
            color: var(--text);
        }

        .brand a {
            color: var(--text);
            text-decoration: none;
        }

        .brand a:hover {
            color: var(--accent);
        }

        nav ul {
            display: flex;
            list-style: none;
            padding: 0;
            margin: 0;
            gap: 16px;
        }

        nav a {
            color: var(--text);
            padding: 8px 12px;
            border-radius: 8px;
            text-decoration: none;
        }

        nav a:hover {
            background: rgba(255, 255, 255, 0.06);
            text-decoration: none;
        }

        nav a[href*="pokemon"], nav a[href*="rationally-writing"] {
            background: linear-gradient(90deg, var(--accent), var(--accent-2));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            font-weight: 600;
        }

  
      .nav-icons {
        display: flex;
        gap: 8px;
        align-items: center;
      }

      .icon-button {
        padding: 8px;
        border-radius: 8px;
        color: var(--text);
        cursor: pointer;
        text-decoration: none;
        display: flex;
        align-items: center;
        border: none;
        background: transparent;
      }

      .icon-button:hover {
        background: rgba(255, 255, 255, 0.06);
      }

      #search-overlay {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(10, 10, 10, 0.95);
        backdrop-filter: blur(8px);
        z-index: 1000;
        align-items: flex-start;
        justify-content: center;
        padding-top: 20vh;
      }

      .search-container {
        width: 90%;
        max-width: 600px;
      }

      #search-input {
        width: 100%;
        padding: 16px 20px;
        font-size: 18px;
        background: var(--panel);
        border: 2px solid var(--border);
        border-radius: 12px;
        color: var(--text);
        font-family: inherit;
      }

      #search-input:focus {
        outline: none;
        border-color: var(--accent);
      }

      #search-results {
        margin-top: 16px;
        max-height: 50vh;
        overflow-y: auto;
      }

      .search-result-item {
        display: block;
        padding: 12px 16px;
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 8px;
        margin-bottom: 8px;
        color: var(--text);
        text-decoration: none;
        transition: all 0.2s;
      }

      .search-result-item:hover {
        border-color: var(--accent);
        transform: translateX(4px);
      }

      .result-title {
        font-weight: 600;
        margin-bottom: 4px;
      }

      .result-meta {
        font-size: 0.85em;
        color: var(--muted);
      }

      .hero {
            padding: 40px 0 20px;
        }

        .title {
            font-size: clamp(28px, 5vw, 44px);
            line-height: 1.15;
            margin: 0 0 12px 0;
        }

        .title .accent {
            background: linear-gradient(90deg, var(--accent), var(--accent-2));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }

        .subtitle {
            color: var(--muted);
            margin: 0;
            max-width: 60ch;
        }

        .panel {
            background: linear-gradient(to bottom right, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 20px;
            margin: 20px 0;
        }

        .panel ul {
            columns: 2;
            column-gap: 30px;
        }

        .panel ul li {
            break-inside: avoid;
            margin-bottom: 8px;
        }

        @media (max-width: 768px) {
            .panel ul {
                columns: 1;
            }
        }

        /* Sidebar support for future use */
        .full-width {
            max-width: none;
            margin: 0;
            padding: 0;
        }

        .main-content-full {
            display: grid;
            grid-template-columns: 680px 300px;
            gap: 24px;
            max-width: 960px;
            margin: 0 auto;
            padding: 0 24px 24px 24px;
            align-items: start;
            justify-content: space-between;
        }

        .content-main {
            min-width: 0;
            margin-left: auto;
            margin-right: auto;
        }

        @media (max-width: 1200px) {
            .main-content-full {
                grid-template-columns: 1fr 300px;
                gap: 24px;
            }
        }

        .sidebar {
            background: linear-gradient(to bottom right, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 20px;
            font-size: 0.9em;
            line-height: 1.6;
        }

        @media (max-width: 968px) {
            .main-content-full {
                grid-template-columns: 1fr;
            }
        }

        a { color: var(--link); text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <header>
        <div class="container nav">
            <div class="brand"><a href="../">Daystar Eld</a></div>
            <div style="display: flex; align-items: center; gap: 20px;">
            <nav aria-label="Primary">
                <ul>
                    <li><a href="../pokemon/">Pokemon: TOoS</a></li>
                    <li><a href="../rationally-writing/">Rationally Writing</a></li>
                    <li><a href="../stories/">Stories</a></li>
                    <li><a href="https://www.patreon.com/c/daystareld" target="_blank" rel="noopener">Support</a></li>
          <div class="nav-icons">
            <button class="icon-button" onclick="toggleSearch()" aria-label="Search">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"></circle>
                <path d="m21 21-4.35-4.35"></path>
              </svg>
            </button>
            <a href="../feed.xml" class="icon-button" aria-label="RSS Feed" target="_blank">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 11a9 9 0 0 1 9 9"></path>
                <path d="M4 4a16 16 0 0 1 16 16"></path>
                <circle cx="5" cy="19" r="1"></circle>
              </svg>
            </a>
          </div>
        </div>
        </div>
    </header>

    <main class="container">
        <section class="hero">
            <h1 class="title">Blog & <span class="accent">Reviews</span></h1>
            <p class="subtitle">Essays on therapy, psychology, epistemology, and occasionally other things.</p>
        </section>

''' + '\n\n'.join(html_sections) + '''
    </main>

    <!-- Search Overlay -->
    <div id="search-overlay" onclick="if(event.target.id === 'search-overlay') toggleSearch()">
      <div class="search-container">
        <input 
          type="text" 
          id="search-input" 
          placeholder="Search chapters, episodes, and pages..."
          oninput="performSearch(this.value)"
          autocomplete="off"
        />
        <div id="search-results"></div>
      </div>
    </div>

    <script src="../search.js"></script>
</body>
</html>
'''

# Write the updated blog index
blog_index_path = Path('blog/index.html')
blog_index_path.write_text(blog_index_html, encoding='utf-8')
print(f"\nUpdated {blog_index_path} with {len(blog_posts)} blog post links!")
print(f"\nCategories:")
for category in category_order:
    count = len(categorized_posts.get(category, []))
    if count > 0:
        print(f"  - {category}: {count} posts")

