#!/usr/bin/env python3
"""
Fix blog posts by removing WordPress block comments
"""

import re
from pathlib import Path

def clean_wordpress_blocks(content):
    """Remove WordPress block editor comments"""
    # Remove block comments like <!-- wp:paragraph -->
    content = re.sub(r'<!-- /?wp:[^>]+ -->', '', content)
    # Remove empty lines that resulted
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    return content

def fix_blog_post(html_file):
    """Fix a single blog post HTML file"""
    content = html_file.read_text(encoding='utf-8')
    
    # Find the article-content section
    match = re.search(r'(<div class="article-content">)(.*?)(</div>\s*<div class="article-footer">)', 
                     content, re.DOTALL)
    
    if match:
        before = match.group(1)
        article_content = match.group(2)
        after = match.group(3)
        
        # Clean the article content
        cleaned_content = clean_wordpress_blocks(article_content)
        
        # Rebuild the HTML
        new_content = content[:match.start()] + before + '\n' + cleaned_content + '\n            ' + after + content[match.end():]
        
        html_file.write_text(new_content, encoding='utf-8')
        return True
    return False

# Fix all blog posts
blog_dir = Path('blog')
fixed_count = 0

for post_dir in blog_dir.iterdir():
    if post_dir.is_dir():
        index_file = post_dir / 'index.html'
        if index_file.exists():
            if fix_blog_post(index_file):
                fixed_count += 1
                if fixed_count % 10 == 0:
                    print(f"Fixed {fixed_count} posts...")

print(f"\nFixed {fixed_count} blog posts total!")

