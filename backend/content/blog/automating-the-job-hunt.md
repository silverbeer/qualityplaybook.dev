---
title: "Automating the Job Hunt: Claude Code, Gmail, and the Engineering Mindset"
date: 2025-12-05
tags: ["automation", "claude-code", "ai", "python", "job-hunting", "mcp", "cli", "duckdb"]
description: "Finding a new job is a full-time job. So I built a CLI tool and Claude Code slash command to automate my job application tracking. Here's how."
---

> "Friends don't let friends run manual processes."

I'm on the job hunt. Still.

If you've been through this recently, you know: **finding a new job is a full-time job**. LinkedIn applications. Company portals. Recruiter emails. Confirmation emails from 47 different ATS systems. And then — because you're collecting unemployment — you need to document every single application for your weekly certification.

After the third week of manually copying job titles from Gmail into a spreadsheet, my engineering brain screamed: *"There has to be a better way."*

So I built one.

---

## The Problem

Every week, my unemployment certification asks:
- How many jobs did you apply to?
- What companies?
- What dates?

And every week, I'd:
1. Open Gmail
2. Search for "application received" or "thank you for applying"
3. Scroll through LinkedIn confirmation emails
4. Copy company names and dates into... somewhere
5. Repeat next week

**Time spent:** 30-45 minutes per week of mind-numbing copy-paste.

**Error rate:** High. Did I already log that one? Was that this week or last week?

**Frustration level:** Through the roof.

---

## The Solution: job-log

