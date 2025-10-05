<template>
  <div class="container-custom py-12">
    <h1 class="text-4xl font-bold text-gray-900 mb-8">Portfolio</h1>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <!-- missingtable.com -->
      <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition">
        <div class="p-6">
          <h2 class="text-2xl font-bold text-gray-900 mb-3">
            <a href="https://missingtable.com" target="_blank" class="hover:text-primary-600 transition">
              missingtable.com ↗
            </a>
          </h2>
          <div class="flex flex-wrap gap-2 mb-4">
            <span class="text-xs font-semibold text-primary-600 bg-primary-50 px-2 py-1 rounded">Vue.js</span>
            <span class="text-xs font-semibold text-primary-600 bg-primary-50 px-2 py-1 rounded">FastAPI</span>
            <span class="text-xs font-semibold text-primary-600 bg-primary-50 px-2 py-1 rounded">Supabase</span>
            <span class="text-xs font-semibold text-primary-600 bg-primary-50 px-2 py-1 rounded">GKE</span>
          </div>
          <p class="text-gray-700 mb-4">
            A comprehensive data quality and validation platform designed to help teams identify and track
            missing data patterns. Features automated data profiling, anomaly detection, and quality metrics.
          </p>
          <h3 class="font-bold text-gray-900 mb-2">Key Features:</h3>
          <ul class="list-disc list-inside text-gray-700 space-y-1 mb-4">
            <li>Real-time data quality monitoring</li>
            <li>Automated anomaly detection</li>
            <li>Custom validation rules</li>
            <li>Interactive dashboards and reporting</li>
          </ul>
          <a
            href="https://missingtable.com"
            target="_blank"
            class="text-primary-600 hover:text-primary-700 font-semibold"
          >
            Visit Project →
          </a>
        </div>
      </div>

      <!-- match-scraper -->
      <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition">
        <div class="p-6">
          <h2 class="text-2xl font-bold text-gray-900 mb-3">match-scraper</h2>
          <div class="flex flex-wrap gap-2 mb-4">
            <span class="text-xs font-semibold text-primary-600 bg-primary-50 px-2 py-1 rounded">Python</span>
            <span class="text-xs font-semibold text-primary-600 bg-primary-50 px-2 py-1 rounded">Scrapy</span>
            <span class="text-xs font-semibold text-primary-600 bg-primary-50 px-2 py-1 rounded">PostgreSQL</span>
            <span class="text-xs font-semibold text-primary-600 bg-primary-50 px-2 py-1 rounded">Docker</span>
          </div>
          <p class="text-gray-700 mb-4">
            An automated sports data collection and analysis tool that scrapes, processes, and analyzes
            match data from multiple sources. Built with reliability and data quality in mind.
          </p>
          <h3 class="font-bold text-gray-900 mb-2">Key Features:</h3>
          <ul class="list-disc list-inside text-gray-700 space-y-1 mb-4">
            <li>Distributed web scraping architecture</li>
            <li>Automated data validation and cleaning</li>
            <li>Historical data tracking and trends</li>
            <li>RESTful API for data access</li>
          </ul>
          <p class="text-gray-600 italic">Currently in active development</p>
        </div>
      </div>

      <!-- Quality Playbook -->
      <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition">
        <div class="p-6">
          <h2 class="text-2xl font-bold text-gray-900 mb-3">Quality Playbook</h2>
          <div class="flex flex-wrap gap-2 mb-4">
            <span class="text-xs font-semibold text-primary-600 bg-primary-50 px-2 py-1 rounded">Vue 3</span>
            <span class="text-xs font-semibold text-primary-600 bg-primary-50 px-2 py-1 rounded">TypeScript</span>
            <span class="text-xs font-semibold text-primary-600 bg-primary-50 px-2 py-1 rounded">FastAPI</span>
            <span class="text-xs font-semibold text-primary-600 bg-primary-50 px-2 py-1 rounded">Tailwind</span>
          </div>
          <p class="text-gray-700 mb-4">
            This very site! A GitOps-based blog platform where I share quality engineering insights.
            Features markdown-based content management with automated deployments to Kubernetes.
          </p>
          <h3 class="font-bold text-gray-900 mb-2">Technical Highlights:</h3>
          <ul class="list-disc list-inside text-gray-700 space-y-1 mb-4">
            <li>GitOps workflow for content updates</li>
            <li>Runtime markdown parsing with syntax highlighting</li>
            <li>Responsive design with Tailwind CSS</li>
            <li>Deployed on GKE Autopilot via Helm</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="mt-12 p-6 bg-gray-100 rounded-lg">
      <h2 class="text-2xl font-bold text-gray-900 mb-3">Technologies & Tools</h2>
      <div class="flex flex-wrap gap-3">
        <span class="bg-white px-4 py-2 rounded shadow text-gray-800 font-medium">Python</span>
        <span class="bg-white px-4 py-2 rounded shadow text-gray-800 font-medium">FastAPI</span>
        <span class="bg-white px-4 py-2 rounded shadow text-gray-800 font-medium">Vue.js</span>
        <span class="bg-white px-4 py-2 rounded shadow text-gray-800 font-medium">TypeScript</span>
        <span class="bg-white px-4 py-2 rounded shadow text-gray-800 font-medium">Pytest</span>
        <span class="bg-white px-4 py-2 rounded shadow text-gray-800 font-medium">Playwright</span>
        <span class="bg-white px-4 py-2 rounded shadow text-gray-800 font-medium">Docker</span>
        <span class="bg-white px-4 py-2 rounded shadow text-gray-800 font-medium">Kubernetes</span>
        <span class="bg-white px-4 py-2 rounded shadow text-gray-800 font-medium">GCP</span>
        <span class="bg-white px-4 py-2 rounded shadow text-gray-800 font-medium">PostgreSQL</span>
        <span class="bg-white px-4 py-2 rounded shadow text-gray-800 font-medium">Supabase</span>
        <span class="bg-white px-4 py-2 rounded shadow text-gray-800 font-medium">GitHub Actions</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Portfolio page component
</script>
