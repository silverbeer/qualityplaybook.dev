---
title: "Resume as Code: I Built a GitOps Pipeline for My Job Search (And I'm Still Learning)"
date: 2025-11-06
tags: ["career", "devops", "ai", "python", "open-source", "job-search", "gitops"]
description: "Job hunting was crushing me. So I did what any DevOps engineer would do: I built a CI/CD pipeline for my resume. Here's what happened when I applied Infrastructure as Code principles to my career."
---

**Real talk:** Job hunting has been brutal.

I've got solid experience—Director-level SRE and QE leadership, hands-on Python development, CI/CD pipelines for everything from critical infrastructure to test automation (I once automated so much we joked about building pipelines to update your daily scrum status). On paper, I should be getting interviews. But LinkedIn applications? **Crickets.**

The rejections hit different when you've spent hours tailoring a resume only to get auto-rejected by an ATS system in 3 minutes. You start questioning everything: *Is my experience not relevant? Am I too senior? Not senior enough? Did I say "Kubernetes" enough times?*

Then one night, staring at my 47th Word document named `resume_final_v2_ACTUAL_final_use_this_one.docx`, I had a thought:

**If I manage infrastructure as code, why am I managing my resume as... whatever this is?**

---

## The Problem: Resume Management is Broken

Here's the reality of modern job searching:

1. **Every job needs a different resume.** SRE roles want reliability metrics and incident response. QE leadership roles want quality strategy and team building. SDET/IC roles want hands-on Python and test automation. I can do all three, but maintaining separate Word docs for each is madness.

2. **ATS systems are black boxes.** You know your resume got filtered, but *why*? Missing keywords? Wrong format? Too many pages? Who knows.

3. **Iteration is painful.** Found a better way to describe an achievement? Cool, now update it in 8 different documents. Hope you didn't miss any.

4. **Version control? LOL.** `resume_v3_updated_final_REALLY_final_2.docx` is not version control. It's chaos with better file names.

Sound familiar?

---

## The Solution: Resume as Code

So I built what any reasonable DevOps engineer would: **a GitOps workflow for my career.**

### The Core Idea

```yaml
# data/common/header.yml
name: "Your Name"
title: "Default Title"
contact:
  email: "you@example.com"
  github: "https://github.com/you"

# data/profiles/sdet/summary.yml (hands-on IC role)
content: >
  Lead CI/CD Automation Engineer with 10+ years
  hands-on Python development, test automation...

# data/profiles/sre-leadership/summary.yml
content: >
  Director of Site Reliability Engineering
  leading teams, 99.9% uptime, incident response...

# data/profiles/qe-leadership/summary.yml
content: >
  Director of Quality Engineering
  building scalable organizations, quality strategy...
```

**YAML-based resume data** with profile-specific overrides. Think Kubernetes ConfigMaps for your career.

**The beauty:** One set of experience data, multiple targeted presentations—SRE leader, QE leader, or hands-on IC. Same person, different lenses.

### The Workflow

```bash
# Find a job posting
pbpaste > data/profiles/sdet/job.txt

# Analyze with AI
uv run resume analyze sdet
# → Shows skill gaps, ATS match %, recommendations

# Build optimized resume
uv run resume build sdet --format both
# → Generates HTML + PDF

# Version control everything
git commit -m "Optimize SDET profile for Lead CI/CD Automation role"
```

**Infrastructure as Code patterns, applied to job searching.**

---

## The Tech Stack (Because Of Course)

- **Python + uv** – Modern package management (bye pip 👋)
- **Typer + Rich** – Beautiful CLI with progress bars
- **PydanticAI + OpenAI** – AI-powered job description analysis
- **Playwright** – PDF generation (no WeasyPrint native dependency hell)
- **Jinja2** – HTML templating
- **Git** – Actual version control

The whole thing is ~1,000 lines of Python, fully type-checked with mypy, linted with ruff, and 77 tests passing.

**Because if I'm building a tool to get a job, it better showcase the skills I'm claiming to have.**

---

## The Real Game-Changer: AI-Assisted Optimization

Here's where it gets interesting. I created a structured prompt for Claude Code:

```markdown
**Profile**: sdet
**Files provided**:
- data/profiles/sdet/job.txt (job description)
- data/profiles/sdet/fit.txt (ATS analysis)

Please update header.yml, summary.yml, experience.yml, and skills.yml
to maximize alignment with this role while maintaining authenticity.
```

