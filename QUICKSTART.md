# Quick Start Guide

Get your Quality Playbook blog running in 5 minutes!

## 🚀 Option 1: Docker Compose (Easiest)

```bash
# Clone and start
cd qualityplaybook.dev
docker-compose up

# Visit http://localhost:5173
```

That's it! 🎉

## 🛠️ Option 2: Local Development

### 1. Run Setup Script

```bash
chmod +x scripts/setup-local.sh
./scripts/setup-local.sh
```

### 2. Start Services

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 3. Open Browser

Visit http://localhost:5173

## ✍️ Write Your First Blog Post

1. Create file `backend/content/blog/my-first-post.md`:

```markdown
---
title: My First Post
date: 2025-10-05
tags: [Testing, Quality]
excerpt: This is my first blog post!
author: Quality Playbook
---

# My First Post

Hello world! This is my first post on Quality Playbook.

## Code Example

```python
def test_quality():
    assert True
```
\```

2. Refresh http://localhost:5173/blog - your post appears!

3. Add an image:
   - Put image in `frontend/public/media/blog/my-first-post/`
   - Reference in markdown: `![Alt text](/media/blog/my-first-post/image.png)`

## 📦 Deploy to Production

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment guide.

Quick version:

1. Setup GCP & GKE cluster
2. Configure GitHub secrets
3. Push to `main` branch
4. GitHub Actions deploys automatically!

## 🎯 Key Files

- `backend/content/blog/*.md` - Your blog posts
- `frontend/src/views/*` - Page components
- `helm/*/values.yaml` - Kubernetes config
- `.github/workflows/deploy.yml` - CI/CD pipeline

## 📚 Next Steps

- Customize About page (`frontend/src/views/AboutView.vue`)
- Update Portfolio (`frontend/src/views/PortfolioView.vue`)
- Change colors (`frontend/tailwind.config.js`)
- Add more blog posts!

## 🆘 Troubleshooting

**Backend won't start:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend won't start:**
```bash
cd frontend
npm install
```

**Port already in use:**
```bash
# Change port in docker-compose.yml or vite.config.ts
```

## 📖 Full Documentation

- [README.md](README.md) - Complete project documentation
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment guide

---

Happy blogging! 🎉
