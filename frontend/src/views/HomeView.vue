<template>
  <div>
    <!-- Hero Section -->
    <section class="bg-gradient-to-r from-primary-600 to-primary-800 dark:from-primary-700 dark:to-primary-900 text-white py-20">
      <div class="container-custom">
        <div class="max-w-3xl">
          <h1 class="text-5xl font-bold mb-6">Welcome to Quality Playbook</h1>
          <div class="text-2xl font-semibold mb-4 text-primary-200">
            "Quality is a Team Sport"
          </div>
          <p class="text-xl mb-8 text-primary-100">
            Insights, strategies, and best practices in quality engineering from a seasoned QE professional.
            Join me as I share my journey in building robust testing frameworks and quality-first cultures.
          </p>
          <div class="flex gap-4">
            <RouterLink to="/blog" class="bg-white text-primary-600 px-6 py-3 rounded-lg font-semibold hover:bg-primary-50 transition">
              Read the Blog
            </RouterLink>
            <RouterLink to="/about" class="border-2 border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white hover:text-primary-600 transition">
              About Me
            </RouterLink>
          </div>
        </div>
      </div>
    </section>

    <!-- Recent Posts Section -->
    <section class="container-custom py-16">
      <div class="flex items-center justify-between mb-8">
        <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100">Recent Posts</h2>
        <RouterLink to="/blog" class="text-primary-600 hover:text-primary-700 font-semibold">
          View all posts →
        </RouterLink>
      </div>

      <div v-if="blogStore.loading" class="text-center py-12">
        <p class="text-gray-600">Loading posts...</p>
      </div>

      <div v-else-if="blogStore.error" class="text-center py-12">
        <p class="text-red-600">{{ blogStore.error }}</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <BlogCard
          v-for="post in blogStore.posts.slice(0, 3)"
          :key="post.slug"
          :post="post"
        />
      </div>
    </section>

    <!-- Features Section -->
    <section class="bg-gray-100 dark:bg-gray-800 py-16">
      <div class="container-custom">
        <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 text-center mb-12">What You'll Find Here</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="bg-white dark:bg-gray-700 p-6 rounded-lg shadow-md">
            <div class="text-primary-600 dark:text-primary-400 text-4xl mb-4">🧪</div>
            <h3 class="text-xl font-bold mb-3 text-gray-900 dark:text-gray-100">Testing Strategies</h3>
            <p class="text-gray-700 dark:text-gray-300">
              Deep dives into test automation, frameworks, and quality engineering best practices.
            </p>
          </div>
          <div class="bg-white dark:bg-gray-700 p-6 rounded-lg shadow-md">
            <div class="text-primary-600 dark:text-primary-400 text-4xl mb-4">⚙️</div>
            <h3 class="text-xl font-bold mb-3 text-gray-900 dark:text-gray-100">Tools & Tech</h3>
            <p class="text-gray-700 dark:text-gray-300">
              Reviews and tutorials on the latest testing tools, CI/CD pipelines, and automation frameworks.
            </p>
          </div>
          <div class="bg-white dark:bg-gray-700 p-6 rounded-lg shadow-md">
            <div class="text-primary-600 dark:text-primary-400 text-4xl mb-4">📊</div>
            <h3 class="text-xl font-bold mb-3 text-gray-900 dark:text-gray-100">Real Projects</h3>
            <p class="text-gray-700 dark:text-gray-300">
              Case studies and experiences from building products like missingtable.com and match-scraper.
            </p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useBlogStore } from '../stores/blog'
import BlogCard from '../components/BlogCard.vue'

const blogStore = useBlogStore()

onMounted(() => {
  blogStore.fetchPosts(undefined, 3, 0)
})
</script>