I built a simple CLI tool called [job-log](https://github.com/silverbeer/job-log) — a local DuckDB database with a Python CLI for tracking job applications.

Why DuckDB? It's fast, it's simple, it's embeddable, and honestly — **it has a cool name**. 🦆

```bash
# Add a job
uv run python src/job_log/cli.py add "Acme Corp" "Senior Engineer"

# Mark it as applied
uv run python src/job_log/cli.py apply 1 --date "2025-12-05"

# Search your history
uv run python src/job_log/cli.py search "Acme"

# List recent applications
uv run python src/job_log/cli.py list --status applied
```

Simple. Local. Fast. No SaaS subscription. No data leaving my machine.

But here's where it gets interesting...

---

## Enter Claude Code + MCP

I've been using [Claude Code](https://claude.ai/claude-code) as my daily coding companion. It's Anthropic's CLI for Claude — think AI pair programmer in your terminal.

Claude Code supports something called **MCP (Model Context Protocol)** — a way to give Claude access to external tools and data sources. One of those tools? **Gmail**.

*Wait... Claude can read my email?*

Yes. With your permission. And that unlocked something powerful.

---

## The Slash Command: `/scan-jobs`

Claude Code lets you create custom slash commands — reusable prompts stored as markdown files. I created `/scan-jobs`:

```markdown
# .claude/commands/scan-jobs.md

# Scan Gmail for Job Application Emails

Scan my Gmail for recent job application confirmation emails
and automatically add them to my job log.

## Usage
/scan-jobs [--days N]

## Workflow
1. Search Gmail for application emails (LinkedIn, Workday, Greenhouse, etc.)
2. Extract company name, job title, and date
3. Check if job already exists in database
4. Add new jobs automatically
5. Mark application confirmations as applied
6. Print summary
```

Now instead of 45 minutes of manual work, I run:

```bash
/scan-jobs --days 7
```

And Claude:
- Searches my Gmail for application confirmation emails
- Parses LinkedIn's "your application was sent to X" format
- Extracts company names from Workday, Greenhouse, and Lever emails
- Checks my database for duplicates
- Adds new jobs and marks them as applied
- Gives me a summary

**Time spent:** About 30 seconds.

---

## How It Works

### 1. Gmail MCP Integration

Claude Code connects to Gmail via MCP. In my `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gmail": {
      "command": "uvx",
      "args": ["mcp-gmail"]
    }
  }
}
```

This gives Claude access to Gmail search and read tools — with my explicit permission.

### 2. The Slash Command

The `/scan-jobs` command is a markdown file that tells Claude exactly what to do:

```markdown
## Email Pattern Recognition

- LinkedIn: "[Name], your application was sent to [Company]"
- Workday: "Thank you for applying to [Title] at [Company]"
- Greenhouse: "Thanks for your interest in [Company]!"
- Lever: "Your application to [Company]"
```

It knows how to parse different ATS email formats and extract the data I need.

### 3. The CLI Backend + DuckDB

The [job-log CLI](https://github.com/silverbeer/job-log) uses DuckDB as its data store. Why DuckDB?

- **Zero config** — No server, no setup, just a file
- **SQL power** — Full analytical SQL when you need it
- **Fast** — Columnar storage means lightning-fast aggregations
- **Portable** — Single file, works everywhere
- **Cool mascot** — I mean, look at that duck 🦆

```python
import duckdb

def add_job(company: str, title: str, ai_sourced: bool = False):
    conn = duckdb.connect('jobs.duckdb')
    conn.execute("""
        INSERT INTO jobs (company, title, ai_sourced, created_at)
        VALUES (?, ?, ?, NOW())
    """, [company, title, ai_sourced])
    return conn.execute("SELECT last_insert_rowid()").fetchone()[0]
```

When unemployment asks "how many jobs did you apply to this week?":

```sql
SELECT COUNT(*) FROM jobs
WHERE status = 'applied'
AND applied_date >= DATE_TRUNC('week', CURRENT_DATE)
```

DuckDB makes that instant, even with thousands of applications (not that I'm hoping to need that many).

---

## A Real Run

Here's what it looks like in practice:

```
> /scan-jobs --days 1

Scanning Gmail for job application emails...

Found 7 application emails:
- Initech - TPS Report Automation Architect (Dec 5)
- Hooli - Senior Vice President of Pivoting (Dec 4)
- Pied Piper - Middle-Out Compression Engineer (Dec 4)
- Umbrella Corp - Definitely Not Evil DevOps Lead (Dec 4)
- Cyberdyne Systems - Skynet Reliability Engineer (Dec 4)
- Dunder Mifflin - Assistant to the Regional SRE (Dec 4)
- Monsters Inc - Scream Infrastructure Engineer (Dec 5) [REJECTED]

Checking database...

## Summary

**Jobs Added:** 1
| Company | Title | Date |
|---------|-------|------|
| Initech | TPS Report Automation Architect | 2025-12-05 |

**Jobs Skipped (already in database):** 6
| Company | Status |
|---------|--------|
| Hooli | applied |
| Pied Piper | applied |
| Umbrella Corp | applied |
| Cyberdyne Systems | applied |
| Dunder Mifflin | applied |
| Monsters Inc | rejected |
```

One command. Seven emails processed. One new job added. Six duplicates skipped. Zero TPS report cover sheets required.

**That's the engineering mindset in action.**

---

## Why This Matters

This isn't about the specific tool. It's about the mindset.

### 1. Automate Repetitive Tasks

If you're doing something manually more than twice, automate it the third time. That's not laziness — that's efficiency.

### 2. Use the Right Tools

Claude Code + MCP is a force multiplier. I didn't have to build Gmail parsing, OAuth flows, or email search. I just connected existing tools.

DuckDB is the right database for this: powerful enough for real SQL queries, simple enough that it's just a file.

### 3. Keep It Simple

`job-log` is ~300 lines of Python. DuckDB database. Click CLI. Rich console output. No framework. No cloud. No complexity.

### 4. Solve Your Own Problems

The best side projects solve problems you actually have. I needed to track job applications. Now I have a tool that does it in seconds.

---

## The Irony

I'm using my engineering skills to optimize the process of finding my next engineering job.

There's something poetic about that.

And honestly? Building this tool was more fun than filling out my 47th Workday application. At least I learned something new.

---

## Try It Yourself

The code is open source: **[github.com/silverbeer/job-log](https://github.com/silverbeer/job-log)**

The [README](https://github.com/silverbeer/job-log#readme) has detailed setup instructions covering:

1. **Clone and install** — Uses `uv` for dependency management
2. **Google Cloud setup** — Creating OAuth credentials for Gmail API access
3. **Gmail MCP server** — Options for connecting Claude Code to your inbox
4. **Claude Code configuration** — Wiring up the MCP server
5. **Database location** — Optional iCloud/Dropbox sync for multi-device access

The setup takes about 15 minutes if you're familiar with Google Cloud Console, longer if you're not. But you only do it once.

Fork it, adapt it, make it your own. The engineering mindset matters more than my specific implementation.

---

## The Tech Stack

For the curious:

- **[Claude Code](https://claude.ai/claude-code)** — AI coding assistant with MCP support
- **MCP Gmail** — Gmail integration via Model Context Protocol
- **Python 3.12** — Because we're not savages
- **[uv](https://github.com/astral-sh/uv)** — Modern Python package manager ([bye pip, hello uv](/blog/bye-pip-hello-uv))
- **Click** — CLI framework that doesn't make you cry
- **[DuckDB](https://duckdb.org/)** — The analytical database with the best mascot 🦆
- **Rich** — Pretty terminal output because we have standards

---

## The Engineering Quotes Wall

A few mantras I live by:

> "Friends don't let friends run manual processes."

> "The best time to automate was yesterday. The second best time is now."

> "If you're doing it twice, script it."

> "Automate yourself out of the boring stuff so you can focus on the interesting stuff."

---

## What's Next

I'm still job hunting. Still applying. Still building tools to make the process less painful.

And at least I'm not spending 45 minutes a week copying data from Gmail.

That time is better spent preparing for interviews, building portfolio projects, or writing blog posts about automating the job hunt.

If you're also in the trenches, hang in there. And maybe automate something while you're at it.

---

*I'm actively looking for leadership roles in SRE/Cloud Reliability and Quality Engineering. If you're hiring (or just want to chat about automation), connect with me on [LinkedIn](https://www.linkedin.com/in/tomdrake-qe).*

*Check out the code: [github.com/silverbeer/job-log](https://github.com/silverbeer/job-log)*
