import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export interface BlogPost {
  slug: string
  title: string
  date: string
  tags: string[]
  excerpt: string
  author: string
  content?: string
  toc?: string
}

export interface BlogListResponse {
  posts: BlogPost[]
  total: number
  limit: number
  offset: number
  has_more: boolean
}

const API_BASE = import.meta.env.VITE_API_BASE || '/api'

export const useBlogStore = defineStore('blog', () => {
  const posts = ref<BlogPost[]>([])
  const currentPost = ref<BlogPost | null>(null)
  const tags = ref<string[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const total = ref(0)
  const hasMore = ref(false)

  const fetchPosts = async (tag?: string, limit = 10, offset = 0) => {
    loading.value = true
    error.value = null
    try {
      const params = new URLSearchParams()
      if (tag) params.append('tag', tag)
      params.append('limit', limit.toString())
      params.append('offset', offset.toString())

      const response = await axios.get<BlogListResponse>(
        `${API_BASE}/blog/posts?${params.toString()}`
      )

      posts.value = response.data.posts
      total.value = response.data.total
      hasMore.value = response.data.has_more
    } catch (e: any) {
      error.value = e.message || 'Failed to fetch posts'
      console.error('Error fetching posts:', e)
    } finally {
      loading.value = false
    }
  }

  const fetchPost = async (slug: string) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.get<BlogPost>(`${API_BASE}/blog/posts/${slug}`)
      currentPost.value = response.data
    } catch (e: any) {
      error.value = e.message || 'Failed to fetch post'
      console.error('Error fetching post:', e)
    } finally {
      loading.value = false
    }
  }

  const fetchTags = async () => {
    try {
      const response = await axios.get<{ tags: string[] }>(`${API_BASE}/blog/tags`)
      tags.value = response.data.tags
    } catch (e: any) {
      console.error('Error fetching tags:', e)
    }
  }

  return {
    posts,
    currentPost,
    tags,
    loading,
    error,
    total,
    hasMore,
    fetchPosts,
    fetchPost,
    fetchTags
  }
})
