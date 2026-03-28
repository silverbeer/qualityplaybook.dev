---
title: "MissingTable Q1 2026: Playoffs, AI Scrapers, Club Logos, and Scoring Matches From Your Phone"
date: 2026-03-28
tags: [MissingTable, AI Agents, Soccer, Kubernetes, Python, Quality Engineering, OpenClaw]
excerpt: "Three months of shipping: live match scoring, an autonomous AI scraper, a RADIUS-controlled LLM proxy, club logos, playoff brackets, and a Telegram bot that lets you score matches from the sideline."
author: Quality Playbook
---

# MissingTable Q1 2026: Playoffs, AI Scrapers, Club Logos, and Scoring Matches From Your Phone

It's been almost three months since I [introduced quality.missingtable.com](/blog/introducing-quality-missingtable-dashboard). That post was about CI infrastructure. This one is about what happens when you spend a youth soccer season actually *using* the platform you built—and keep adding features every time you hit a wall at the field.

Here's everything that shipped since January 4th across MissingTable, match-scraper, match-scraper-agent, missingtable-platform-bootstrap, iron-claw, and a new experiment called OpenClaw.

---

## MissingTable: The Platform Grows Up

### Live Match Scoring

The biggest UX leap of the quarter. Coaches and managers can now score matches in real time—goals go up as they happen, the scoreboard updates live, and anyone watching the app sees the score change without a refresh.

```
feat: Live match scoring with real-time updates (#174)
feat: Add team logos and fix scoreboard layout (#175)
```

This was the unlock that made everything else worth building. Once you can run the scoreboard from the sideline, you want to track *everything*.

### Player Stats, Rosters, and Lineups

With live scoring came the appetite for more: who scored? Who started? What cards did they pick up?

- **Roster management and player stats tracking** — goals, appearances, cards tracked per player
- **Pre-match starting lineup** with futsal support (7v7, 5v5)
- **Card events** — yellow and red cards recorded in the match timeline
- **Post-match stats editing** — fix anything you got wrong in the heat of the moment
- **Goal and card entry for teams without a roster** — no roster? No problem. Still records goals.

```
feat: Add player stats tracking and roster management (#177)
feat: Pre-match starting lineup with futsal support (#206)
feat: Add played tracking, card events, and post-match stats editing (#238)
feat: Allow goal and card entry for teams without a roster (#239)
```

### Playoffs and Forfeit Support

Spring season means playoff brackets. MissingTable now tracks the full playoff picture:

- **Playoff bracket tracking** — single-elimination bracket view
- **Forfeit support** — for league *and* playoff matches
- **Match type filter on goals leaderboard** — separate playoff scorers from regular season
- **Club managers can edit matches for their club's teams** — no more waiting for an admin

```
feat: Add playoff bracket tracking (#203)
feat: Add forfeit support for playoff matches (#213, #214)
feat: Playoff forfeit support and post-match stats editor (#215)
```

### Club Logo System

This one took a full day but it looks great. Clubs now have logos displayed across standings, match cards, and the scoreboard.

The pipeline:
1. `prep-logo.py` — takes a raw PNG, removes the background with `rembg`, generates xs/sm/md/lg sizes
2. Logos upload to Supabase storage and are served via the CDN
3. `ClubLogo` Vue component renders the right size for the context (thumbnail in standings vs. large on the scoreboard)

Multi-size logos mean mobile gets a 32px thumbnail instead of downloading a 512px logo it'll never render at full size.

```
feat: Add ClubLogo component and integrate across all views (#226)
feat: Multi-size club logo system for bandwidth optimization (#228)
```

### League Table: Form and Movement

The standings table now shows the last 5 results (W/D/L form) and position movement arrows (↑↓) compared to the previous week. On mobile portrait the extra columns collapse—no horizontal scroll on small screens.

```
feat: Add position movement indicators and last-5 form to league table (#231)
```

### Tournament Support

Just landed this week. Tournaments are now a first-class entity: multi-age-group support, real match counts per tournament, and a **Tournament Match Center** fan view where spectators can follow all the action in one place.

```
feat: add tournaments table and tournament columns to matches
feat: add TournamentDAO and tournament API endpoints
feat: add AdminTournaments component and wire into AdminPanel
feat: add TournamentMatchCenter fan view and Match Center tab
feat: support multiple age groups per tournament
feat: show real match counts in tournament list
```

### Forgot Password + Auth Improvements

