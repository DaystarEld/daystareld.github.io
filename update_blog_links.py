#!/usr/bin/env python3
"""
Update blog/index.html to add links to extracted blog posts
"""

import json
import re
from pathlib import Path

def load_blog_posts():
    """Load blog posts from manifest, excluding story chapters"""
    manifest_file = Path('blog-manifest.json')
    if not manifest_file.exists():
        print("Error: blog-manifest.json not found")
        return {}
    
    manifest = json.loads(manifest_file.read_text(encoding='utf-8'))
    
    # Filter out story chapters (pokemon, guardian, hpmor-remix, etc.)
    story_patterns = [
        r'^pokemon-\d+$',
        r'^guardian-\d+$',
        r'^hpmor-remix-\d+$',
        r'^rationally-writing-\d+$',
        r'^(hearts-and-minds|because-prophecy)$'
    ]
    
    blog_posts = {}
    for post in manifest:
        slug = post['slug']
        # Skip if it matches any story pattern
        if any(re.match(pattern, slug) for pattern in story_patterns):
            continue
        
        # Check if the directory actually exists
        post_dir = Path('blog') / slug
        if post_dir.exists():
            blog_posts[post['title']] = slug
            # Also store normalized title for fuzzy matching
            normalized = post['title'].lower().replace(':', '').replace('  ', ' ').strip()
            blog_posts[normalized] = slug
    
    return blog_posts

def normalize_title(title):
    """Normalize title for matching"""
    return title.lower().replace(':', '').replace('  ', ' ').strip()

def update_blog_index(blog_posts):
    """Update blog/index.html with links"""
    index_file = Path('blog/index.html')
    if not index_file.exists():
        print("Error: blog/index.html not found")
        return False
    
    html = index_file.read_text(encoding='utf-8')
    
    # Find all <li> items without links
    # Pattern: <li>TITLE</li> where TITLE doesn't contain <a>
    pattern = r'<li>([^<]+)</li>'
    
    def replace_if_exists(match):
        title = match.group(1).strip()
        
        # Try exact match first
        if title in blog_posts:
            slug = blog_posts[title]
            return f'<li><a href="./{slug}/">{title}</a></li>'
        
        # Try normalized match
        normalized = normalize_title(title)
        if normalized in blog_posts:
            slug = blog_posts[normalized]
            return f'<li><a href="./{slug}/">{title}</a></li>'
        
        # No match found, keep as-is
        return match.group(0)
    
    # Replace all matching items
    updated_html = re.sub(pattern, replace_if_exists, html)
    
    # Remove the migration notice
    notice_pattern = r'<div class="panel" style="background: rgba\(16, 185, 129, 0\.1\); border-color: var\(--accent\);">\s*<p[^>]*>.*?Blog post migration in progress.*?</p>\s*</div>\s*'
    updated_html = re.sub(notice_pattern, '', updated_html, flags=re.DOTALL)
    
    # Write updated HTML
    index_file.write_text(updated_html, encoding='utf-8')
    
    # Count how many links were added
    original_links = html.count('<a href=')
    new_links = updated_html.count('<a href=')
    added = new_links - original_links
    
    print(f"Updated blog/index.html:")
    print(f"  - Added {added} new links")
    print(f"  - Removed migration notice")
    
    return True

def main():
    print("Loading blog posts from manifest...")
    blog_posts = load_blog_posts()
    print(f"Found {len(set(blog_posts.values()))} unique blog posts")
    
    print("\nUpdating blog/index.html...")
    success = update_blog_index(blog_posts)
    
    if success:
        print("\n✓ Successfully updated blog index!")
    else:
        print("\n✗ Failed to update blog index")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())

