<template>
  <div class="bg-white dark:bg-gray-700 p-6 rounded-lg shadow-md">
    <!-- Loading State -->
    <div v-if="loading" class="animate-pulse">
      <div class="h-6 bg-gray-200 dark:bg-gray-600 rounded w-3/4 mb-4"></div>
      <div class="h-10 bg-gray-200 dark:bg-gray-600 rounded w-1/2 mb-4"></div>
      <div class="h-4 bg-gray-200 dark:bg-gray-600 rounded w-full mb-2"></div>
      <div class="h-4 bg-gray-200 dark:bg-gray-600 rounded w-2/3"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center">
      <div class="text-gray-400 dark:text-gray-500 text-4xl mb-2">🏃</div>
      <p class="text-gray-500 dark:text-gray-400 text-sm">Running data unavailable</p>
    </div>

    <!-- Data Display -->
    <div v-else-if="streakData">
      <div class="flex items-center gap-2 mb-3">
        <span class="text-2xl">🏃</span>
        <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100">Did I Run Today?</h3>
      </div>

      <!-- Today's Status -->
      <div class="flex items-center gap-2 mb-4">
        <span
          v-if="streakData.ran_today"
          class="inline-flex items-center gap-1 text-sm font-semibold text-green-600 dark:text-green-400 bg-green-100 dark:bg-green-900/30 px-3 py-1 rounded-full"
        >
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
          </svg>
          Yes!
        </span>
        <span
          v-else
          class="inline-flex items-center gap-1 text-sm font-semibold text-amber-600 dark:text-amber-400 bg-amber-100 dark:bg-amber-900/30 px-3 py-1 rounded-full"
        >
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
          </svg>
          Not yet today
        </span>
      </div>

      <!-- Streak Count -->
      <div class="mb-4">
        <div class="text-4xl font-bold text-primary-600 dark:text-primary-400">
          {{ formatNumber(streakData.streak.current_days) }}
        </div>
        <div class="text-sm text-gray-600 dark:text-gray-400">
          day streak since {{ formatStartDate(streakData.streak.started) }}
        </div>
        <!-- Days Milestone Celebration -->
        <div
          v-if="getDaysMilestone(streakData.streak.current_days)"
          class="text-xs font-semibold text-amber-600 dark:text-amber-400 bg-amber-100 dark:bg-amber-900/30 px-2 py-1 rounded mt-2 inline-block"
        >
          🎉 {{ formatNumber(getDaysMilestone(streakData.streak.current_days)!) }} days!
        </div>

        <div v-if="streakData.streak.total_mi" class="text-sm font-medium text-gray-700 dark:text-gray-300 mt-1">
          {{ formatNumber(streakData.streak.total_mi) }} miles total
        </div>
        <!-- Miles Milestone Celebration -->
        <div
          v-if="streakData.streak.total_mi && getMilesMilestone(streakData.streak.total_mi)"
          class="text-xs font-semibold text-amber-600 dark:text-amber-400 bg-amber-100 dark:bg-amber-900/30 px-2 py-1 rounded mt-1 inline-block"
        >
          🎉 {{ formatNumber(getMilesMilestone(streakData.streak.total_mi)!) }} miles!
        </div>
      </div>

      <!-- Last Run Info -->
      <div v-if="streakData.last_run" class="text-sm text-gray-600 dark:text-gray-400 border-t border-gray-200 dark:border-gray-600 pt-3">
        <div class="flex justify-between">
          <span>Last run:</span>
          <span class="font-medium text-gray-900 dark:text-gray-100">
            {{ formatLastRunDate(streakData.last_run.date) }}
          </span>
        </div>
        <div class="flex justify-between mt-1">
          <span>Distance:</span>
          <span class="font-medium text-gray-900 dark:text-gray-100">
            {{ streakData.last_run.distance_mi.toFixed(1) }} mi
          </span>
        </div>
        <div class="flex justify-between mt-1">
          <span>Duration:</span>
          <span class="font-medium text-gray-900 dark:text-gray-100">
            {{ streakData.last_run.duration_min.toFixed(0) }} min
          </span>
        </div>
      </div>

      <!-- Totals -->
      <div class="text-xs text-gray-500 dark:text-gray-400 border-t border-gray-200 dark:border-gray-600 pt-3 mt-3">
        <div class="flex justify-between items-center">
          <span>This month:</span>
          <span class="flex items-center gap-1">
            <span :class="streakData.month_total_mi >= 100 ? 'text-green-600 dark:text-green-400 font-medium' : ''">
              {{ streakData.month_total_mi.toFixed(1) }} mi
            </span>
            <svg v-if="streakData.month_total_mi >= 100" class="w-3 h-3 text-green-600 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
            </svg>
          </span>
        </div>
        <div class="flex justify-between items-center mt-1">
          <span>This year:</span>
          <span class="flex items-center gap-1">
            <span :class="streakData.year_total_mi >= 1200 ? 'text-green-600 dark:text-green-400 font-medium' : ''">
              {{ streakData.year_total_mi.toFixed(1) }} mi
            </span>
            <svg v-if="streakData.year_total_mi >= 1200" class="w-3 h-3 text-green-600 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
            </svg>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface StreakData {
  updated_at: string
  ran_today: boolean
  streak: {
    current_days: number
    started: string
    total_mi?: number
  }
  last_run: {
    date: string
    distance_mi: number
    duration_min: number
  }
  last_7_days: Array<{
    date: string
    distance_mi: number
  }>
  month_total_mi: number
  year_total_mi: number
}

