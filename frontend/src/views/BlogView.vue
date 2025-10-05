<template>
  <div class="container-custom py-12">
    <h1 class="text-4xl font-bold text-gray-900 mb-8">Blog</h1>

    <!-- Tags Filter -->
    <div class="mb-8">
      <div class="flex flex-wrap gap-2">
        <button
          @click="selectedTag = null; loadPosts()"
          :class="[
            'px-4 py-2 rounded-lg font-semibold transition',
            selectedTag === null
              ? 'bg-primary-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          ]"
        >
          All Posts
        </button>
        <button
          v-for="tag in blogStore.tags"
          :key="tag"
          @click="selectedTag = tag; loadPosts()"
          :class="[
            'px-4 py-2 rounded-lg font-semibold transition',
            selectedTag === tag
              ? 'bg-primary-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          ]"
        >
          {{ tag }}
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="blogStore.loading" class="text-center py-12">
      <p class="text-gray-600">Loading posts...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="blogStore.error" class="text-center py-12">
      <p class="text-red-600">{{ blogStore.error }}</p>
    </div>

    <!-- Posts Grid -->
    <div v-else>
      <div v-if="blogStore.posts.length === 0" class="text-center py-12">
        <p class="text-gray-600">No posts found.</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
        <BlogCard
          v-for="post in blogStore.posts"
          :key="post.slug"
          :post="post"
        />
      </div>

      <!-- Pagination -->
      <div v-if="blogStore.total > postsPerPage" class="flex justify-center gap-4">
        <button
          @click="previousPage"
          :disabled="currentPage === 1"
          :class="[
            'px-6 py-2 rounded-lg font-semibold transition',
            currentPage === 1
              ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
              : 'bg-primary-600 text-white hover:bg-primary-700'
          ]"
        >
          ← Previous
        </button>

        <span class="px-4 py-2 text-gray-700">
          Page {{ currentPage }} of {{ totalPages }}
        </span>

        <button
          @click="nextPage"
          :disabled="!blogStore.hasMore"
          :class="[
            'px-6 py-2 rounded-lg font-semibold transition',
            !blogStore.hasMore
              ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
              : 'bg-primary-600 text-white hover:bg-primary-700'
          ]"
        >
          Next →
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useBlogStore } from '../stores/blog'
import BlogCard from '../components/BlogCard.vue'

const blogStore = useBlogStore()
const selectedTag = ref<string | null>(null)
const currentPage = ref(1)
const postsPerPage = 10

const totalPages = computed(() => Math.ceil(blogStore.total / postsPerPage))

const loadPosts = () => {
  const offset = (currentPage.value - 1) * postsPerPage
  blogStore.fetchPosts(selectedTag.value || undefined, postsPerPage, offset)
}

const nextPage = () => {
  if (blogStore.hasMore) {
    currentPage.value++
    loadPosts()
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    loadPosts()
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

onMounted(() => {
  blogStore.fetchTags()
  loadPosts()
})
</script>
