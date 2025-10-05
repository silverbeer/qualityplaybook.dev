<template>
  <article class="container-custom py-12">
    <div v-if="blogStore.loading" class="text-center py-12">
      <p class="text-gray-600">Loading post...</p>
    </div>

    <div v-else-if="blogStore.error" class="text-center py-12">
      <p class="text-red-600">{{ blogStore.error }}</p>
      <RouterLink to="/blog" class="text-primary-600 hover:text-primary-700 mt-4 inline-block">
        ← Back to blog
      </RouterLink>
    </div>

    <div v-else-if="blogStore.currentPost" class="max-w-4xl mx-auto">
      <!-- Back Link -->
      <RouterLink to="/blog" class="text-primary-600 hover:text-primary-700 mb-6 inline-flex items-center">
        ← Back to blog
      </RouterLink>

      <!-- Post Header -->
      <header class="mb-8 mt-6">
        <div class="flex flex-wrap gap-2 mb-4">
          <span
            v-for="tag in blogStore.currentPost.tags"
            :key="tag"
            class="text-sm font-semibold text-primary-600 bg-primary-50 px-3 py-1 rounded"
          >
            {{ tag }}
          </span>
        </div>

        <h1 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          {{ blogStore.currentPost.title }}
        </h1>

        <div class="flex items-center text-gray-600">
          <time :datetime="blogStore.currentPost.date">
            {{ formatDate(blogStore.currentPost.date) }}
          </time>
          <span class="mx-3">•</span>
          <span>{{ blogStore.currentPost.author }}</span>
        </div>
      </header>

      <!-- Post Content -->
      <div
        class="prose prose-lg max-w-none prose-headings:text-gray-900 prose-a:text-primary-600 prose-code:text-primary-600 prose-pre:bg-gray-900"
        v-html="blogStore.currentPost.content"
      ></div>
    </div>
  </article>
</template>

<script setup lang="ts">
import { onMounted, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useBlogStore } from '../stores/blog'
import Prism from 'prismjs'
import 'prismjs/themes/prism-tomorrow.css'
import 'prismjs/components/prism-python'
import 'prismjs/components/prism-javascript'
import 'prismjs/components/prism-typescript'
import 'prismjs/components/prism-bash'
import 'prismjs/components/prism-json'
import 'prismjs/components/prism-yaml'

const route = useRoute()
const blogStore = useBlogStore()

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const loadPost = async () => {
  const slug = route.params.slug as string
  await blogStore.fetchPost(slug)

  // Highlight code blocks after content is loaded
  setTimeout(() => {
    Prism.highlightAll()
  }, 100)
}

onMounted(loadPost)

watch(() => route.params.slug, loadPost)
</script>

<style>
/* Tailwind Typography styles */
.prose {
  color: #374151;
  line-height: 1.75;
}

.prose img {
  border-radius: 0.5rem;
  margin: 2rem 0;
}

.prose code {
  background-color: #f3f4f6;
  padding: 0.2rem 0.4rem;
  border-radius: 0.25rem;
  font-size: 0.875em;
}

.prose pre {
  background-color: #1e293b !important;
  border-radius: 0.5rem;
  padding: 1.5rem;
  overflow-x: auto;
}

.prose pre code {
  background-color: transparent;
  padding: 0;
  color: #e2e8f0;
}

.prose h1, .prose h2, .prose h3, .prose h4 {
  font-weight: 700;
  margin-top: 2rem;
  margin-bottom: 1rem;
}

.prose h2 {
  font-size: 1.875rem;
  border-bottom: 2px solid #e5e7eb;
  padding-bottom: 0.5rem;
}

.prose h3 {
  font-size: 1.5rem;
}

.prose ul, .prose ol {
  margin: 1.5rem 0;
  padding-left: 1.5rem;
}

.prose li {
  margin: 0.5rem 0;
}

.prose a {
  text-decoration: underline;
}

.prose a:hover {
  color: #0284c7;
}

.prose blockquote {
  border-left: 4px solid #0ea5e9;
  padding-left: 1rem;
  font-style: italic;
  color: #6b7280;
  margin: 1.5rem 0;
}

.prose table {
  width: 100%;
  border-collapse: collapse;
  margin: 2rem 0;
}

.prose th, .prose td {
  border: 1px solid #e5e7eb;
  padding: 0.75rem;
  text-align: left;
}

.prose th {
  background-color: #f9fafb;
  font-weight: 600;
}
</style>