The basic auth flow is now complete: forgot password triggers a Resend email with a reset link. Also added an admin **user login activity view** so I can see who's actually using the platform.

```
feat: Add forgot password flow with Resend email (#254)
feat: add admin user login activity view (#256)
```

### Async Match Processing with Celery

The match pipeline (scraper → RabbitMQ → MissingTable) now runs through a proper Celery worker in Kubernetes. Matches submitted by the scraper agent are processed asynchronously—no more blocking API calls.

```
feat: Enable Celery worker for match processing in LKE (#221)
fix: Consume matches.prod queue so MSA submissions are processed (#252)
```

### Other Notable Platform Fixes

- **Division filter** on the This Week matches view — helpful when tracking one division at a time
- **Reschedule handling** — matches that move dates update correctly instead of creating duplicates
- **Date/timezone off-by-one fix** — the classic "game was yesterday according to the app" bug
- **Browser cache headers** — API responses no longer get stale in the browser
- **Match cancellation endpoint** — `PATCH /api/agent/matches/cancel` for the audit pipeline

---

## Match Scraper: The Library

`match-scraper` (the Python library) had a busy quarter:

- **Crawl-based pagination** — replaced fragile upfront page count detection with crawl-as-you-go
- **Calendar date navigation rewrite** — always navigates to the target month correctly; the old index-based approach broke on certain months
- **Florida division support** — expanded beyond the Northeast
- **`discover` command** — scan available divisions without knowing them in advance
- **Pagination dedup** — stops re-processing matches seen on previous pages
- **`js-groups` attribute selector** — fixed a selector that broke when Bootstrap Select collided with the old index-based approach

```
fix: Rewrite calendar date navigation to always navigate to target month (#56)
fix: Add pagination dedup, Florida division support, and library architecture docs (#55)
feat: Add discover command and Florida to VALID_DIVISIONS (#54)
fix: Use select[js-groups] attribute instead of fragile index-based selector (#57)
```

---

## Match Scraper Agent: From LLM to Deterministic Planner

This is the project I'm most proud of this quarter. `match-scraper-agent` went from a sketch to a production Kubernetes CronJob that runs 8 times a day on weekends and twice a day on weekdays during match season.

### The Origin Story

The agent started as an LLM-driven system: give an AI model a set of scraping tools and let it figure out what to scrape. It worked, but it was expensive, slow, and non-deterministic — the same input could produce different scraping strategies on different runs.

### The Pivot: Deterministic Planner

In mid-March I replaced the LLM planning layer with a **rules-based deterministic planner**. The planner knows:

- Which divisions to scrape and when
- Which date windows to look at (weekends vs. weekdays)
- Whether a given match in MissingTable already has a score, kickoff time, or lineup

The LLM is still involved—but only for natural language interpretation and report writing, not for planning. The scraper always does the same thing given the same inputs.

```
feat: Deterministic scrape planner replaces LLM decision-making
feat: Replace PydanticAI with pipeline-based rules engine (#42)
```

### Audit Module

One of the trickier problems: after scraping, how do I know the data in MissingTable is *correct*? Scores get entered wrong. Home and away teams get swapped. Kickoff times are missing.

The audit module compares scraped data against what's in MissingTable and flags discrepancies:

- `missing_in_mt` — scraped match doesn't exist in MT
- `score_mismatch` — scores differ between scraper and MT
- `home_away_swapped` — teams are reversed
- `extra_in_mt` — match in MT but not found in scraper (auto-cancelled after 7 days)

```
feat: Add audit module for Northeast HG data-integrity auditing (#39)
feat: Detect home/away team swaps in audit + add --team/--age-group CLI override
feat: Auto-cancel extra_in_mt matches older than 7 days (#43)
feat: Batch audit runs (--count) and remove weekly FULL_SYNC
feat: Add audit-report command for HG Northeast coverage tracking
```

### Telegram Reports

After every agent run, a Telegram message lands on my phone summarizing what happened: how many matches were scraped, what was submitted, what was cancelled, and any audit findings. If Telegram delivery fails, it falls back to Resend email.

```
feat: Add Telegram run summary report after each agent run (#26)
feat: Add Resend email fallback when Telegram fails (#48)
```

### Division Expansion

The agent now covers U13, U14, U15, and U16 in both Florida and HG Northeast — with dedicated backfill scripts for bootstrapping each new division at the start of the season.

---

## missingtable-platform-bootstrap: Off DigitalOcean, Onto Linode

