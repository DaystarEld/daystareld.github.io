#!/usr/bin/env python3
"""
Update search.json with blog post entries (excluding story chapters)
"""

import json
import re
from pathlib import Path

def main():
    manifest_file = Path('blog-manifest.json')
    search_file = Path('search.json')
    
    # Load manifest
    if not manifest_file.exists():
        print("Error: blog-manifest.json not found")
        return 1
    
    manifest = json.loads(manifest_file.read_text(encoding='utf-8'))
    
    # Load existing search data
    if search_file.exists():
        try:
            search_data = json.loads(search_file.read_text(encoding='utf-8'))
        except:
            search_data = []
    else:
        search_data = []
    
    # Filter out story chapters
    story_patterns = [
        r'^pokemon-\d+$',
        r'^guardian-\d+$',
        r'^hpmor-remix-\d+$',
        r'^rationally-writing-\d+$',
        r'^(hearts-and-minds|because-prophecy)$'
    ]
    
    # Remove old blog entries from search
    search_data = [item for item in search_data if not (
        item.get('url', '').startswith('/blog/') and 
        item.get('type') == 'Blog Post'
    )]
    
    # Add new blog entries (only those that exist)
    added = 0
    for post in manifest:
        slug = post['slug']
        
        # Skip story chapters
        if any(re.match(pattern, slug) for pattern in story_patterns):
            continue
        
        # Check if directory exists
        post_dir = Path('blog') / slug
        if not post_dir.exists():
            continue
        
        search_data.append({
            'title': post['title'],
            'url': f"/blog/{slug}/",
            'type': 'Blog Post',
            'excerpt': post.get('excerpt', '')[:200]
        })
        added += 1
    
    # Write updated search data
    search_file.write_text(json.dumps(search_data, indent=2), encoding='utf-8')
    print(f"Updated search.json: added {added} blog posts")
    
    return 0

if __name__ == '__main__':
    exit(main())

