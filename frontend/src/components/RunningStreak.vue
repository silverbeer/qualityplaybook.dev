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

      <!-- Streak Count - Flip Clock Style -->
      <div class="mb-4">
        <div class="flip-counter">
          <div
            v-for="(digit, index) in getDigits(streakData.streak.current_days)"
            :key="index"
            class="flip-digit"
          >
            <span class="digit-value">{{ digit }}</span>
            <div class="digit-divider"></div>
          </div>
        </div>
        <div class="text-sm text-gray-600 dark:text-gray-400 mt-2">
          day streak since {{ formatStartDate(streakData.streak.started) }}
        </div>
        <div v-if="streakData.streak.duration" class="text-sm text-gray-500 dark:text-gray-400">
          {{ streakData.streak.duration }}
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
            <span class="text-gray-500 dark:text-gray-400 font-normal">({{ formatDateShort(streakData.last_run.date) }})</span>
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
            <span :class="monthGoalMet ? 'text-green-600 dark:text-green-400 font-medium' : ''">
              {{ streakData.month_total_mi.toFixed(1) }} mi
            </span>
            <svg v-if="monthGoalMet" class="w-3 h-3 text-green-600 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
            </svg>
          </span>
        </div>
        <div class="flex justify-between items-center mt-1">
          <span>This year:</span>
          <span class="flex items-center gap-1">
            <span :class="yearGoalMet ? 'text-green-600 dark:text-green-400 font-medium' : ''">
              {{ streakData.year_total_mi.toFixed(1) }} mi
            </span>
            <svg v-if="yearGoalMet" class="w-3 h-3 text-green-600 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
            </svg>
          </span>
        </div>
      </div>

      <!-- Goals Progress -->
      <div
        v-if="streakData.goals && (streakData.goals.monthly || streakData.goals.yearly)"
        class="border-t border-gray-200 dark:border-gray-600 pt-3 mt-3"
      >
        <div class="text-xs font-semibold text-gray-700 dark:text-gray-300 mb-2 uppercase tracking-wide">
          Goals
        </div>

        <!-- Monthly Goal -->
        <div v-if="streakData.goals.monthly && monthlyDisplay" class="mb-3">
          <div class="flex items-start justify-between gap-2 mb-1">
            <span class="text-xs font-medium text-gray-700 dark:text-gray-300">
              📅 {{ currentMonthName }}
              <span v-if="monthlyDisplay.percent >= 100" class="ml-1">🎉</span>
            </span>
            <span class="text-xs font-semibold text-gray-900 dark:text-gray-100 whitespace-nowrap">
              {{ monthlyDisplay.progress_mi.toFixed(1) }} / {{ monthlyDisplay.goal_mi.toFixed(0) }} mi
            </span>
          </div>
          <p
            v-if="streakData.goals.monthly.text"
            class="text-xs text-gray-500 dark:text-gray-400 italic mb-1.5 line-clamp-3"
            :title="streakData.goals.monthly.text"
          >
            {{ streakData.goals.monthly.text }}
          </p>
          <div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2 overflow-hidden">
            <div
              class="h-2 rounded-full transition-all duration-500"
              :class="getProgressBarColor(monthlyDisplay.percent, monthlyPaceDelta)"
              :style="{ width: Math.min(monthlyDisplay.percent, 100) + '%' }"
            ></div>
          </div>
          <div class="flex justify-between items-center mt-1 text-xs">
            <span class="text-gray-500 dark:text-gray-400">
              {{ monthlyDisplay.percent.toFixed(1) }}%
            </span>
            <span v-if="monthlyDisplay.percent >= 100" class="text-green-600 dark:text-green-400 font-medium">
              🎉 Goal achieved!
            </span>
            <span v-else :class="getPaceColor(monthlyPaceDelta)">
              {{ formatMilesDelta(monthlyMilesDelta) }}
            </span>
          </div>
        </div>

        <!-- Yearly Goal -->
        <div v-if="streakData.goals.yearly && yearlyDisplay">
          <div class="flex items-start justify-between gap-2 mb-1">
            <span class="text-xs font-medium text-gray-700 dark:text-gray-300">
              🎯 {{ currentYear }}
              <span v-if="yearlyDisplay.percent >= 100" class="ml-1">🎉</span>
            </span>
            <span class="text-xs font-semibold text-gray-900 dark:text-gray-100 whitespace-nowrap">
              {{ yearlyDisplay.progress_mi.toFixed(1) }} / {{ yearlyDisplay.goal_mi.toFixed(0) }} mi
            </span>
          </div>
          <p
            v-if="streakData.goals.yearly.text"
            class="text-xs text-gray-500 dark:text-gray-400 italic mb-1.5 line-clamp-3"
            :title="streakData.goals.yearly.text"
          >
            {{ streakData.goals.yearly.text }}
          </p>
          <div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2 overflow-hidden">
            <div
              class="h-2 rounded-full transition-all duration-500"
              :class="getProgressBarColor(yearlyDisplay.percent, yearlyPaceDelta)"
              :style="{ width: Math.min(yearlyDisplay.percent, 100) + '%' }"
            ></div>
          </div>
          <div class="flex justify-between items-center mt-1 text-xs">
            <span class="text-gray-500 dark:text-gray-400">
              {{ yearlyDisplay.percent.toFixed(1) }}%
            </span>
            <span v-if="yearlyDisplay.percent >= 100" class="text-green-600 dark:text-green-400 font-medium">
              🎉 Goal achieved!
            </span>
            <span v-else :class="getPaceColor(yearlyPaceDelta)">
              {{ formatMilesDelta(yearlyMilesDelta) }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

interface GoalProgress {
  goal_mi: number
  progress_mi: number
  percent: number
  text?: string
  fetched_at?: string
}

interface StreakData {
  updated_at: string
  ran_today: boolean
  streak: {
    current_days: number
    started: string
    duration?: string
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
  goals?: {
    monthly?: GoalProgress
    yearly?: GoalProgress
  }
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

const getDigits = (num: number): string[] => {
  return num.toString().split('')
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

const formatDateShort = (dateString: string): string => {
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

// Goal pace calculations — compare actual % against expected % based on
// how far through the period we are (day_of_period / days_in_period).
const now = new Date()
const currentYear = now.getFullYear()
const currentMonthName = now.toLocaleDateString('en-US', { month: 'long' })

const dayOfYear = (d: Date): number => {
  const start = new Date(d.getFullYear(), 0, 0)
  const diff = d.getTime() - start.getTime()
  return Math.floor(diff / 86400000)
}

const daysInYear = (year: number): number => {
  return ((year % 4 === 0 && year % 100 !== 0) || year % 400 === 0) ? 366 : 365
}

const expectedMonthlyPct = computed((): number => {
  const daysInMonth = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate()
  return (now.getDate() / daysInMonth) * 100
})

const expectedYearlyPct = computed((): number => {
  return (dayOfYear(now) / daysInYear(now.getFullYear())) * 100
})

// Upstream goals.*.progress_mi can lag behind the authoritative
// month_total_mi / year_total_mi from the same payload. Prefer the totals and
// recompute percent so the GOALS section stays in sync with the values shown
// directly above it.
const monthlyDisplay = computed((): GoalProgress | null => {
  const g = streakData.value?.goals?.monthly
  if (!g) return null
  const progress_mi = streakData.value?.month_total_mi ?? g.progress_mi
  const percent = g.goal_mi > 0 ? (progress_mi / g.goal_mi) * 100 : 0
  return { ...g, progress_mi, percent }
})

const yearlyDisplay = computed((): GoalProgress | null => {
  const g = streakData.value?.goals?.yearly
  if (!g) return null
  const progress_mi = streakData.value?.year_total_mi ?? g.progress_mi
  const percent = g.goal_mi > 0 ? (progress_mi / g.goal_mi) * 100 : 0
  return { ...g, progress_mi, percent }
})

const monthlyPaceDelta = computed((): number | null => {
  const pct = monthlyDisplay.value?.percent
  return pct !== undefined ? pct - expectedMonthlyPct.value : null
})

const yearlyPaceDelta = computed((): number | null => {
  const pct = yearlyDisplay.value?.percent
  return pct !== undefined ? pct - expectedYearlyPct.value : null
})

// Checkmark next to "This month" / "This year" totals fires only when the
// active goal is met (falls back to legacy 100/1200 mi if no goal payload).
const monthGoalMet = computed((): boolean => {
  const total = streakData.value?.month_total_mi ?? 0
  const goal = streakData.value?.goals?.monthly?.goal_mi ?? 100
  return total >= goal
})

const yearGoalMet = computed((): boolean => {
  const total = streakData.value?.year_total_mi ?? 0
  const goal = streakData.value?.goals?.yearly?.goal_mi ?? 1200
  return total >= goal
})

const monthlyMilesDelta = computed((): number | null => {
  const delta = monthlyPaceDelta.value
  const goal = monthlyDisplay.value?.goal_mi
  if (delta === null || goal === undefined) return null
  return (delta / 100) * goal
})

const yearlyMilesDelta = computed((): number | null => {
  const delta = yearlyPaceDelta.value
  const goal = yearlyDisplay.value?.goal_mi
  if (delta === null || goal === undefined) return null
  return (delta / 100) * goal
})

const formatMilesDelta = (milesDelta: number | null): string => {
  if (milesDelta === null) return ''
  const abs = Math.abs(milesDelta).toFixed(1)
  if (milesDelta >= 0.1) return `${abs} mi ahead of pace`
  if (milesDelta <= -0.1) return `${abs} mi behind pace`
  return 'on pace'
}

const getPaceColor = (delta: number | null): string => {
  if (delta === null) return 'text-gray-500 dark:text-gray-400'
  if (delta >= 0.5) return 'text-green-600 dark:text-green-400 font-medium'
  if (delta <= -5) return 'text-red-600 dark:text-red-400 font-medium'
  if (delta <= -0.5) return 'text-amber-600 dark:text-amber-400 font-medium'
  return 'text-gray-500 dark:text-gray-400'
}

const getProgressBarColor = (percent: number, delta: number | null): string => {
  if (percent >= 100) return 'bg-green-500 dark:bg-green-400'
  if (delta === null) return 'bg-blue-500 dark:bg-blue-400'
  if (delta >= 0.5) return 'bg-green-500 dark:bg-green-400'
  if (delta <= -5) return 'bg-red-500 dark:bg-red-400'
  if (delta <= -0.5) return 'bg-amber-500 dark:bg-amber-400'
  return 'bg-blue-500 dark:bg-blue-400'
}

onMounted(() => {
  fetchStreakData()
})
</script>

<style scoped>
.flip-counter {
  display: inline-flex;
  gap: 3px;
  padding: 6px;
  background: linear-gradient(180deg, #1a1a1a 0%, #0d0d0d 100%);
  border-radius: 8px;
  box-shadow:
    0 4px 6px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.flip-digit {
  position: relative;
  width: 36px;
  height: 52px;
  background: linear-gradient(180deg, #2a2a2a 0%, #1a1a1a 49%, #0f0f0f 51%, #1a1a1a 100%);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow:
    0 2px 4px rgba(0, 0, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.digit-value {
  font-family: 'Roboto Mono', 'SF Mono', 'Monaco', 'Consolas', monospace;
  font-size: 32px;
  font-weight: 700;
  color: #ffffff;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  line-height: 1;
}

.digit-divider {
  position: absolute;
  left: 0;
  right: 0;
  top: 50%;
  height: 1px;
  background: rgba(0, 0, 0, 0.6);
  box-shadow: 0 1px 0 rgba(255, 255, 255, 0.05);
}
</style>
