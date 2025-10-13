<template>
  <div class="container-custom py-12">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-4xl font-bold text-gray-900 mb-8">About Me</h1>

      <div class="prose prose-lg max-w-none">
        <p class="text-xl text-gray-700 mb-6">
          Hi! I'm a quality engineering professional passionate about building robust testing frameworks
          and championing quality-first development practices.
        </p>

        <h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4">What I Do</h2>
        <p class="text-gray-700 mb-4">
          I specialize in test automation, CI/CD pipelines, and quality engineering strategies. My focus
          is on helping teams build better software through comprehensive testing, automation, and quality
          metrics.
        </p>

        <h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4">My Projects</h2>
        <ul class="list-disc list-inside text-gray-700 space-y-2 mb-4">
          <li>
            <a href="https://dev.missingtable.com" target="_blank" class="text-primary-600 hover:text-primary-700 font-semibold">
              dev.missingtable.com
            </a> - A data quality and validation platform
          </li>
          <li>
            <strong>match-scraper</strong> - Automated sports data collection and analysis tool
          </li>
        </ul>

        <h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4">Tech Stack</h2>
        <p class="text-gray-700 mb-4">
          I work with modern technologies including Python (FastAPI, Pytest), JavaScript/TypeScript (Vue.js, Node.js),
          and cloud platforms (GCP, Kubernetes). I'm experienced in building scalable testing infrastructure
          and quality automation systems.
        </p>

        <h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4">Why Quality Playbook?</h2>
        <p class="text-gray-700 mb-4">
          This blog is my playbook for quality engineering - a collection of strategies, tools, and insights
          I've learned throughout my career. I created it to share knowledge with the QE community and to
          document my journey in building quality-first software.
        </p>

        <div class="mt-12 p-6 bg-primary-50 rounded-lg">
          <h3 class="text-xl font-bold text-gray-900 mb-3">Let's Connect</h3>
          <p class="text-gray-700 mb-4">
            Interested in working together or have questions about quality engineering?
          </p>
          <RouterLink to="/contact" class="btn-primary inline-block">
            Get in Touch
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>
