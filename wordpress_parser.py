#!/usr/bin/env python3
"""
WordPress XML Export Parser
Extracts and organizes content from WordPress XML export files
"""

import xml.etree.ElementTree as ET
import os
import re
from datetime import datetime
from pathlib import Path
import html
from urllib.parse import unquote
import json

class WordPressParser:
    def __init__(self, xml_file_path):
        self.xml_file_path = xml_file_path
        self.tree = None
        self.root = None
        self.posts = []
        self.pages = []
        self.attachments = []
        self.categories = {}
        self.tags = {}
        self.authors = {}
        
    def parse_xml(self):
        """Parse the WordPress XML file"""
        print(f"Parsing WordPress XML file: {self.xml_file_path}")
        
        try:
            self.tree = ET.parse(self.xml_file_path)
            self.root = self.tree.getroot()
            
            # Find the channel element
            channel = self.root.find('channel')
            if channel is None:
                raise ValueError("No channel element found in XML file")
            
            # Parse metadata
            self._parse_categories(channel)
            self._parse_tags(channel)
            self._parse_authors(channel)
            
            # Parse content
            self._parse_posts(channel)
            self._parse_pages(channel)
            self._parse_attachments(channel)
            
            print(f"Parsing complete!")
            print(f"- Categories: {len(self.categories)}")
            print(f"- Tags: {len(self.tags)}")
            print(f"- Authors: {len(self.authors)}")
            print(f"- Posts: {len(self.posts)}")
            print(f"- Pages: {len(self.pages)}")
            print(f"- Attachments: {len(self.attachments)}")
            
        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False
            
        return True
    
    def _parse_categories(self, channel):
        """Parse categories from XML"""
        for item in channel.findall('item'):
            if item.find('wp:post_type', {'wp': 'http://wordpress.org/export/1.2/'}) is not None:
                continue  # Skip non-taxonomy items
                
            taxonomy = item.find('wp:post_type', {'wp': 'http://wordpress.org/export/1.2/'})
            if taxonomy is None or taxonomy.text == 'category':
                title = item.find('title').text
                term_id = item.find('wp:term_id', {'wp': 'http://wordpress.org/export/1.2/'}).text
                self.categories[term_id] = title
    
    def _parse_tags(self, channel):
        """Parse tags from XML"""
        for item in channel.findall('item'):
            taxonomy = item.find('wp:post_type', {'wp': 'http://wordpress.org/export/1.2/'})
            if taxonomy is None or taxonomy.text == 'post_tag':
                title = item.find('title').text
                term_id = item.find('wp:term_id', {'wp': 'http://wordpress.org/export/1.2/'}).text
                self.tags[term_id] = title
    
    def _parse_authors(self, channel):
        """Parse authors from XML"""
        for item in channel.findall('item'):
            taxonomy = item.find('wp:post_type', {'wp': 'http://wordpress.org/export/1.2/'})
            if taxonomy is None or taxonomy.text == 'author':
                login = item.find('wp:post_name', {'wp': 'http://wordpress.org/export/1.2/'}).text
                display_name = item.find('title').text
                email = item.find('wp:author_email', {'wp': 'http://wordpress.org/export/1.2/'})
                email = email.text if email is not None else ""
                self.authors[login] = {'display_name': display_name, 'email': email}
    
    def _parse_posts(self, channel):
        """Parse blog posts from XML"""
        for item in channel.findall('item'):
            post_type = item.find('wp:post_type', {'wp': 'http://wordpress.org/export/1.2/'})
            if post_type is None or post_type.text != 'post':
                continue
                
            post_data = self._extract_post_data(item)
            if post_data:
                self.posts.append(post_data)
    
    def _parse_pages(self, channel):
        """Parse pages from XML"""
        for item in channel.findall('item'):
            post_type = item.find('wp:post_type', {'wp': 'http://wordpress.org/export/1.2/'})
            if post_type is None or post_type.text != 'page':
                continue
                
            post_data = self._extract_post_data(item)
            if post_data:
                self.pages.append(post_data)
    
    def _parse_attachments(self, channel):
        """Parse attachments from XML"""
        for item in channel.findall('item'):
            post_type = item.find('wp:post_type', {'wp': 'http://wordpress.org/export/1.2/'})
            if post_type is None or post_type.text != 'attachment':
                continue
                
            post_data = self._extract_post_data(item)
            if post_data:
                self.attachments.append(post_data)
    
    def _extract_post_data(self, item):
        """Extract post data from XML item"""
        try:
            # Basic post data
            title = item.find('title').text or "Untitled"
            content = item.find('{http://purl.org/rss/1.0/modules/content/}encoded')
            content = content.text if content is not None else ""
            
            # WordPress specific data
            post_id = item.find('wp:post_id', {'wp': 'http://wordpress.org/export/1.2/'})
            post_id = post_id.text if post_id is not None else ""
            
            post_date = item.find('wp:post_date', {'wp': 'http://wordpress.org/export/1.2/'})
            post_date = post_date.text if post_date is not None else ""
            
            post_status = item.find('wp:status', {'wp': 'http://wordpress.org/export/1.2/'})
            post_status = post_status.text if post_status is not None else ""
            
            post_name = item.find('wp:post_name', {'wp': 'http://wordpress.org/export/1.2/'})
            post_name = post_name.text if post_name is not None else ""
            
            post_type = item.find('wp:post_type', {'wp': 'http://wordpress.org/export/1.2/'})
            post_type = post_type.text if post_type is not None else ""
            
            author = item.find('{http://purl.org/dc/elements/1.1/}creator')
            author = author.text if author is not None else ""
            
            # Extract categories and tags
            categories = []
            tags = []
            
            for category in item.findall('category'):
                domain = category.get('domain', '')
                term_id = category.get('{http://wordpress.org/export/1.2/}term_id')
                
                if domain == 'category' and term_id in self.categories:
                    categories.append(self.categories[term_id])
                elif domain == 'post_tag' and term_id in self.tags:
                    tags.append(self.tags[term_id])
            
            # Extract excerpt
            excerpt = item.find('{http://wordpress.org/export/1.2/excerpt/}encoded')
            excerpt = excerpt.text if excerpt is not None else ""
            
            return {
                'id': post_id,
                'title': title,
                'content': content,
                'excerpt': excerpt,
                'post_date': post_date,
                'post_name': post_name,
                'post_type': post_type,
                'post_status': post_status,
                'author': author,
                'categories': categories,
                'tags': tags
            }
            
        except Exception as e:
            print(f"Error extracting post data: {e}")
            return None
    
    def categorize_content(self):
        """Categorize content by type and themes"""
        categorized = {
            'blog_posts': [],
            'fiction_posts': [],
            'podcast_posts': [],
            'other_posts': [],
            'pages': [],
            'attachments': []
        }
        
        # Categorize posts
        for post in self.posts:
            title_lower = post['title'].lower()
            content_lower = post['content'].lower()
            categories_lower = [cat.lower() for cat in post['categories']]
            
            # Determine content type based on categories, tags, or content
            if any(keyword in title_lower or keyword in content_lower or keyword in categories_lower 
                   for keyword in ['fiction', 'story', 'chapter', 'novel', 'tale']):
                categorized['fiction_posts'].append(post)
            elif any(keyword in title_lower or keyword in content_lower or keyword in categories_lower 
                     for keyword in ['podcast', 'episode', 'audio', 'interview']):
                categorized['podcast_posts'].append(post)
            elif any(keyword in title_lower or keyword in content_lower or keyword in categories_lower 
                     for keyword in ['blog', 'thoughts', 'opinion', 'review', 'tutorial']):
                categorized['blog_posts'].append(post)
            else:
                categorized['other_posts'].append(post)
        
        # Add pages and attachments
        categorized['pages'] = self.pages
        categorized['attachments'] = self.attachments
        
        return categorized
    
    def generate_html_output(self, output_dir='wordpress_content'):
        """Generate HTML files for each category"""
        Path(output_dir).mkdir(exist_ok=True)
        
        categorized = self.categorize_content()
        
        # Generate index page
        self._generate_index_html(output_dir, categorized)
        
        # Generate category pages
        for category, posts in categorized.items():
            if posts:  # Only create files for categories with content
                self._generate_category_html(output_dir, category, posts)
        
        # Generate individual post pages
        self._generate_individual_posts(output_dir, categorized)
        
        print(f"HTML files generated in '{output_dir}' directory")
    
    def _generate_index_html(self, output_dir, categorized):
        """Generate main index page"""
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WordPress Content Archive</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
        .header { border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }
        .category { margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
        .category h2 { color: #333; margin-top: 0; }
        .post-list { list-style: none; padding: 0; }
        .post-list li { margin: 10px 0; padding: 10px; background: #f9f9f9; border-radius: 4px; }
        .post-list a { text-decoration: none; color: #0066cc; }
        .post-list a:hover { text-decoration: underline; }
        .meta { color: #666; font-size: 0.9em; }
        .stats { background: #e8f4f8; padding: 15px; border-radius: 8px; margin-bottom: 30px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>WordPress Content Archive</h1>
        <p>Extracted and organized from WordPress export</p>
    </div>
    
    <div class="stats">
        <h3>Content Statistics</h3>
        <ul>
"""
        
        for category, posts in categorized.items():
            if posts:
                category_name = category.replace('_', ' ').title()
                html_content += f"            <li>{category_name}: {len(posts)} items</li>\n"
        
        html_content += """        </ul>
    </div>
"""
        
        for category, posts in categorized.items():
            if posts:
                category_name = category.replace('_', ' ').title()
                html_content += f"""
    <div class="category">
        <h2><a href="{category}.html">{category_name}</a></h2>
        <p>{len(posts)} items</p>
        <ul class="post-list">
"""
                
                # Show first 5 items as preview
                for post in posts[:5]:
                    date_str = post['post_date'][:10] if post['post_date'] else 'No date'
                    html_content += f"""
            <li>
                <a href="posts/{post['id']}.html">{post['title']}</a>
                <div class="meta">{date_str} | {post['author']}</div>
            </li>"""
                
                if len(posts) > 5:
                    html_content += f"""
            <li><em>... and {len(posts) - 5} more items</em></li>"""
                
                html_content += """
        </ul>
    </div>"""
        
        html_content += """
</body>
</html>"""
        
        with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _generate_category_html(self, output_dir, category, posts):
        """Generate HTML page for a specific category"""
        category_name = category.replace('_', ' ').title()
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{category_name} - WordPress Archive</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        .header {{ border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }}
        .post-list {{ list-style: none; padding: 0; }}
        .post-item {{ margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }}
        .post-title {{ color: #333; margin-top: 0; }}
        .post-title a {{ text-decoration: none; color: #0066cc; }}
        .post-title a:hover {{ text-decoration: underline; }}
        .post-meta {{ color: #666; font-size: 0.9em; margin-bottom: 10px; }}
        .post-excerpt {{ margin-top: 10px; }}
        .back-link {{ margin-bottom: 20px; }}
    </style>
</head>
<body>
    <div class="back-link">
        <a href="index.html">← Back to Archive</a>
    </div>
    
    <div class="header">
        <h1>{category_name}</h1>
        <p>{len(posts)} items</p>
    </div>
    
    <ul class="post-list">
"""
        
        for post in posts:
            date_str = post['post_date'][:10] if post['post_date'] else 'No date'
            categories_str = ', '.join(post['categories']) if post['categories'] else 'Uncategorized'
            
            html_content += f"""
        <li class="post-item">
            <h2 class="post-title">
                <a href="posts/{post['id']}.html">{post['title']}</a>
            </h2>
            <div class="post-meta">
                {date_str} | {post['author']} | {categories_str}
            </div>
            <div class="post-excerpt">
                {post['excerpt'][:200] if post['excerpt'] else 'No excerpt available'}...
            </div>
        </li>"""
        
        html_content += """
    </ul>
</body>
</html>"""
        
        with open(os.path.join(output_dir, f'{category}.html'), 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _generate_individual_posts(self, output_dir, categorized):
        """Generate individual HTML files for each post"""
        posts_dir = os.path.join(output_dir, 'posts')
        Path(posts_dir).mkdir(exist_ok=True)
        
        all_posts = []
        for posts in categorized.values():
            if isinstance(posts, list):
                all_posts.extend(posts)
        
        for post in all_posts:
            date_str = post['post_date'][:10] if post['post_date'] else 'No date'
            categories_str = ', '.join(post['categories']) if post['categories'] else 'Uncategorized'
            tags_str = ', '.join(post['tags']) if post['tags'] else ''
            
            # Clean and format content
            content = self._clean_html_content(post['content'])
            
            html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{post['title']} - WordPress Archive</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; max-width: 800px; }}
        .header {{ border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }}
        .post-meta {{ color: #666; font-size: 0.9em; margin-bottom: 20px; }}
        .post-content {{ margin-top: 20px; }}
        .back-link {{ margin-bottom: 20px; }}
    </style>
</head>
<body>
    <div class="back-link">
        <a href="../index.html">← Back to Archive</a>
    </div>
    
    <div class="header">
        <h1>{post['title']}</h1>
        <div class="post-meta">
            <strong>Date:</strong> {date_str}<br>
            <strong>Author:</strong> {post['author']}<br>
            <strong>Categories:</strong> {categories_str}<br>
"""
            
            if tags_str:
                html_content += f'            <strong>Tags:</strong> {tags_str}<br>\n'
            
            html_content += f"""        </div>
    </div>
    
    <div class="post-content">
        {content}
    </div>
</body>
</html>"""
            
            with open(os.path.join(posts_dir, f"{post['id']}.html"), 'w', encoding='utf-8') as f:
                f.write(html_content)
    
    def _clean_html_content(self, content):
        """Clean and format HTML content"""
        if not content:
            return "<p>No content available.</p>"
        
        # Decode HTML entities
        content = html.unescape(content)
        
        # Basic cleaning - you might want to add more sophisticated cleaning
        content = content.replace('\n', '<br>\n')
        
        return content
    
    def export_to_json(self, output_file='wordpress_content.json'):
        """Export all content to JSON format"""
        categorized = self.categorize_content()
        
        export_data = {
            'metadata': {
                'export_date': datetime.now().isoformat(),
                'source_file': self.xml_file_path,
                'total_categories': len(self.categories),
                'total_tags': len(self.tags),
                'total_authors': len(self.authors),
                'total_posts': len(self.posts),
                'total_pages': len(self.pages),
                'total_attachments': len(self.attachments)
            },
            'categories': self.categories,
            'tags': self.tags,
            'authors': self.authors,
            'content': categorized
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"Content exported to JSON: {output_file}")


def main():
    """Main function to run the parser"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python wordpress_parser.py <wordpress_export.xml>")
        print("Example: python wordpress_parser.py wordpress-export-2024-01-01.xml")
        return
    
    xml_file = sys.argv[1]
    
    if not os.path.exists(xml_file):
        print(f"Error: File '{xml_file}' not found.")
        return
    
    # Create parser and parse XML
    parser = WordPressParser(xml_file)
    
    if not parser.parse_xml():
        print("Failed to parse XML file.")
        return
    
    # Generate outputs
    print("\nGenerating HTML output...")
    parser.generate_html_output()
    
    print("\nExporting to JSON...")
    parser.export_to_json()
    
    print("\nWordPress content extraction complete!")
    print("Check the 'wordpress_content' directory for organized HTML files.")
    print("Check 'wordpress_content.json' for raw data export.")


if __name__ == "__main__":
    main()


