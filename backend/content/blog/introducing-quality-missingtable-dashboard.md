---
title: "Introducing quality.missingtable.com: A Serverless Quality Dashboard Built with 100% IaC"
date: 2026-01-04
tags: [Quality Engineering, AWS, Infrastructure as Code, Ansible, Testing, Serverless]
excerpt: "A deep dive into building a low-cost serverless quality reporting solution using AWS S3, CloudFront, and GitHub Actions—with an honest confession about why I used Ansible."
author: Quality Playbook
---

# Introducing quality.missingtable.com: A Serverless Quality Dashboard Built with 100% IaC

I'm excited to share [quality.missingtable.com](https://quality.missingtable.com)—a live quality dashboard for the Missing Table project. But more than the dashboard itself, I want to share the journey of building the infrastructure behind it.

## The Challenge

I needed a way to:
- Run comprehensive test suites on every push
- Generate beautiful, browsable reports (Allure, coverage HTML)
- Track test history and detect regressions
- Keep costs minimal (this is a side project, after all)

The solution? A 100% serverless reporting platform built entirely with Infrastructure as Code.

## The Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  GitHub Push    │────▶│  EC2 Runner      │────▶│  S3 Bucket      │
│  (any branch)   │     │  (self-hosted)   │     │  (static host)  │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                               │                          │
                               │ pytest, vitest           │
                               │ allure generate          │
                               │ coverage reports         ▼
                               │                 ┌─────────────────┐
                               │                 │   CloudFront    │
                               ▼                 │   (CDN + HTTPS) │
                        ┌──────────────┐        └─────────────────┘
                        │ Allure       │                 │
                        │ Reports      │                 │
                        │ Coverage     │                 ▼
                        │ Dashboard    │        quality.missingtable.com
                        └──────────────┘
```

### The Stack

| Component | Technology | Cost |
|-----------|------------|------|
| CI Runner | EC2 t3.small (self-hosted) | ~$15/month |
| Report Storage | S3 | ~$0.50/month |
| CDN + HTTPS | CloudFront | ~$1/month |
| DNS | Route53 | $0.50/month |
| **Total** | | **~$17/month** |

Compare this to managed CI/CD solutions that can easily run $50-100+/month for similar capabilities.

## 100% Infrastructure as Code

Everything is codified. No clicking around in the AWS console.

### S3 + CloudFront (Terraform)

```hcl
resource "aws_s3_bucket" "quality_reports" {
  bucket = "quality-missingtable-com"
}

resource "aws_cloudfront_distribution" "quality_cdn" {
  origin {
    domain_name = aws_s3_bucket.quality_reports.bucket_regional_domain_name
    origin_id   = "S3-quality-reports"
  }

  default_cache_behavior {
    viewer_protocol_policy = "redirect-to-https"
    # ... caching config
  }

  aliases = ["quality.missingtable.com"]
}
```

### GitHub Actions Workflow

The [quality.yml](https://github.com/silverbeer/missing-table/blob/main/.github/workflows/quality.yml) workflow runs on every push:

```yaml
name: Publish Quality Reports
on:
  push:
    branches: ['**']  # Every branch gets quality reports

jobs:
  publish-quality:
    runs-on: [self-hosted, quality-runner]
    steps:
      - name: Run backend tests with Allure
        run: |
          cd backend
          uv run pytest tests/ -m unit \
            --cov=. --cov-report=html \
            --alluredir=allure-results
          allure generate allure-results -o allure-report

      - name: Upload to S3
        run: |
          aws s3 sync backend/allure-report/ \
            s3://quality-missingtable-com/latest/allure/
```

## The Ansible Confession

Here's where I get honest: **I used Ansible to configure the EC2 runner.**

Why? Let me be transparent:

1. **Learning refresh** - I used Ansible heavily 8 years ago for configuration management of production EC2 fleets. It's been a while, and I wanted to dust off those skills.

2. **Interview preparation** - Ansible still comes up in DevOps and SDET interviews. Having recent, hands-on experience matters.

3. **It's actually the right tool** - For configuring a single runner with specific software (Python, Node.js, Allure CLI, AWS CLI), Ansible is clean and repeatable.

### The Playbook

```yaml
# ansible/playbooks/configure-runner.yml
---
- name: Configure GitHub Actions Runner
  hosts: quality_runner
  become: yes

  tasks:
    - name: Install Python 3.13
      apt:
        name: python3.13
        state: present

    - name: Install Node.js 20
      shell: |
        curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
        apt-get install -y nodejs

    - name: Install Allure CLI
      unarchive:
        src: "https://github.com/allure-framework/allure2/releases/download/{{ allure_version }}/allure-{{ allure_version }}.tgz"
        dest: /opt/
        remote_src: yes

    - name: Install uv (Python package manager)
      shell: curl -LsSf https://astral.sh/uv/install.sh | sh

    - name: Configure GitHub Actions runner
      include_role:
        name: github-actions-runner
