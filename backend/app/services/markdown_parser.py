import frontmatter
import markdown
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class MarkdownParser:
    def __init__(self, content_dir: str = "content/blog"):
        self.content_dir = Path(content_dir)
        self.md = markdown.Markdown(
            extensions=[
                'fenced_code',
                'codehilite',
                'tables',
                'toc',
                'extra'
            ],
            extension_configs={
                'codehilite': {
                    'css_class': 'highlight',
                    'linenums': False
                }
            }
        )

    def parse_post(self, slug: str) -> Optional[Dict]:
        """Parse a single blog post by slug"""
        post_path = self.content_dir / f"{slug}.md"

        if not post_path.exists():
            return None

        post = frontmatter.load(post_path)

        # Reset markdown instance for clean parsing
        self.md.reset()
        html_content = self.md.convert(post.content)

        # Normalize date to string for consistent output
        date_value = post.get('date', datetime.now())
        if isinstance(date_value, datetime):
            date_str = date_value.isoformat()
        elif hasattr(date_value, 'isoformat'):  # datetime.date
            date_str = date_value.isoformat()
        else:
            date_str = str(date_value)

        return {
            "slug": slug,
            "title": post.get('title', 'Untitled'),
            "date": date_str,
            "tags": post.get('tags', []),
            "excerpt": post.get('excerpt', ''),
            "author": post.get('author', 'Quality Playbook'),
            "content": html_content,
            "toc": self.md.toc if hasattr(self.md, 'toc') else ''
        }

    def list_posts(self, tag: Optional[str] = None, limit: int = 10, offset: int = 0) -> Dict:
        """List blog posts with optional tag filtering and pagination"""
        posts = []

        # Get all markdown files
        for post_path in sorted(self.content_dir.glob("*.md"), reverse=True):
            post = frontmatter.load(post_path)
            slug = post_path.stem

            # Filter by tag if specified
            if tag and tag not in post.get('tags', []):
                continue

            # Normalize date to string for consistent comparison
            date_value = post.get('date', datetime.now())
            if isinstance(date_value, datetime):
                date_str = date_value.isoformat()
            elif hasattr(date_value, 'isoformat'):  # datetime.date
                date_str = date_value.isoformat()
            else:
                date_str = str(date_value)

            posts.append({
                "slug": slug,
                "title": post.get('title', 'Untitled'),
                "date": date_str,
                "tags": post.get('tags', []),
                "excerpt": post.get('excerpt', ''),
                "author": post.get('author', 'Quality Playbook'),
            })

        # Sort by date (most recent first) - now all dates are strings in ISO format
        posts.sort(key=lambda x: x['date'], reverse=True)

        # Apply pagination
        total = len(posts)
        paginated_posts = posts[offset:offset + limit]

        return {
            "posts": paginated_posts,
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": (offset + limit) < total
        }

    def get_all_tags(self) -> List[str]:
        """Get all unique tags from all posts"""
        tags = set()

        for post_path in self.content_dir.glob("*.md"):
            post = frontmatter.load(post_path)
            post_tags = post.get('tags', [])
            tags.update(post_tags)

        return sorted(list(tags))
