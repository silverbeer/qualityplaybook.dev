---
title: "4,107 Days of Running: One Commit at a Time"
date: 2025-11-20
tags: [Running, CLI, Side Projects, Automation]
excerpt: "I've run every single day for over 11 years. Here's how I built a CLI to track my obsession, because Strava is for people who touch grass voluntarily."
author: Quality Playbook
---

# 4,107 Days of Running: One Commit at a Time

Let me tell you about my longest-running production system.

No, not a Kubernetes cluster. Not a CI/CD pipeline. Not even that one cron job everyone's afraid to touch.

I'm talking about my **running streak**: 4,107 consecutive days of running. That's every single day since August 24, 2014. Through blizzards. Through 100°F heat. Through that time I had food poisoning in Mexico City (0/10, would not recommend).

## The Problem

Like any self-respecting engineer, I couldn't just *run*. I needed data. Metrics. Dashboards. So I've been logging every run to [SmashRun](https://smashrun.com) for years.

But here's the thing—I don't want to open a browser. I don't want to click through UI. I live in the terminal. My IDE is Vim. My git commits have better prose than my text messages.

When I want to check my streak, I want to type:

```bash
stk streak
```

Not open Chrome, wait for JavaScript to load, click three buttons, and see my stats rendered in a font that's probably Helvetica but might be Arial and I'll never know.

## The Solution: MyRunStreak CLI

So I built `stk` — a terminal-native CLI for runners who think `curl` is a perfectly acceptable way to check the weather.

```bash
╭────────────────────────────── stk ──────────────────────────────╮
│                                                                  │
│          )  (                                                    │
│         (   ) )                                                  │
│          ) ( (                                                   │
│         (  )  )                                                  │
│        .-'''''`-.                                                │
│       ,'         `.                                              │
│      /   LEGEND   \                                              │
│     :    4107d     :                                             │
│      \           /                                               │
│       `._______.'                                                │
│                                                                  │
│ Current Streak: 4107 days                                        │
│                                                                  │
╰──────────────────────────────────────────────────────────────────╯
```

Yes, that's ASCII art. Yes, it's a trophy. No, I will not apologize.

## Features for the Terminal-Obsessed

### Check Your Stats

```bash
$ stk stats

       Overall Statistics
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Metric           ┃       Value ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ Total Runs       │       4,535 │
│ Total Distance   │ 11,041.5 mi │
│ Average Distance │     4.97 mi │
│ Longest Run      │    26.79 mi │
│ Average Pace     │    8:48 /mi │
└──────────────────┴─────────────┘
```

11,000+ miles. That's roughly the distance from Boston to Tokyo and back. On foot. One painful mile at a time.

### Sync From SmashRun

```bash
$ stk sync --year 2014
ℹ Syncing year 2014
  Found 156 runs  ━━━━━━━━━━━━━━━━━━━ 100%
  Stored 156 runs ━━━━━━━━━━━━━━━━━━━ 100%
✓ Synced 156 runs
```

OAuth, token refresh, pagination—all handled. You just type the command and go make coffee.

### Monthly Breakdowns

```bash
$ stk monthly

┏━━━━━━━━━┳━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━┓
┃ Month   ┃ Runs ┃    Total ┃     Avg ┃ Pace ┃
┡━━━━━━━━━╇━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━┩
│ 2025-11 │   20 │  66.4 mi │ 3.32 mi │ 9:27 │
│ 2025-10 │   31 │ 100.5 mi │ 3.24 mi │ 9:15 │
│ 2025-09 │   30 │ 100.2 mi │ 3.34 mi │ 9:26 │
└─────────┴──────┴──────────┴─────────┴──────┘
```

## The Tech Stack (Because You Were Going to Ask)

- **Python 3.12** with UV (because `pip` is so 2019)
- **Typer** for the CLI framework
- **Rich** for those beautiful tables and ASCII art
- **Supabase** for the database (Postgres + RLS)
- **AWS Lambda** for the API (container-based, because dependencies)
- **Pydantic v2** for all the data models
- **SmashRun API** for the data source

The whole thing is a love letter to modern Python tooling. Type hints everywhere. Ruff for linting. Pytest for testing. If it doesn't pass `mypy --strict`, it doesn't ship.

## The Hardest Bug

You want to know what broke my streak calculation? Timezone handling.

I run at 11 PM sometimes (don't judge me, I have kids). SmashRun sends `startDateTimeLocal: "2023-03-05T23:52:00-05:00"`. PostgreSQL stores it as UTC. The `DATE()` function extracts March 6th.

My 4,000+ day streak showed as 991 days because of five runs stored on the wrong date.

The fix? Extract the date from local time *before* any timezone conversion:

```python
local_dt = activity.start_date_time_local
start_date = local_dt.date().isoformat()  # March 5th, not March 6th
```

Timezones: undefeated since 1883.

## Why a CLI?

Look, I get it. Normal people use apps. Normal people like buttons and colors and notifications that remind them to "crush their goals."

I'm not normal people. I want to:

- Check my streak without leaving my terminal
- Pipe output to other commands (`stk stats --json | jq`)
- Script my own dashboards
- Not have my running data harvested for targeted ads

If that sounds like you, maybe give `stk` a try.

## What's Next

I'm working on [myrunstreak.com](https://myrunstreak.com) — a web dashboard for the normies in my life who want to see my streak but refuse to `ssh` into my server. It'll pull from the same data, just with more CSS and less `vim`.

But the CLI will always be the first-class citizen. Because some of us prefer our dopamine hits in monospace.

## Update: "Did I Run Today?" Tile

I couldn't resist. You can now see my streak status in real-time right here on [qualityplaybook.dev](/).

Look for the **"Did I Run Today?"** tile on the homepage. It shows:
- Whether I've logged a run today (spoiler: yes)
- My current streak count
- Live data pulled from my running API

### The Serverless Stack

This was a fun excuse to build more AWS infrastructure:

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  EventBridge    │────▶│  Lambda          │────▶│  S3 Bucket      │
│  (scheduled)    │     │  (Python 3.12)   │     │  (static JSON)  │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
     ↑ twice daily             │                          │
     │ (9am + 12pm EST)        │ fetch from               │
     │                         │ SmashRun API             ▼
     │                         │                 ┌─────────────────┐
     │                         ▼                 │  CloudFront     │
                        ┌──────────────┐        │  (CDN + cache)  │
                        │ Check if     │        └─────────────────┘
                        │ run logged   │                 │
                        │ today        │                 ▼
                        └──────────────┘        qualityplaybook.dev
```

**100% Infrastructure as Code** using OpenTofu:

```hcl
schedules = [
  {
    name        = "morning-sync"
    expression  = "cron(0 14 * * ? *)"  # 9am EST
    description = "Morning sync check"
  },
  {
    name        = "midday-sync"
    expression  = "cron(0 17 * * ? *)"  # 12pm EST
    description = "Midday sync check"
  }
]
```

The Lambda checks SmashRun, writes a simple JSON to S3, and CloudFront serves it globally with caching. Total AWS cost? About **$0.50/month**.

### Why Twice a Day?

Morning run? Caught by the 9am sync. Afternoon run? Caught by noon. Most of my runs happen before lunch anyway, but the second sync is insurance.

And yes, if I run at 11 PM (don't judge), the tile won't update until the next morning. I can live with that—the streak still counts.

## The Streak Continues

4,107 days. That's:

- 11 years, 2 months, and 27 days
- 2 different jobs
- 1 pandemic
- 3 pairs of knees (kidding... mostly)

Tomorrow it'll be 4,108. Then 4,109. The streak doesn't care about your excuses.

Neither do I.

```bash
$ stk streak
Current Streak: 4107 days

$ # See you tomorrow
```

---

*Interested in the code? It's built with the same quality engineering principles I write about here. Maybe I'll open-source it once I clean up those TODO comments. You know, the ones that say "fix this properly later" from 6 months ago.*