```

Could I have used a pre-built AMI or Docker? Sure. But I wanted that muscle memory back—and now I have a reproducible runner I can tear down and rebuild in minutes.

## Test Types on the Dashboard

The dashboard showcases multiple testing approaches, each serving a specific purpose:

### Backend Unit Tests (pytest + Allure)

Traditional unit tests with rich reporting via Allure decorators:

```python
@allure.suite("Parameterized Tests")
@allure.feature("Security")
@allure.story("Team Management Permissions")
class TestTeamManagementMatrix:
    @pytest.mark.parametrize("scenario", PERMISSION_SCENARIOS)
    def test_can_manage_team(self, scenario):
        # 33 scenarios covering all role combinations
        pass
```

### Frontend Unit Tests (Vitest)

Vue component tests with coverage tracking:

```javascript
describe('MatchesView', () => {
  it('renders match list correctly', () => {
    const wrapper = mount(MatchesView)
    expect(wrapper.findAll('.match-card')).toHaveLength(10)
  })
})
```

### Parameterized Tests

Three innovative approaches I'm particularly proud of:

1. **Authorization Matrix Testing** - 33 scenarios testing every role/permission combination
2. **YAML-Driven Validation** - 92 test cases loaded from human-readable YAML files
3. **League Table Scenarios** - 12 business rule scenarios as executable documentation

### API Tests

Contract testing against the FastAPI backend, verifying response schemas and status codes.

### User Journey Tests (TSC)

The **Test Scenario Chain** tests are comprehensive end-to-end journeys that test the entire application flow with real API calls against production:

```python
# tests/tsc/test_01_club_manager.py
class TestClubManagerJourney:
    """Complete club manager workflow as a user journey."""

    def test_01_club_manager_signup(self, tsc_context):
        """Club manager creates account and gets approved."""
        # Real signup, email verification, admin approval

    def test_02_create_team(self, tsc_context):
        """Club manager creates their first team."""
        # Creates team, assigns players

    def test_03_manage_roster(self, tsc_context):
        """Club manager manages team roster."""
        # Add players, set jersey numbers, customize profiles
```

These tests run against the live API and cover:
- **Admin Setup** - Initial data and user creation
- **Club Manager Journey** - Full club management workflow
- **Team Manager Journey** - Team-specific operations
- **Player Journey** - Player customization and profile management
- **Fan Journey** - Read-only user interactions

Each journey test creates its own test data with a unique prefix (`tsc_ci_`), runs through the complete workflow, and cleans up after itself.

## The Learning Foundation

Here's the honest truth: Missing Table doesn't *need* 90% test coverage. It's a side project for tracking youth soccer standings.

But that's not the point.

I'm using MT as my **learning laboratory**—a real codebase where I can:

- Experiment with innovative testing patterns
- Build skills that transfer to enterprise environments
- Create portfolio pieces that demonstrate capability
- Stay sharp for technical interviews

The goal isn't just high coverage numbers. It's **learning and innovating my way there**.

Every test type on that dashboard represents something I've learned or re-learned:
- Allure decorators for rich reporting
- pytest parametrization patterns
- YAML-driven test specifications
- Terraform for AWS infrastructure
- Ansible for server configuration
- GitHub Actions self-hosted runners

## What's Next

I'm laying the foundation for even more:

- **Visual regression testing** with Playwright screenshots
- **Performance baselines** tracking API response times
- **Mutation testing** to verify test quality
- **AI-assisted test generation** using the parameterized patterns

## Try It Yourself

Visit [quality.missingtable.com](https://quality.missingtable.com) to see:

- **Backend Allure Report** - Drill into test suites, see parameterized scenarios
- **Backend Coverage** - Line-by-line coverage visualization
- **Frontend Vitest Report** - Component test results
- **Frontend Coverage** - Vue component coverage
- **User Journey Tests** - End-to-end workflow validations

Every push to any branch triggers a fresh report. The dashboard shows history, regression detection, and suite-by-suite breakdowns.

## The Real Value

Building this dashboard taught me more than any tutorial:

- **Terraform** for AWS resource management
- **CloudFront** cache invalidation patterns
- **S3** static website hosting with custom domains
- **Ansible** for reproducible server configuration
- **GitHub Actions** self-hosted runner architecture
- **Allure** framework integration and customization

That's the quality playbook approach: **learn by building real things**.

---

Have questions about the setup? Want to build something similar? Check out the [source code](https://github.com/silverbeer/missing-table) or reach out via the [contact page](/contact).

*The infrastructure code is in a private repo, but I'm happy to share specifics if you're building something similar.*