In late January I migrated the production cluster from DigitalOcean Kubernetes (DOKS) to **Linode Kubernetes Engine (LKE)**. Cost-driven: same specs, lower monthly bill.

In March: **cert-manager** for automatic TLS certificate management, and **UptimeRobot** for external uptime monitoring. The CI pipeline now supports Linode natively in the Kubernetes infra workflow.

```
feat: Migrate from DOKS to Linode Kubernetes Engine (LKE) (#25, #26)
feat: Add cert-manager for automatic TLS certificate management on LKE (#27)
feat: Add UptimeRobot monitoring for missingtable.com (#28)
```

---

## Iron-Claw: A RADIUS-Controlled LLM Proxy

Side project that became infrastructure. `iron-claw` is a local LLM proxy that sits between clients (Claude Code, OpenClaw, any OpenAI-compatible tool) and the upstream APIs. It enforces a monthly token budget using **FreeRADIUS**—the same protocol ISPs use to control internet access.

How it works:

1. Every LLM request goes through the iron-claw proxy
2. The proxy checks FreeRADIUS: does this session have budget remaining?
3. If yes: forward the request, deduct tokens
4. If no (or approaching the limit): throttle or block

The throttle ladder means I don't hit a hard wall — it slows things down as the budget runs low, which is the right behavior for a side project that doesn't need to burn API credits at 3 AM.

A **monitor TUI** shows live proxy policy state, active sessions, and budget burn in real time.

```
feat: Add LLM proxy server (Phase 1: bare pipe, no RADIUS)
feat: Add RADIUS session lifecycle to proxy (Phase 2)
feat: Add throttle ladder enforcement + /status endpoint (Phase 3)
feat: Add monitor-only policy mode for observability without enforcement
feat: Add real-time log monitor TUI
feat: Add OpenAI provider support to LLM proxy (#12)
```

Iron-claw runs in K3s alongside the rest of the local stack.

---

## OpenClaw + Telegram: Scoring Matches From Your Phone

This is the experiment I'm most excited to keep building.

**OpenClaw** is a local AI agent gateway — a personal AI that lives on your machine, stays connected to Telegram, Discord, and other messaging platforms, and acts on your behalf. My agent is named Claw.

The use case: I'm a parent at youth soccer matches, and I wanted a way to score a game and broadcast live updates without pulling out a laptop. Just a phone in my pocket and a Telegram DM.

### How It Works

```
Field → Telegram DM → Claw → MT CLI → MissingTable API → Discord + Telegram group
```

From my phone, I DM `@mt_match_bot` on Telegram:

```
> Start match 1186
> Goal home Matt
> Goal away #7
> Halftime
> Second half
> What's the score?
> Game over
```

Claw translates each message into an MT CLI command:

```bash
uv run mt match start 1186
uv run mt match goal --team home --player "Matt"
uv run mt match status
# ...
```

After each event, Claw broadcasts to **Discord #live-matches** and the **IFA Live Matches Telegram group** — so everyone following the match sees updates in real time.

### First Test Run (Feb 20, Match 1186)

- ✅ Match kicked off, status: live
- ✅ Goal recorded (home, #10, 19') → TSC A-Team 1-0
- ✅ Goal recorded (away, #4, 29') → TSC A-Team 1-1
- ✅ Goal recorded (home, #33, 42') → TSC A-Team 2-1
- ✅ Discord #live-matches received updates
- ✅ Telegram "IFA Live Matches" group received updates

A few things needed fixing: Telegram bot privacy mode was ON (disabled via BotFather), and cross-context messaging needed an explicit config flag. Both minor. The flow works.

The `telegram-notify` Python package I extracted during this work is now a standalone library used by both OpenClaw and match-scraper-agent.

---

## What's Next

There's no shortage of things to build. A few things I'm thinking about:

- **Card tracking in the Telegram flow** — "Yellow card home #5" should work the same as goal recording
- **Full halftime/match-end testing** — the Feb 20 test run didn't get that far
- **Audit coverage expansion** — more divisions, automated correction instead of just flagging
- **Tournament bracket view in the fan-facing app** — the admin side is done, the public view is next

The season is running. The scraper is running. The platform is running. Now I'm just trying to keep up with the data.

---

*MissingTable is a youth soccer platform I'm building as a parent who likes to nerd out with Claude Code. If you're curious about the stack (FastAPI, Vue 3, Supabase, k3s, Celery, RabbitMQ), I'm always happy to talk shop on [LinkedIn](https://www.linkedin.com/in/tomdrake-qe).*
