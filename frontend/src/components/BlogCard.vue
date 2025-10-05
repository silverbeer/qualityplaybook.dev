<template>
  <article class="bg-white rounded-lg shadow-md hover:shadow-lg transition duration-300 overflow-hidden">
    <RouterLink :to="`/blog/${post.slug}`" class="block">
      <div class="p-6">
        <div class="flex items-center gap-2 mb-3">
          <span
            v-for="tag in post.tags"
            :key="tag"
            class="text-xs font-semibold text-primary-600 bg-primary-50 px-2 py-1 rounded"
          >
            {{ tag }}
          </span>
        </div>

        <h2 class="text-2xl font-bold text-gray-900 mb-2 hover:text-primary-600 transition">
          {{ post.title }}
        </h2>

        <div class="text-sm text-gray-500 mb-3">
          <time :datetime="post.date">{{ formatDate(post.date) }}</time>
          <span class="mx-2">•</span>
          <span>{{ post.author }}</span>
        </div>

        <p class="text-gray-700 line-clamp-3">
          {{ post.excerpt }}
        </p>

        <div class="mt-4 text-primary-600 font-semibold hover:text-primary-700">
          Read more →
        </div>
      </div>
    </RouterLink>
  </article>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import type { BlogPost } from '../stores/blog'

defineProps<{
  post: BlogPost
}>()

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