Claude Code helps me:
1. **Extract ATS keywords** from job descriptions
2. **Identify skill gaps** (e.g., "You list TCP/IP but not DNS explicitly")
3. **Reframe achievements** to match job language
4. **Maintain honesty** (no fabricating experience)

### The Honesty Part is Critical

During optimization for a recent Lead CI/CD Automation Engineer role, I had to confront two gaps:

**Networking Experience:**
- **The lie:** "Strong TCP/IP, DHCP, VPN experience"
- **The truth:** "Application-level cloud networking (Route53, VPC, ALB/NLB, WAF)"

**Ansible Experience:**
- **The lie:** "Expert in Ansible"
- **The truth:** "Used Ansible 10 years ago on EC2. Now I use Terraform + Helm + K8s because, you know, containers happened."

Claude Code helped me reframe both honestly:

```yaml
# Before (overstated)
skills:
  - name: "TCP/IP"
    proficiency: "Advanced"
  - name: "Ansible"
    proficiency: "Advanced"

# After (truthful)
skills:
  - name: "AWS Cloud Networking (VPC, Route53, ALB/NLB)"
    proficiency: "Advanced"
  - name: "Terraform"
    proficiency: "Expert"
  - name: "Helm Charts & Kubernetes Manifests"
    proficiency: "Expert"
```

**The result:** A resume that's honest, strategic, and interview-ready. No lies to defend later.

---

## The Workflow in Practice

### Day 1: Found a Role
> Lead CI/CD Automation Software Engineer at a satellite communications company

Pasted job description into `data/profiles/sdet/job.txt`.

### Day 2: AI Analysis
Ran `uv run resume analyze sdet`:

```
ATS Match: 82-87%

Missing Keywords:
- Ansible (you have Terraform)
- Bash (you mention Python but not Bash explicitly)
- ELK (you use Grafana/Prometheus)
- On-call/RCA (you do this, not stated)
- Networking protocols (DNS, TCP/IP)
```

### Day 3: Optimization with Claude Code
Used the structured prompt. Claude Code:
- Rewrote summary to emphasize cloud networking
- Added "Partnered with Network Engineering..." bullet
- Restructured skills to prioritize job requirements
- Removed outdated Ansible claims, added modern K8s stack

**New ATS match: 90-94%** ✅

### Day 4: Built Resume
```bash
uv run resume build sdet --format both
# → output/sdet_resume.pdf ready to submit
```

### Day 5: Version Control
```bash
git add data/profiles/sdet/
git commit -m "Optimize SDET profile for Lead CI/CD Automation role

- Updated networking experience (cloud-focused)
- Removed stale Ansible, added Helm/K8s/ArgoCD
- Restructured skills to match job requirements
- ATS match: 90-94%"
```

**Everything is tracked. Every iteration documented.**

---

## What I've Learned

### 1. ATS Systems Are Real (And Beatable)

**Before Resume as Code:**
- Generic resume → Auto-reject in 3 minutes
- No idea what keywords were missing
- Frustration → desperation → imposter syndrome spiral

**After Resume as Code:**
- Targeted resume → ATS match 90%+
- Clear understanding of skill gaps
- Honest positioning → confidence in interviews

### 2. AI + Human = Strategic Truth-Telling

Claude Code doesn't just stuff keywords. It helps me **reframe experience honestly**.

**Example:**
- ❌ "I don't know DHCP" → Panic, lie on resume
- ✅ "I don't know DHCP, but I know cloud networking at the application level" → Honest positioning

The AI helps me see what I **actually have** vs. what I **think I'm missing**.

### 3. GitOps for Career = Clarity

Version controlling my resume means I can:
- **Track what works** (which framing gets interviews?)
- **A/B test approaches** (technical deep-dive vs. leadership focus)
- **Maintain multiple profiles** without Word doc hell
- **See my evolution** (`git log --oneline` = career journey)

### 4. The Tool Became My Portfolio

**Plot twist:** Resume as Code itself demonstrates the exact skills I'm applying for.

Every company sees:
- ✅ Modern Python development (Pydantic, Typer, type hints)
- ✅ AI integration (PydanticAI, structured prompts)
- ✅ DevOps thinking (GitOps, IaC patterns)
- ✅ CLI tool building (Rich, Playwright)
- ✅ Open source best practices (docs/, prompts/, tests/)