const CACHE_KEY = 'running_streak_data'
const CACHE_DURATION = 5 * 60 * 1000 // 5 minutes in milliseconds
const API_URL = 'https://storage.googleapis.com/myrunstreak-public/status.json'

const streakData = ref<StreakData | null>(null)
const loading = ref(true)
const error = ref(false)

const formatNumber = (num: number): string => {
  return num.toLocaleString('en-US')
}

// Check if a milestone was recently crossed (within the last value)
const getDaysMilestone = (days: number): number | null => {
  const milestones = [10000, 7500, 5000, 4000, 3000, 2000, 1000]
  for (const milestone of milestones) {
    if (days >= milestone && days < milestone + 100) {
      return milestone
    }
  }
  return null
}

const getMilesMilestone = (miles: number): number | null => {
  const milestones = [50000, 40000, 30000, 25000, 20000, 15000, 10000, 5000]
  for (const milestone of milestones) {
    if (miles >= milestone && miles < milestone + 500) {
      return milestone
    }
  }
  return null
}

const formatStartDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const formatLastRunDate = (dateString: string): string => {
  // Compare date strings directly to avoid timezone issues
  // dateString format is "YYYY-MM-DD"
  const today = new Date()
  const todayStr = today.toISOString().split('T')[0]

  const yesterday = new Date(today)
  yesterday.setDate(yesterday.getDate() - 1)
  const yesterdayStr = yesterday.toISOString().split('T')[0]

  if (dateString === todayStr) {
    return 'Today'
  }

  if (dateString === yesterdayStr) {
    return 'Yesterday'
  }

  // Parse the date string as local date for display
  const [year, month, day] = dateString.split('-').map(Number)
  const date = new Date(year, month - 1, day)

  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric'
  })
}

const getCachedData = (): StreakData | null => {
  try {
    const cached = localStorage.getItem(CACHE_KEY)
    if (!cached) return null

    const { data, timestamp } = JSON.parse(cached)
    const now = Date.now()

    if (now - timestamp < CACHE_DURATION) {
      return data
    }
  } catch {
    // Cache read failed, return null
  }
  return null
}

const setCachedData = (data: StreakData): void => {
  try {
    localStorage.setItem(CACHE_KEY, JSON.stringify({
      data,
      timestamp: Date.now()
    }))
  } catch {
    // Cache write failed, ignore
  }
}

const fetchStreakData = async (): Promise<void> => {
  // Try cache first
  const cached = getCachedData()
  if (cached) {
    streakData.value = cached
    loading.value = false
    return
  }

  try {
    const response = await fetch(API_URL)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data: StreakData = await response.json()
    streakData.value = data
    setCachedData(data)
    error.value = false
  } catch (e) {
    // Try to use stale cache on error
    try {
      const stale = localStorage.getItem(CACHE_KEY)
      if (stale) {
        const { data } = JSON.parse(stale)
        streakData.value = data
        error.value = false
        return
      }
    } catch {
      // Stale cache read failed
    }

    error.value = true
    console.error('Failed to fetch running streak data:', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchStreakData()
})
</script>
