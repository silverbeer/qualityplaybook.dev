# Claude Code Project Instructions

This file contains project-specific instructions and preferences for working with this codebase.

## Python Package Management

**IMPORTANT: This project uses `uv`, NOT pip.**

### DO:
- ✅ Use `uv` for all Python dependency management
- ✅ Manage dependencies in `pyproject.toml`
- ✅ Use `uv sync` to install dependencies
- ✅ Use `uv add <package>` to add new dependencies
- ✅ Use `uv run <command>` to run Python commands
- ✅ Use `uv lock --upgrade` to update dependencies

### DON'T:
- ❌ Do NOT use `pip install`
- ❌ Do NOT create `requirements.txt` files
- ❌ Do NOT use `python -m venv` (uv manages virtual environments)
- ❌ Do NOT suggest pip-based workflows

## Backend Development

### Running the Backend
```bash
cd backend
uv sync                                    # Install dependencies
uv run uvicorn app.main:app --reload      # Run dev server
```

### Adding Dependencies
```bash
cd backend
uv add fastapi                             # Add new dependency
uv add --dev pytest                        # Add dev dependency
```

### Dockerfile Pattern
All Dockerfiles should use the uv pattern:
```dockerfile
FROM python:3.11-slim
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml .
COPY uv.lock* ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Run application
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Tech Stack

### Backend
- **FastAPI** - REST API framework
- **Python 3.11+**
- **uv** - Package management (REQUIRED)
- **python-frontmatter** - YAML metadata parsing
- **Python-Markdown** - Markdown to HTML conversion

### Frontend
- **Vue 3** - Framework (Composition API)
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Pinia** - State management
- **Prism.js** - Syntax highlighting

### Infrastructure
- **k3s/Rancher** - Local Kubernetes
- **GKE Autopilot** - Production Kubernetes
- **Helm** - Deployment management
- **Docker** - Containerization

## Project Structure

```
qualityplaybook.dev/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   └── services/       # Business logic
│   ├── content/blog/       # Markdown blog posts
│   ├── pyproject.toml      # Python dependencies (uv)
│   ├── uv.lock             # Locked dependencies
│   └── Dockerfile
├── frontend/               # Vue 3 frontend
│   ├── src/
│   │   ├── views/         # Page components
│   │   ├── components/    # Reusable components
│   │   └── stores/        # Pinia stores
│   └── public/media/      # Blog images/videos
└── helm/                   # Kubernetes deployment
```

## Development Workflows

### Local Development
```bash
# Option 1: Docker Compose
docker-compose up

# Option 2: Manual
cd backend && uv run uvicorn app.main:app --reload
cd frontend && npm run dev
```

### k3s Deployment
```bash
make k3s-deploy              # Full deployment
make k3s-redeploy frontend   # Quick frontend update
make k3s-redeploy backend    # Quick backend update
```

### Adding Blog Posts
1. Create `backend/content/blog/post-slug.md` with frontmatter
2. Add images to `frontend/public/media/blog/post-slug/`
3. Reference images: `![alt](/media/blog/post-slug/image.png)`
4. Test locally, commit, push

## Code Style Preferences

### Python
- Use type hints
- Follow FastAPI best practices
- Keep services modular and testable
- Use async/await for API endpoints

### Vue/TypeScript
- Use Composition API (not Options API)
- Define TypeScript interfaces for all data models
- Keep components small and focused
- Use Tailwind utility classes

### Markdown
- All blog posts require frontmatter:
  ```yaml
  ---
  title: Post Title
  date: YYYY-MM-DD
  tags: [Tag1, Tag2]
  excerpt: Brief description
  author: Quality Playbook
  ---
  ```

## Important Files

- `backend/pyproject.toml` - Python dependencies (managed by uv)
- `backend/app/services/markdown_parser.py` - Markdown processing logic
- `frontend/src/stores/blog.ts` - Blog state management
- `helm/*/values.yaml` - Deployment configuration
- `.github/workflows/deploy.yml` - CI/CD pipeline

## When Making Changes

### Adding Python Dependencies
```bash
cd backend
uv add <package-name>           # Adds to pyproject.toml and uv.lock
git add pyproject.toml uv.lock
```

### Modifying Deployment
- Local: Update `helm/*/values.yaml` and redeploy with `make k3s-deploy`
- Production: Changes automatically deploy via GitHub Actions on merge to main

### Writing New Features
1. Update backend API if needed (`backend/app/api/`)
2. Update frontend components/views (`frontend/src/`)
3. Test locally with Docker Compose or k3s
4. Commit and push

## Author & Contact

- **Author:** Tom Drake
- **LinkedIn:** [www.linkedin.com/in/tomdrake-qe](https://www.linkedin.com/in/tomdrake-qe)

## References

- [uv Documentation](https://github.com/astral-sh/uv)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Vue 3 Documentation](https://vuejs.org)
- [Tailwind CSS Documentation](https://tailwindcss.com)

---

**Remember: Always use `uv` for Python package management. No pip, no requirements.txt!**
