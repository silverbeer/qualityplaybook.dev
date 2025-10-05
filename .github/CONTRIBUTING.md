# Contributing to Quality Playbook

Thanks for your interest in contributing! This document outlines the development workflow.

## 🔒 Branch Protection

The `main` branch is protected and requires pull requests for all changes. Direct commits to `main` are not allowed.

## 🔄 Development Workflow

### 1. Create a Feature Branch

```bash
# Make sure you're on main and up to date
git checkout main
git pull origin main

# Create a new branch for your work
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
# or
git checkout -b post/new-blog-post
```

**Branch naming conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `post/` - New blog posts
- `docs/` - Documentation updates
- `chore/` - Maintenance tasks

### 2. Make Your Changes

Work on your branch with hot reload:

```bash
# Start development environment
./qp start --mode all

# Make changes to code or content
# Changes auto-reload in browser!

# Check status
./qp status
```

### 3. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "Add feature: description of what you did"

# Push to GitHub
git push origin feature/your-feature-name
```

**Commit message format:**
```
<type>: <short description>

<optional longer description>

<optional footer>
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks
- `post:` - New blog post

### 4. Create a Pull Request

Using GitHub CLI (recommended):

```bash
# Create PR from current branch
gh pr create --title "Your PR title" --body "Description of changes"

# Or use interactive mode
gh pr create --web
```

Using GitHub Web UI:
1. Go to https://github.com/silverbeer/qualityplaybook.dev
2. Click "Pull requests" → "New pull request"
3. Select your branch
4. Fill in title and description
5. Click "Create pull request"

### 5. Review and Merge

Since you're the sole contributor:
- Review your own changes in the PR
- Check that the PR template checklist is complete
- Merge when ready

```bash
# Merge via CLI
gh pr merge --squash  # Squash commits
# or
gh pr merge --merge   # Keep all commits
# or
gh pr merge --rebase  # Rebase commits
```

### 6. Clean Up

```bash
# After merging, delete the branch
git checkout main
git pull origin main
git branch -d feature/your-feature-name

# Delete remote branch (if not auto-deleted)
git push origin --delete feature/your-feature-name
```

## 📝 Adding Blog Posts

Blog posts follow the same PR workflow:

```bash
# Create a branch for your post
git checkout -b post/my-new-post

# Create the markdown file
touch backend/content/blog/my-new-post.md

# Add frontmatter and content
cat > backend/content/blog/my-new-post.md << 'EOF'
---
title: My New Post
date: 2025-10-05
tags: [Quality Engineering, Testing]
excerpt: A brief description of the post
author: Quality Playbook
---

# My New Post

Content goes here...
EOF

# Add images if needed
mkdir -p frontend/public/media/blog/my-new-post
cp ~/screenshot.png frontend/public/media/blog/my-new-post/

# Preview locally
./qp start --mode all
# Visit http://localhost:5173/blog/my-new-post

# Commit and create PR
git add .
git commit -m "post: Add blog post about topic"
git push origin post/my-new-post
gh pr create
```

## 🚀 Quick Reference

**Start working on new feature:**
```bash
git checkout main && git pull
git checkout -b feature/awesome-feature
./qp start --mode all
# ... make changes ...
git add . && git commit -m "feat: add awesome feature"
git push origin feature/awesome-feature
gh pr create
```

**View your PRs:**
```bash
gh pr list
gh pr view 123
```

**Check PR status:**
```bash
gh pr status
```

## 🔧 Testing Before PR

Always test your changes locally:

```bash
# Start services
./qp start --mode all

# Check both work
open http://localhost:5173      # Frontend
open http://localhost:8000/docs # Backend API

# View logs
./qp tail backend
./qp tail frontend

# Check status
./qp status
```

## 🎯 PR Checklist

Before merging, ensure:

- [ ] Code works locally with `./qp start --mode all`
- [ ] No console errors in browser
- [ ] Backend API docs load at http://localhost:8000/docs
- [ ] Blog posts render correctly (if applicable)
- [ ] Images load properly (if applicable)
- [ ] Code follows existing style
- [ ] Commit messages are descriptive
- [ ] PR description explains what and why

## 🚫 What Not to Do

- ❌ Don't commit directly to `main` (it's protected)
- ❌ Don't force push to `main`
- ❌ Don't commit secrets or API keys
- ❌ Don't commit `node_modules/` or `.venv/`
- ❌ Don't commit `.env` files (use `.env.example`)

## 📚 Resources

- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Writing Good PR Descriptions](https://github.blog/2015-01-21-how-to-write-the-perfect-pull-request/)

---

Questions? Open an issue or check existing documentation in the repo.
