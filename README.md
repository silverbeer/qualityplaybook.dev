# Quality Playbook

A modern, GitOps-based blog platform for quality engineering insights and best practices.

Built with Vue 3, FastAPI, and deployed to GKE Autopilot.

## 🚀 Features

- **GitOps Workflow** - Write blog posts in Markdown, commit to repo, auto-deploy
- **Modern Stack** - Vue 3 + TypeScript + Tailwind CSS frontend, FastAPI backend
- **Code Highlighting** - Beautiful syntax highlighting with Prism.js
- **Tag-based Filtering** - Organize and filter posts by tags
- **Pagination** - Clean pagination for blog listings
- **Responsive Design** - Mobile-first design with Tailwind CSS
- **Kubernetes Ready** - Helm charts for GKE Autopilot deployment

## 📁 Project Structure

```
qualityplaybook.dev/
├── frontend/               # Vue 3 + TypeScript + Tailwind
│   ├── src/
│   │   ├── components/    # Reusable Vue components
│   │   ├── views/         # Page components
│   │   ├── stores/        # Pinia state management
│   │   └── router/        # Vue Router configuration
│   └── public/
│       └── media/         # Blog images/videos (synced to GCS)
├── backend/               # FastAPI + Python
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   └── services/     # Business logic (markdown parsing)
│   └── content/
│       └── blog/         # Markdown blog posts
├── helm/                  # Kubernetes deployment
│   ├── frontend/         # Frontend Helm chart
│   └── backend/          # Backend Helm chart
└── .github/workflows/    # CI/CD pipeline
```

## 🛠️ Tech Stack

### Frontend
- **Vue 3** with Composition API
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **Pinia** for state management
- **Vue Router** for navigation
- **Prism.js** for code syntax highlighting
- **Axios** for API calls

### Backend
- **FastAPI** for REST API
- **Python 3.11+**
- **python-frontmatter** for YAML metadata parsing
- **Python-Markdown** with extensions (code highlighting, tables, TOC)
- **Uvicorn** as ASGI server

### Infrastructure
- **GKE Autopilot** - Kubernetes hosting
- **Helm** - Deployment management
- **GitHub Actions** - CI/CD pipeline
- **GCS** - Media storage
- **nginx-ingress** - Ingress controller
- **cert-manager** - SSL certificates

## 🏃 Local Development

### Prerequisites
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer
- Node.js 20+
- Docker & Docker Compose (optional)

**Install uv:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Option 1: Docker Compose (Recommended)

```bash
# Start all services
docker-compose up

# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup

**Backend:**
```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Visit http://localhost:5173 to see the site.

## ✍️ Writing Blog Posts

1. Create a new markdown file in `backend/content/blog/`:

```markdown
---
title: Your Post Title
date: 2025-10-05
tags: [Testing, Automation, Python]
excerpt: A short description of your post
author: Quality Playbook
---

# Your Post Title

Your content here...

## Code Examples

```python
def hello_world():
    print("Hello, World!")
```
\```

2. Add images to `frontend/public/media/blog/your-post-slug/`:

```markdown
![Screenshot](/media/blog/your-post-slug/screenshot.png)
```

3. Run locally to preview:
```bash
# Visit http://localhost:5173/blog/your-post-slug
```

4. Commit and create PR:
```bash
git add .
git commit -m "Add new blog post: Your Post Title"
git push origin feature/new-post
```

5. Merge PR → Automatic deployment! 🚀

## 🚢 Deployment

### Initial Setup

1. **Configure GCP Secrets** in GitHub:
   - `GCP_PROJECT_ID` - Your GCP project ID
   - `GCP_SA_KEY` - Service account JSON key
   - `GKE_CLUSTER` - Your GKE cluster name
   - `GKE_ZONE` - GKE cluster zone
   - `GCS_MEDIA_BUCKET` - GCS bucket for media files

2. **Create GCS Bucket** for media:
```bash
gsutil mb -p YOUR_PROJECT_ID gs://qualityplaybook-media
gsutil iam ch allUsers:objectViewer gs://qualityplaybook-media
```

3. **Update Helm values**:
   - Edit `helm/frontend/values.yaml` - Set your GCR image repository
   - Edit `helm/backend/values.yaml` - Set your GCR image repository

4. **Setup DNS**:
   - Point `qualityplaybook.dev` to GKE Ingress IP
   - Point `www.qualityplaybook.dev` to GKE Ingress IP

### Automated Deployment

Merging to `main` branch triggers:
1. Build Docker images for frontend & backend
2. Push images to Google Container Registry
3. Sync media files to GCS
4. Deploy to GKE via Helm

View deployment status in GitHub Actions.

## 🔧 Configuration

### Environment Variables

**Frontend (`frontend/.env`):**
```
VITE_API_BASE=/api
```

**Backend:**
```
ENVIRONMENT=development
```

### Customization

- **Colors**: Edit `frontend/tailwind.config.js`
- **API endpoints**: See `backend/app/api/blog.py`
- **Styling**: Edit `frontend/src/assets/main.css`
- **Content directory**: Configure in `backend/app/services/markdown_parser.py`

## 📝 API Endpoints

- `GET /api/blog/posts` - List blog posts (with pagination & tag filter)
- `GET /api/blog/posts/{slug}` - Get single post
- `GET /api/blog/tags` - Get all tags
- `GET /health` - Health check

Full API docs: http://localhost:8000/docs

## 🧪 Testing

```bash
# Backend tests (coming soon)
cd backend
pytest

# Frontend tests (coming soon)
cd frontend
npm run test
```

## 📦 Production Build

**Frontend:**
```bash
cd frontend
npm run build
# Output in dist/
```

**Backend:**
```bash
cd backend
docker build -t qualityplaybook-backend .
```

## 🤝 Contributing

This is a personal blog, but suggestions are welcome! Open an issue or PR.

## 📄 License

MIT License - See LICENSE file for details

## 🔗 Links

- **Live Site**: https://qualityplaybook.dev
- **Portfolio**: https://qualityplaybook.dev/portfolio
- **Related Projects**:
  - [missingtable.com](https://missingtable.com)
  - match-scraper

---

Built with ❤️ by a quality engineering enthusiast