**The meta is strong:** I'm using the tool to find jobs where I can build tools like this.

### 5. I'm a Hybrid, and That's a Strength

The job market wants you to pick a lane: **Are you a leader or an IC? SRE or QE?**

But I'm both:
- 🎯 **SRE leadership** – I've led teams, established practices, achieved 99.9% uptime
- 🧪 **QE leadership** – I've built quality organizations, designed test strategies
- 💻 **Hands-on IC** – I write Python daily, build CLIs, automate everything

Resume as Code lets me present **all three versions** without lying or diluting my story. Same experience, different emphasis based on what the role needs.

**The reality:** The best SRE leaders can debug production. The best QE leaders can write test frameworks. And the best ICs understand the systems they're building for.

I don't want to pick a lane. I want to work where being a hybrid is an asset, not a compromise.

---

## The Honest Part: It's Still Hard

Let me be clear: **Resume as Code didn't magically get me a job.**

Job hunting is still:
- 😰 Emotionally draining
- ⏰ Time-consuming
- 🎲 Full of randomness (timing, budgets, internal candidates)
- 🤷 Often opaque (why no response after 3 rounds?)

What it **did** do:
- ✅ Give me back control of the process
- ✅ Help me see my strengths more clearly
- ✅ Reduce the anxiety of "did I send the right version?"
- ✅ Make iteration fast (minutes, not hours)
- ✅ Ensure honesty (no lies to defend in interviews)

**It's not a silver bullet. It's a better process.**

---

## Try It Yourself

Resume as Code is open source on GitHub: [github.com/silverbeer/resume-as-code](https://github.com/silverbeer/resume-as-code)

### Quick Start

```bash
# Clone the repo
git clone https://github.com/silverbeer/resume-as-code.git
cd resume-as-code

# Install dependencies
uv sync

# Install Playwright for PDF generation
uv run playwright install chromium

# List available profiles
uv run resume list-profiles

# Build a resume
uv run resume build test-ninja --format both
```

### Full Documentation

- 📖 [Complete Workflow Guide](https://github.com/silverbeer/resume-as-code/blob/main/docs/WORKFLOW.md) – 8-step process from job posting to submission
- 📝 [AI Optimization Prompt](https://github.com/silverbeer/resume-as-code/blob/main/prompts/optimize-profile-for-job.md) – Reusable prompt for Claude Code

### What You Get

- **Profile system** – Maintain multiple resume variations (SRE leadership, QE leadership, hands-on IC roles)
- **AI analysis** – Job description keyword extraction and skill gap analysis
- **Multi-format output** – HTML and PDF (ATS-friendly)
- **Version control** – Git-based workflow for resume data
- **Claude Code integration** – Structured prompts for AI-assisted optimization
- **Honest optimization** – Reframe experience truthfully, don't fabricate skills

---

## What's Next

I'm still job hunting. Still iterating. Still learning what works.

But I'm doing it with:
- ✅ A process that scales
- ✅ Version control that tracks progress
- ✅ AI assistance that keeps me honest
- ✅ Confidence that my resume represents me accurately

And maybe—just maybe—that's enough to beat the robots and land in front of an actual human who appreciates that I built a CI/CD pipeline for my career. 🤖

**If you're that human, [let's talk](https://linkedin.com/in/silverbeer).** 👋

---

## The Irony I Can't Ignore

I built a tool to optimize resumes while searching for a job.

The tool demonstrates exactly the skills I'm trying to prove I have.

I'm writing a blog post about building the tool to show I can communicate complex technical ideas.

**It's turtles all the way down, and I'm here for it.** 🐢

---

**Meta Note:** This entire blog post was written collaboratively with Claude Code. The human provided the experience, honesty, and emotion. Claude provided structure, clarity, and polish. Together, we told a true story about building tools to solve real problems.

Kind of like how Resume as Code actually works. 🚀

---

*Want to follow my journey? Subscribe at [qualityplaybook.dev](https://qualityplaybook.dev) or find me on [GitHub](https://github.com/silverbeer) where I'm building tools for quality engineering and DevOps.*

*Currently open to: SRE Leadership, QE/Quality Leadership, Lead SDET, or Senior IC roles where I can use Python to solve infrastructure and quality problems. I can lead teams or write code—ideally both.* 😄
