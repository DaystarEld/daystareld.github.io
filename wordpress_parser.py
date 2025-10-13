#!/usr/bin/env python3
"""
WordPress XML Parser for Daystar Eld Website Migration
Extracts blog posts and generates static HTML pages
"""

import xml.etree.ElementTree as ET
import html
import re
from pathlib import Path
from datetime import datetime
import json

# WordPress XML namespaces
NAMESPACES = {
    'wp': 'http://wordpress.org/export/1.2/',
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'excerpt': 'http://wordpress.org/export/1.2/excerpt/',
    'dc': 'http://purl.org/dc/elements/1.1/'
}

# Categories to exclude (already migrated)
EXCLUDE_CATEGORIES = {
    'pokemon', 'rationally-writing', 'podcasts', 
    'hpmor-remix', 'uncategorized'
}

# HTML template for blog posts
BLOG_POST_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{excerpt}">
    <meta name="author" content="Daystar Eld">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{excerpt}">
    <meta property="og:type" content="article">
    <title>{title} - Daystar Eld</title>
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
            --phthalo: #123524;
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

        nav a[href*="pokemon"], nav a[href*="rationally-writing"] {{
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

        .article-header {{
            margin-bottom: 40px;
        }}

        .article-title {{
            font-size: clamp(28px, 5vw, 44px);
            line-height: 1.15;
            margin: 0 0 16px 0;
        }}

        .article-meta {{
            color: var(--muted);
            font-size: 0.9em;
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
        }}

        .article-meta span {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .article-content {{
            font-size: 1.05em;
            line-height: 1.8;
        }}

        .article-content h2 {{
            margin-top: 48px;
            margin-bottom: 16px;
            font-size: 1.8em;
        }}

        .article-content h3 {{
            margin-top: 32px;
            margin-bottom: 12px;
            font-size: 1.4em;
        }}

        .article-content p {{
            margin: 20px 0;
        }}

        .article-content a {{
            color: var(--link);
            text-decoration: underline;
            text-decoration-color: rgba(52, 211, 153, 0.3);
            text-decoration-thickness: 2px;
            text-underline-offset: 2px;
        }}

        .article-content a:hover {{
            text-decoration-color: var(--link);
        }}

        .article-content ul, .article-content ol {{
            margin: 20px 0;
            padding-left: 28px;
        }}

        .article-content li {{
            margin: 8px 0;
        }}

        .article-content blockquote {{
            margin: 28px 0;
            padding: 16px 24px;
            border-left: 4px solid var(--accent);
            background: rgba(4, 120, 87, 0.05);
            border-radius: 0 8px 8px 0;
        }}

        .article-content code {{
            background: var(--panel);
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.9em;
            font-family: 'Courier New', monospace;
        }}

        .article-content pre {{
            background: var(--panel);
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
            border: 1px solid var(--border);
        }}

        .article-content pre code {{
            padding: 0;
            background: none;
        }}

        .article-content img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 24px 0;
        }}

        .article-footer {{
            margin-top: 60px;
            padding-top: 24px;
            border-top: 1px solid var(--border);
        }}

        .tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 16px;
        }}

        .tag {{
            display: inline-block;
            padding: 4px 12px;
            background: rgba(4, 120, 87, 0.1);
            border: 1px solid var(--border);
            border-radius: 16px;
            font-size: 0.85em;
            color: var(--link);
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
            nav ul {{
                gap: 8px;
            }}
            
            nav a {{
                padding: 6px 10px;
                font-size: 0.9em;
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
            <a href="/blog/" class="back-link">← Back to Blog</a>
            
            <div class="article-header">
                <h1 class="article-title">{title}</h1>
                <div class="article-meta">
                    <span>
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"></circle>
                            <polyline points="12 6 12 12 16 14"></polyline>
                        </svg>
                        {date}
                    </span>
                    {categories_html}
                </div>
            </div>

            <div class="article-content">
{content}
            </div>

            <div class="article-footer">
                {tags_html}
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


def clean_html_content(content):
    """Clean and format HTML content from WordPress"""
    if not content:
        return ""
    
    # Unescape HTML entities
    content = html.unescape(content)
    
    # Fix common WordPress formatting issues
    content = content.replace('\r\n', '\n')
    content = content.replace('\r', '\n')
    
    # Remove WordPress block comments
    content = re.sub(r'<!-- /?wp:[^>]+ -->', '', content)
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    # Fix WordPress image URLs to be absolute
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
        if para.startswith(('<p>', '<div>', '<h1>', '<h2>', '<h3>', '<h4>', '<ul>', '<ol>', '<blockquote>', '<hr', '<iframe', '<img')):
            formatted_paragraphs.append(para)
        else:
            formatted_paragraphs.append(f'<p>{para}</p>')
    
    return '\n\n'.join(formatted_paragraphs)


def slugify(text):
    """Convert text to URL-friendly slug"""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Convert to lowercase
    text = text.lower()
    # Replace special characters
    text = re.sub(r'[^\w\s-]', '', text)
    # Replace whitespace with hyphens
    text = re.sub(r'[-\s]+', '-', text)
    # Remove leading/trailing hyphens
    text = text.strip('-')
    return text


def parse_wordpress_xml(xml_file):
    """Parse WordPress XML export and extract blog posts"""
    print(f"Parsing {xml_file}...")
    
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    channel = root.find('channel')
    items = channel.findall('item')
    
    blog_posts = []
    
    for item in items:
        # Extract post type
        post_type = item.find('wp:post_type', NAMESPACES)
        if post_type is None or post_type.text != 'post':
            continue
        
        # Extract status
        status = item.find('wp:status', NAMESPACES)
        if status is None or status.text != 'publish':
            continue
        
        # Extract basic info
        title = item.find('title')
        title_text = title.text if title is not None and title.text else "Untitled"
        
        # Extract categories
        categories = []
        for cat in item.findall('category[@domain="category"]'):
            if cat.text:
                categories.append(cat.text.lower())
        
        # Skip if in excluded categories
        if any(cat in EXCLUDE_CATEGORIES for cat in categories):
            continue
        
        # Extract content
        content = item.find('content:encoded', NAMESPACES)
        content_text = content.text if content is not None and content.text else ""
        
        # Skip posts with no content
        if not content_text or len(content_text.strip()) < 50:
            continue
        
        # Extract other metadata
        link = item.find('link')
        post_name = item.find('wp:post_name', NAMESPACES)
        slug = post_name.text if post_name is not None and post_name.text else slugify(title_text)
        
        # Skip Pokemon chapters (pokemon-1, pokemon-2, etc.)
        if re.match(r'^pokemon-\d+$', slug):
            continue
        
        # Skip Rationally Writing episodes (handled separately)
        if re.match(r'^rationally-writing-\d+$', slug):
            continue
        
        # Extract date
        pub_date = item.find('pubDate')
        date_str = pub_date.text if pub_date is not None else ""
        try:
            date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
            formatted_date = date_obj.strftime('%B %d, %Y')
        except:
            formatted_date = "Unknown Date"
        
        # Extract excerpt
        excerpt = item.find('excerpt:encoded', NAMESPACES)
        excerpt_text = excerpt.text if excerpt is not None and excerpt.text else ""
        if not excerpt_text:
            # Generate excerpt from content
            plain_text = re.sub(r'<[^>]+>', '', content_text)
            excerpt_text = plain_text[:200] + "..." if len(plain_text) > 200 else plain_text
        
        # Extract tags
        tags = []
        for tag in item.findall('category[@domain="post_tag"]'):
            if tag.text:
                tags.append(tag.text)
        
        blog_post = {
            'title': title_text,
            'slug': slug,
            'content': clean_html_content(content_text),
            'excerpt': excerpt_text.strip(),
            'date': formatted_date,
            'categories': categories,
            'tags': tags,
            'original_link': link.text if link is not None else ""
        }
        
        blog_posts.append(blog_post)
    
    print(f"Found {len(blog_posts)} blog posts to migrate")
    return blog_posts


def generate_blog_post_html(post):
    """Generate HTML for a single blog post"""
    # Generate categories HTML
    if post['categories']:
        cats_display = ', '.join([c.title() for c in post['categories'] if c not in EXCLUDE_CATEGORIES])
        categories_html = f'<span>📁 {cats_display}</span>' if cats_display else ''
    else:
        categories_html = ''
    
    # Generate tags HTML
    if post['tags']:
        tags_items = ''.join([f'<span class="tag">{tag}</span>' for tag in post['tags']])
        tags_html = f'<div class="tags">{tags_items}</div>'
    else:
        tags_html = ''
    
    html_content = BLOG_POST_TEMPLATE.format(
        title=html.escape(post['title']),
        excerpt=html.escape(post['excerpt']),
        date=post['date'],
        categories_html=categories_html,
        content=post['content'],
        tags_html=tags_html
    )
    
    return html_content


def create_blog_pages(blog_posts, output_dir='blog'):
    """Create individual HTML pages for each blog post"""
    output_path = Path(output_dir)
    
    created_posts = []
    
    for post in blog_posts:
        # Create directory for post
        post_dir = output_path / post['slug']
        post_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate HTML
        html_content = generate_blog_post_html(post)
        
        # Write HTML file
        html_file = post_dir / 'index.html'
        html_file.write_text(html_content, encoding='utf-8')
        
        print(f"Created: {post_dir}/index.html")
        
        created_posts.append({
            'title': post['title'],
            'slug': post['slug'],
            'excerpt': post['excerpt'],
            'date': post['date'],
            'categories': post['categories'],
            'tags': post['tags']
        })
    
    return created_posts


def update_search_json(blog_posts):
    """Update search.json with blog post entries"""
    search_file = Path('search.json')
    
    # Read existing search data
    if search_file.exists():
        try:
            search_data = json.loads(search_file.read_text(encoding='utf-8'))
        except:
            search_data = []
    else:
        search_data = []
    
    # Remove old blog entries
    search_data = [item for item in search_data if not item.get('url', '').startswith('/blog/')]
    
    # Add new blog entries
    for post in blog_posts:
        search_data.append({
            'title': post['title'],
            'url': f"/blog/{post['slug']}/",
            'type': 'Blog Post',
            'excerpt': post['excerpt']
        })
    
    # Write updated search data
    search_file.write_text(json.dumps(search_data, indent=2), encoding='utf-8')
    print(f"Updated search.json with {len(blog_posts)} blog posts")


def main():
    """Main execution function"""
    xml_file = 'Original files/daystareld.WordPress.2025-10-07.xml'
    
    # Parse WordPress XML
    blog_posts = parse_wordpress_xml(xml_file)
    
    if not blog_posts:
        print("No blog posts found to migrate!")
        return
    
    # Create blog post pages
    print("\nCreating blog post pages...")
    created_posts = create_blog_pages(blog_posts)
    
    # Update search.json
    print("\nUpdating search index...")
    update_search_json(created_posts)
    
    # Save post manifest
    manifest_file = Path('blog-manifest.json')
    manifest_file.write_text(json.dumps(created_posts, indent=2), encoding='utf-8')
    print(f"\nSaved blog manifest to {manifest_file}")
    
    print(f"\nSuccessfully migrated {len(created_posts)} blog posts!")
    print("\nNext steps:")
    print("1. Update blog/index.html with links to these posts")
    print("2. Review generated pages for formatting issues")
    print("3. Commit changes to Git")


if __name__ == '__main__':
    main()

