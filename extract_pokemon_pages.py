#!/usr/bin/env python3
"""
Extract Pokemon-related WordPress pages (FAQ, Team Rosters, etc.)
"""

import xml.etree.ElementTree as ET
import html
import re
from pathlib import Path

NAMESPACES = {
    'wp': 'http://wordpress.org/export/1.2/',
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'excerpt': 'http://wordpress.org/export/1.2/excerpt/',
    'dc': 'http://purl.org/dc/elements/1.1/'
}

PAGE_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Pokemon: The Origin of Species</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #0a0a0a;
            --panel: #0f0f0f;
            --text: #e5e7eb;
            --muted: #9ca3af;
            --accent: #047857;
            --accent-2: #10b981;
            --border: #1a1a1a;
            --link: #34d399;
        }}

        * {{ box-sizing: border-box; }}
        body {{
            margin: 0;
            font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
            color: var(--text);
            background: radial-gradient(1200px 800px at 80% -200px, rgba(18, 53, 36, 0.15), transparent 60%),
                        radial-gradient(900px 600px at -200px 20%, rgba(16, 185, 129, 0.08), transparent 60%),
                        var(--bg);
            line-height: 1.65;
        }}

        .container {{
            max-width: 960px;
            margin: 0 auto;
            padding: 24px;
        }}

        header {{
            position: sticky;
            top: 0;
            backdrop-filter: blur(8px);
            background: linear-gradient(to bottom, rgba(10, 10, 10, 0.85), rgba(10, 10, 10, 0.45));
            border-bottom: 1px solid var(--border);
            z-index: 10;
        }}

        .nav {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
        }}

        .brand {{
            font-weight: 800;
            letter-spacing: 0.4px;
            color: var(--text);
        }}

        .brand a {{
            color: var(--text);
            text-decoration: none;
        }}

        .brand a:hover {{
            color: var(--accent);
        }}

        nav ul {{
            display: flex;
            list-style: none;
            padding: 0;
            margin: 0;
            gap: 16px;
        }}

        nav a {{
            color: var(--text);
            padding: 8px 12px;
            border-radius: 8px;
            text-decoration: none;
        }}

        nav a:hover {{
            background: rgba(255, 255, 255, 0.06);
            text-decoration: none;
        }}

        nav a[href*="pokemon"] {{
            background: linear-gradient(90deg, var(--accent), var(--accent-2));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            font-weight: 600;
        }}

        .nav-icons {{
            display: flex;
            gap: 8px;
            align-items: center;
        }}

        .icon-button {{
            padding: 8px;
            border-radius: 8px;
            color: var(--text);
            cursor: pointer;
            text-decoration: none;
            display: flex;
            align-items: center;
            border: none;
            background: transparent;
        }}

        .icon-button:hover {{
            background: rgba(255, 255, 255, 0.06);
        }}

        #search-overlay {{
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
        }}

        .search-container {{
            width: 90%;
            max-width: 600px;
        }}

        #search-input {{
            width: 100%;
            padding: 16px 20px;
            font-size: 18px;
            background: var(--panel);
            border: 2px solid var(--border);
            border-radius: 12px;
            color: var(--text);
            font-family: inherit;
        }}

        #search-input:focus {{
            outline: none;
            border-color: var(--accent);
        }}

        #search-results {{
            margin-top: 16px;
            max-height: 50vh;
            overflow-y: auto;
        }}

        .search-result-item {{
            display: block;
            padding: 12px 16px;
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 8px;
            margin-bottom: 8px;
            color: var(--text);
            text-decoration: none;
            transition: all 0.2s;
        }}

        .search-result-item:hover {{
            border-color: var(--accent);
            transform: translateX(4px);
        }}

        .result-title {{
            font-weight: 600;
            margin-bottom: 4px;
        }}

        .result-meta {{
            font-size: 0.85em;
            color: var(--muted);
        }}

        article {{
            max-width: 720px;
            margin: 0 auto;
            padding: 40px 0;
        }}

        .page-title {{
            font-size: clamp(28px, 5vw, 44px);
            line-height: 1.15;
            margin: 0 0 32px 0;
        }}

        .page-content {{
            font-size: 1.05em;
            line-height: 1.8;
        }}

        .page-content h2 {{
            margin-top: 48px;
            margin-bottom: 16px;
            font-size: 1.8em;
        }}

        .page-content h3 {{
            margin-top: 32px;
            margin-bottom: 12px;
            font-size: 1.4em;
        }}

        .page-content p {{
            margin: 20px 0;
        }}

        .page-content a {{
            color: var(--link);
            text-decoration: underline;
            text-decoration-color: rgba(52, 211, 153, 0.3);
            text-decoration-thickness: 2px;
            text-underline-offset: 2px;
        }}

        .page-content a:hover {{
            text-decoration-color: var(--link);
        }}

        .page-content ul, .page-content ol {{
            margin: 20px 0;
            padding-left: 28px;
        }}

        .page-content li {{
            margin: 8px 0;
        }}

        .page-content img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 24px 0;
        }}

        .back-link {{
            display: inline-block;
            margin-bottom: 24px;
            color: var(--link);
            text-decoration: none;
        }}

        .back-link:hover {{
            text-decoration: underline;
        }}

        a {{ color: var(--link); text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <header>
        <div class="container nav">
            <div class="brand"><a href="/">Daystar Eld</a></div>
            <div style="display: flex; align-items: center; gap: 20px;">
            <nav aria-label="Primary">
                <ul>
                    <li><a href="/pokemon/">Pokemon: TOoS</a></li>
                    <li><a href="/rationally-writing/">Rationally Writing</a></li>
                    <li><a href="/blog/">Blog</a></li>
                    <li><a href="/stories/">Stories</a></li>
                    <li><a href="https://www.patreon.com/c/daystareld" target="_blank" rel="noopener">Support</a></li>
                </ul>
            </nav>
          <div class="nav-icons">
            <button class="icon-button" onclick="toggleSearch()" aria-label="Search">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"></circle>
                <path d="m21 21-4.35-4.35"></path>
              </svg>
            </button>
            <a href="/feed.xml" class="icon-button" aria-label="RSS Feed" target="_blank">
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
        <article>
            <a href="/pokemon/" class="back-link">← Back to Pokemon</a>
            
            <h1 class="page-title">{title}</h1>

            <div class="page-content">
{content}
            </div>
        </article>
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

    <script src="/search.js"></script>
</body>
</html>
'''

def clean_content(content):
    """Clean and format HTML content"""
    if not content:
        return ""
    
    content = html.unescape(content)
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Remove WordPress block comments
    content = re.sub(r'<!-- /?wp:[^>]+ -->', '', content)
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    # Fix WordPress image URLs
    content = content.replace('src="/wp-content/', 'src="https://daystareld.com/wp-content/')
    content = content.replace('href="/wp-content/', 'href="https://daystareld.com/wp-content/')
    
    return content

def slugify(text):
    """Convert text to URL-friendly slug"""
    text = re.sub(r'<[^>]+>', '', text)
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

# Target Pokemon-related page slugs
TARGET_SLUGS = {
    'pokemon-team-roster', 'pokemon-team-roster-ii', 'pokemon-team-roster-iii', 'pokemon-team-roster-iv',
    'the-origin-of-species-faq', 'toos-fan-art', 'pokemon-goal-factoring'
}

print("Parsing WordPress export for Pokemon pages...")
tree = ET.parse('Original files/daystareld.WordPress.2025-10-07.xml')
root = tree.getroot()
channel = root.find('channel')
items = channel.findall('item')

pokemon_pages = []

for item in items:
    post_type = item.find('wp:post_type', NAMESPACES)
    if post_type is None or post_type.text not in ['page', 'post']:
        continue
    
    status = item.find('wp:status', NAMESPACES)
    if status is None or status.text != 'publish':
        continue
    
    post_name = item.find('wp:post_name', NAMESPACES)
    if post_name is None or post_name.text not in TARGET_SLUGS:
        continue
    
    title_elem = item.find('title')
    title = title_elem.text if title_elem is not None else "Untitled"
    
    content_elem = item.find('content:encoded', NAMESPACES)
    content = content_elem.text if content_elem is not None else ""
    
    if not content or len(content.strip()) < 20:
        continue
    
    pokemon_pages.append({
        'title': title,
        'slug': post_name.text,
        'content': clean_content(content)
    })
    print(f"Found: {post_name.text}")

print(f"\nCreating {len(pokemon_pages)} Pokemon pages...")

for page in pokemon_pages:
    page_dir = Path('pokemon') / page['slug']
    page_dir.mkdir(parents=True, exist_ok=True)
    
    html_content = PAGE_TEMPLATE.format(
        title=html.escape(page['title']),
        content=page['content']
    )
    
    html_file = page_dir / 'index.html'
    html_file.write_text(html_content, encoding='utf-8')
    print(f"Created: pokemon/{page['slug']}/index.html")

print(f"\nDone! Created {len(pokemon_pages)} Pokemon-related pages.")

