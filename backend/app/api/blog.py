from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.services.markdown_parser import MarkdownParser

router = APIRouter(prefix="/api/blog", tags=["blog"])
parser = MarkdownParser()


@router.get("/posts")
async def list_posts(
    tag: Optional[str] = Query(None, description="Filter posts by tag"),
    limit: int = Query(10, ge=1, le=50, description="Number of posts per page"),
    offset: int = Query(0, ge=0, description="Number of posts to skip")
):
    """
    List blog posts with optional tag filtering and pagination
    """
    result = parser.list_posts(tag=tag, limit=limit, offset=offset)
    return result


@router.get("/posts/{slug}")
async def get_post(slug: str):
    """
    Get a single blog post by slug
    """
    post = parser.parse_post(slug)

    if not post:
        raise HTTPException(status_code=404, detail=f"Post '{slug}' not found")

    return post


@router.get("/tags")
async def get_tags():
    """
    Get all unique tags from all blog posts
    """
    tags = parser.get_all_tags()
    return {"tags": tags}
