<template>
  <div class="container-custom py-12">
    <h1 class="text-4xl font-bold text-gray-900 mb-8">Portfolio</h1>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <!-- Resume as Code -->
      <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition">
        <div class="p-6">
          <h2 class="text-2xl font-bold text-gray-900 mb-3">
            <a href="https://github.com/silverbeer/resume-as-code" target="_blank" class="hover:text-primary-600 transition">
              Resume as Code ↗
            </a>
          </h2>
          <div class="flex flex-wrap gap-2 mb-4">
            <span class="text-xs font-semibold text-primary-600 bg-primary-50 px-2 py-1 rounded">Python</span>
            <span class="text-xs font-semibold text-primary-600 bg-primary-50 px-2 py-1 rounded">PydanticAI</span>
            <span class="text-xs font-semibold text-primary-600 bg-primary-50 px-2 py-1 rounded">Playwright</span>
            <span class="text-xs font-semibold text-primary-600 bg-primary-50 px-2 py-1 rounded">GitHub Actions</span>
          </div>
          <p class="text-gray-700 mb-4">
            <strong>Origin Story:</strong> Built by someone who got tired of maintaining 47 different Word documents named
            <code class="text-sm bg-gray-100 px-1">resume_final_v2_ACTUAL_final_use_this_one.docx</code>.
            Now maintains one Git repo instead. Progress? You decide.
          </p>
          <p class="text-gray-700 mb-4">
            <strong>Real Talk:</strong> This is what happens when an SRE applies Infrastructure as Code principles to job hunting.
            Is it over-engineered? Absolutely. Does it work? Also yes. Would I recommend it? Only if you enjoy explaining to
            recruiters why your resume is "deployed via CI/CD pipeline."
          </p>
          <h3 class="font-bold text-gray-900 mb-2">Key Features:</h3>
          <ul class="list-disc list-inside text-gray-700 space-y-1 mb-4">
            <li>AI-powered job description analysis with skill gap detection</li>
            <li>Multiple profile support for different role types (SRE, QE, SDET)</li>
            <li>ATS-friendly PDF generation via Playwright</li>
            <li>Version-controlled YAML-based resume data</li>
            <li>77 passing tests with solid coverage on core modules</li>
            <li>Built with uv, PydanticAI, and Claude Code (heavily vibe-coded)</li>
          </ul>
          <div class="mb-4">
            <a
              href="https://github.com/silverbeer/resume-as-code"
              target="_blank"
              class="text-primary-600 hover:text-primary-700 font-semibold"
            >
              View on GitHub →
            </a>
          </div>
          <p class="text-gray-600 text-sm italic">
            <strong>The Real Goal:</strong> Getting past ATS keyword filters to hopefully land this resume in front of an
            actual human decision maker who appreciates that someone built a CI/CD pipeline for their career. If you're that
            human and you're reading this—hi! 👋 Let's talk about how I can apply this same over-engineering energy to solving
            your infrastructure problems.
          </p>
        </div>
      </div>

      <!-- myrunstreak.run -->
      <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition">
        <div class="p-6">
          <h2 class="text-2xl font-bold text-gray-900 mb-3">
            <a href="https://github.com/silverbeer/myrunstreak.run" target="_blank" class="hover:text-primary-600 transition">
              myrunstreak.run ↗
            </a>
          </h2>
          <div class="flex flex-wrap gap-2 mb-4">
            <span class="text-xs font-semibold text-primary-600 bg-primary-50 px-2 py-1 rounded">AWS Lambda</span>
            <span class="text-xs font-semibold text-primary-600 bg-primary-50 px-2 py-1 rounded">Terraform</span>
            <span class="text-xs font-semibold text-primary-600 bg-primary-50 px-2 py-1 rounded">OIDC</span>
            <span class="text-xs font-semibold text-primary-600 bg-primary-50 px-2 py-1 rounded">GitHub Actions</span>
          </div>
          <p class="text-gray-700 mb-4">
            A serverless running streak tracker that pulls data from Strava and serves it via a public API.
            Built to scratch my own itch—tracking a 4,100+ day running streak—while learning AWS serverless
            patterns and modern IaC practices. Powers the "Did I Run Today?" widget on this very site.
          </p>
          <h3 class="font-bold text-gray-900 mb-2">Key Features:</h3>
          <ul class="list-disc list-inside text-gray-700 space-y-1 mb-4">
            <li>100% Infrastructure as Code with Terraform</li>
            <li>Keyless deploys via OIDC GitHub Actions to AWS</li>
            <li>Serverless API using AWS Lambda + API Gateway</li>
            <li>Nerd-friendly <code class="text-sm bg-gray-100 px-1">stk</code> CLI for local development</li>
            <li>Public JSON API for streak data consumption</li>
            <li>Smashrun integration for automatic activity sync</li>
          </ul>
          <div class="flex gap-4 mb-3">
            <a
              href="https://github.com/silverbeer/myrunstreak.run"
              target="_blank"
              class="text-primary-600 hover:text-primary-700 font-semibold"
            >
              View on GitHub →
            </a>
          </div>
          <p class="text-gray-600 text-sm italic">
            Live in production. The streak must continue. Fellow streak runners should check out
            <a href="https://smashrun.com" target="_blank" class="text-primary-600 hover:text-primary-700">Smashrun</a>—the
            best running analytics platform out there.
            <a href="https://smashrun.com/tom.drake/" target="_blank" class="text-primary-600 hover:text-primary-700">Follow my runs</a>.
          </p>
        </div>
      </div>

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
            A passion project tracking the highest-level youth soccer league in the US, inspired by my son's journey in the sport.
            Built as a learning platform to explore modern development practices including Gen AI, infrastructure as code, and quality
            engineering - while hopefully inspiring the next generation to build and create.
          </p>
          <h3 class="font-bold text-gray-900 mb-2">Key Features:</h3>
          <ul class="list-disc list-inside text-gray-700 space-y-1 mb-4">
            <li>Live match results and schedules for youth soccer leagues</li>
            <li>Community-driven: Team managers can invite fans to follow teams</li>
            <li>Parent and player insights including standings and statistics</li>
            <li>Track league matches, friendlies, and tournaments</li>
            <li>Expandable architecture to support multiple leagues and clubs</li>
            <li>Open source to inspire young players to learn coding</li>
          </ul>
          <div class="flex gap-4 mb-3">
            <a
              href="https://missingtable.com"
              target="_blank"
              class="text-primary-600 hover:text-primary-700 font-semibold"
            >
              Visit Project →
            </a>
            <a
              href="https://github.com/silverbeer/missing-table"
              target="_blank"
              class="text-primary-600 hover:text-primary-700 font-semibold"
            >
              GitHub →
            </a>
          </div>
          <p class="text-gray-600 text-sm italic">
            Actively being developed. Interested in learning more or contributing?
            Contact me at <a href="mailto:silverbeer.io@gmail.com" class="text-primary-600 hover:text-primary-700">silverbeer.io@gmail.com</a>
          </p>
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
            The data collector that powers missingtable.com—and my excuse to geek out on distributed systems.
            Uses Playwright to scrape match data, RabbitMQ and Celery to orchestrate everything, all running on a
            K3S cluster in my house. Learning message queues has never been this fun!
          </p>
          <h3 class="font-bold text-gray-900 mb-2">Key Features:</h3>
          <ul class="list-disc list-inside text-gray-700 space-y-1 mb-4">
            <li>Scrapes match schedules and results automatically</li>
            <li>Distributed task processing (because overkill is underrated)</li>
            <li>Built-in data validation to catch mistakes</li>
            <li>Historical data for tracking team performance</li>
            <li>Deployed on home K3S—real infrastructure, real learning</li>
          </ul>
          <div class="mb-4">
            <a
              href="https://github.com/silverbeer/match-scraper"
              target="_blank"
              class="text-primary-600 hover:text-primary-700 font-semibold"
            >
              View on GitHub →
            </a>
          </div>
          <p class="text-gray-600 text-sm italic">
            Actively being developed. Interested in learning more or contributing?
            Contact me at <a href="mailto:silverbeer.io@gmail.com" class="text-primary-600 hover:text-primary-700">silverbeer.io@gmail.com</a>
          </p>
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
            This very site! A quality engineering blog built with quality engineering practices (practicing what I preach over here).
            Write posts in Markdown, commit to GitHub, auto-deploy to Kubernetes—pure GitOps bliss. Built as a learning project to
            explore modern web architecture, DevOps pipelines, and whether I can actually follow my own advice.
          </p>
          <h3 class="font-bold text-gray-900 mb-2">Key Features:</h3>
          <ul class="list-disc list-inside text-gray-700 space-y-1 mb-4">
            <li>GitOps content workflow—commit to main, watch it deploy</li>
            <li>Vue 3 + TypeScript frontend paired with FastAPI backend</li>
            <li>Prism.js syntax highlighting for all those code examples</li>
            <li>Deployed on GKE Autopilot via Helm charts</li>
            <li>Learning project exploring modern web + DevOps patterns</li>
            <li>Open source because gatekeeping is boring</li>
          </ul>
          <div class="mb-4">
            <a
              href="https://github.com/silverbeer/qualityplaybook.dev"
              target="_blank"
              class="text-primary-600 hover:text-primary-700 font-semibold"
            >
              View on GitHub →
            </a>
          </div>
          <p class="text-gray-600 text-sm italic">
            Actively being developed. Interested in learning more or contributing?
            Contact me at <a href="mailto:silverbeer.io@gmail.com" class="text-primary-600 hover:text-primary-700">silverbeer.io@gmail.com</a>
          </p>
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
        <span class="bg-white px-4 py-2 rounded shadow text-gray-800 font-medium">PydanticAI</span>
        <span class="bg-white px-4 py-2 rounded shadow text-gray-800 font-medium">Pytest</span>
        <span class="bg-white px-4 py-2 rounded shadow text-gray-800 font-medium">Playwright</span>
        <span class="bg-white px-4 py-2 rounded shadow text-gray-800 font-medium">Docker</span>
        <span class="bg-white px-4 py-2 rounded shadow text-gray-800 font-medium">Kubernetes</span>
        <span class="bg-white px-4 py-2 rounded shadow text-gray-800 font-medium">GCP</span>
        <span class="bg-white px-4 py-2 rounded shadow text-gray-800 font-medium">AWS</span>
        <span class="bg-white px-4 py-2 rounded shadow text-gray-800 font-medium">Terraform</span>
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
