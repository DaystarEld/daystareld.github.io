#!/usr/bin/env python3
"""
Extract Pokemon chapters from WordPress export and place them in correct directories
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

CHAPTER_TEMPLATE = '''<!DOCTYPE html>
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
            max-width: 800px;
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

        .chapter-title {{
            font-size: clamp(28px, 5vw, 44px);
            line-height: 1.15;
            margin: 0 0 32px 0;
        }}

        .chapter-nav {{
            display: flex;
            justify-content: space-between;
            gap: 16px;
            margin-bottom: 32px;
            flex-wrap: wrap;
        }}

        .chapter-nav a {{
            color: var(--link);
            text-decoration: none;
            padding: 8px 16px;
            border: 1px solid var(--border);
            border-radius: 8px;
            background: linear-gradient(to bottom right, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
        }}

        .chapter-nav a:hover {{
            border-color: var(--accent);
            text-decoration: none;
        }}

        .chapter-content {{
            font-size: 1.05em;
            line-height: 1.8;
        }}

        .chapter-content h2 {{
            margin-top: 48px;
            margin-bottom: 16px;
            font-size: 1.8em;
        }}

        .chapter-content h3 {{
            margin-top: 32px;
            margin-bottom: 12px;
            font-size: 1.4em;
        }}

        .chapter-content p {{
            margin: 20px 0;
        }}

        .chapter-content a {{
            color: var(--link);
            text-decoration: underline;
            text-decoration-color: rgba(52, 211, 153, 0.3);
            text-decoration-thickness: 2px;
            text-underline-offset: 2px;
        }}

        .chapter-content a:hover {{
            text-decoration-color: var(--link);
        }}

        .chapter-content ul, .chapter-content ol {{
            margin: 20px 0;
            padding-left: 28px;
        }}

        .chapter-content li {{
            margin: 8px 0;
        }}

        .chapter-content img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 24px 0;
        }}

        .chapter-content em {{
            font-style: italic;
            color: var(--muted);
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

        @media (max-width: 768px) {{
            .chapter-nav {{
                flex-direction: column;
            }}
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
            
            <nav class="chapter-nav">
                {prev_link}
                <a href="/pokemon/">Table of Contents</a>
                {next_link}
            </nav>

            <h1 class="chapter-title">{title}</h1>

            <div class="chapter-content">
{content}
            </div>

            <nav class="chapter-nav">
                {prev_link}
                <a href="/pokemon/">Table of Contents</a>
                {next_link}
            </nav>
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
    
    # Convert plain text paragraphs to HTML
    # Split by double newlines (paragraph breaks)
    paragraphs = content.split('\n\n')
    
    # Wrap each paragraph in <p> tags, but skip if it already has block-level HTML tags
    formatted_paragraphs = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        # Check if paragraph already has block-level tags
        if para.startswith(('<p>', '<div>', '<h1>', '<h2>', '<h3>', '<h4>', '<ul>', '<ol>', '<blockquote>', '<hr')):
            formatted_paragraphs.append(para)
        else:
            formatted_paragraphs.append(f'<p>{para}</p>')
    
    return '\n\n'.join(formatted_paragraphs)

print("Parsing WordPress export for Pokemon chapters...")
tree = ET.parse('Original files/daystareld.WordPress.2025-10-07.xml')
root = tree.getroot()
channel = root.find('channel')
items = channel.findall('item')

pokemon_chapters = []

for item in items:
    post_type = item.find('wp:post_type', NAMESPACES)
    if post_type is None or post_type.text not in ['post']:
        continue
    
    status = item.find('wp:status', NAMESPACES)
    if status is None or status.text != 'publish':
        continue
    
    post_name = item.find('wp:post_name', NAMESPACES)
    slug = post_name.text if post_name is not None else ""
    
    # Check if it's a Pokemon chapter
    if slug.startswith('pokemon-') and slug[8:].replace('-', '').isdigit():
        match = re.match(r'pokemon-(\d+)', slug)
        if match:
            chapter_num = int(match.group(1))
            
            title_elem = item.find('title')
            title = title_elem.text if title_elem is not None else "Untitled"
            
            content_elem = item.find('content:encoded', NAMESPACES)
            content = content_elem.text if content_elem is not None else ""
            
            if content and len(content.strip()) > 20:
                pokemon_chapters.append({
                    'chapter_num': chapter_num,
                    'title': title,
                    'slug': slug,
                    'content': clean_content(content)
                })

# Sort by chapter number
pokemon_chapters.sort(key=lambda x: x['chapter_num'])

print(f"Found {len(pokemon_chapters)} Pokemon chapters")
print("Creating chapter HTML files...")

for chapter in pokemon_chapters:
    num = chapter['chapter_num']
    
    # Create navigation links
    prev_link = f'<a href="/pokemon/{num-1}/">← Previous</a>' if num > 1 else '<span></span>'
    next_link = f'<a href="/pokemon/{num+1}/">Next →</a>' if num < len(pokemon_chapters) else '<span></span>'
    
    # Generate HTML
    html_content = CHAPTER_TEMPLATE.format(
        title=html.escape(chapter['title']),
        content=chapter['content'],
        prev_link=prev_link,
        next_link=next_link
    )
    
    # Create directory and write file
    chapter_dir = Path('pokemon') / str(num)
    chapter_dir.mkdir(parents=True, exist_ok=True)
    
    html_file = chapter_dir / 'index.html'
    html_file.write_text(html_content, encoding='utf-8')
    
    if num % 20 == 0:
        print(f"  Created chapters 1-{num}...")

print(f"\nDone! Created {len(pokemon_chapters)} Pokemon chapter pages.")
print("All chapters are now in the correct directories!")

