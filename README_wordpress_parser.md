# WordPress XML Parser

This tool extracts and organizes content from WordPress XML export files, separating your blog posts, fiction, podcasts, and other content into organized categories.

## Features

- **Automatic Content Categorization**: Intelligently categorizes content based on titles, categories, and content
- **Multiple Output Formats**: Generates both HTML and JSON outputs
- **Organized Structure**: Creates separate files for different content types
- **Clean HTML Output**: Generates clean, readable HTML files for each post
- **Comprehensive Metadata**: Preserves author, date, categories, and tags information

## Usage

1. **Place your WordPress XML export file** in the same directory as this script
2. **Run the parser**:
   ```bash
   python wordpress_parser.py your-wordpress-export.xml
   ```

## Output Structure

The parser creates the following structure:

```
wordpress_content/
├── index.html              # Main archive page
├── blog_posts.html         # Blog posts category
├── fiction_posts.html      # Fiction content category  
├── podcast_posts.html      # Podcast episodes category
├── other_posts.html        # Uncategorized posts
├── pages.html              # Static pages
└── posts/                  # Individual post files
    ├── 123.html
    ├── 124.html
    └── ...
```

## Content Categories

The parser automatically categorizes content based on:

- **Fiction Posts**: Contains keywords like "fiction", "story", "chapter", "novel", "tale"
- **Podcast Posts**: Contains keywords like "podcast", "episode", "audio", "interview"  
- **Blog Posts**: Contains keywords like "blog", "thoughts", "opinion", "review", "tutorial"
- **Other Posts**: Content that doesn't match the above categories

## JSON Export

The parser also creates a `wordpress_content.json` file containing:
- All extracted content in structured format
- Metadata about the export
- Categories, tags, and author information
- Raw post data for further processing

## Customization

You can modify the categorization logic in the `categorize_content()` method to better match your content structure. The keyword matching can be adjusted based on your specific WordPress categories and content types.

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Example

```bash
# If your WordPress export file is named "my-blog-export.xml"
python wordpress_parser.py my-blog-export.xml
```

This will create a `wordpress_content` directory with all your organized content ready for use in your static site!


