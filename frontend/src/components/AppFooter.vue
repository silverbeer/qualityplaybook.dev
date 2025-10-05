<template>
  <footer class="bg-gray-800 text-white mt-16">
    <div class="container-custom py-8">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div>
          <h3 class="text-lg font-bold mb-4">Quality Playbook</h3>
          <p class="text-gray-400">
            Insights and best practices in quality engineering, testing automation, and software quality.
          </p>
        </div>

        <div>
          <h3 class="text-lg font-bold mb-4">Quick Links</h3>
          <ul class="space-y-2">
            <li>
              <RouterLink to="/blog" class="text-gray-400 hover:text-white transition">
                Blog
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/about" class="text-gray-400 hover:text-white transition">
                About
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/portfolio" class="text-gray-400 hover:text-white transition">
                Portfolio
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/contact" class="text-gray-400 hover:text-white transition">
                Contact
              </RouterLink>
            </li>
          </ul>
        </div>

        <div>
          <h3 class="text-lg font-bold mb-4">Connect</h3>
          <p class="text-gray-400">
            Follow my work on <a href="https://missingtable.com" target="_blank" class="text-primary-400 hover:text-primary-300">missingtable.com</a>
          </p>
        </div>
      </div>

      <div class="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
        <p>&copy; {{ currentYear }} Quality Playbook. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

const currentYear = computed(() => new Date().getFullYear())
</script>
