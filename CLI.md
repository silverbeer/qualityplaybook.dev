# Quality Playbook CLI 🎯

Beautiful CLI tool built with [Typer](https://typer.tiangolo.com/) and [Rich](https://rich.readthedocs.io/) for managing your Quality Playbook development environment.

## Features

- 🚀 **Start/Stop/Restart** services with one command
- 📊 **Status** dashboard with a beautiful table
- 📜 **Tail logs** from any service
- 🔥 **Hot reload** enabled for both frontend and backend
- 🎨 **Rich terminal UI** with colors and formatting

## Installation

```bash
# Install dependencies (includes typer, rich, watchdog)
cd backend && uv sync && cd ..
```

## Quick Start

```bash
# Start all services with hot reload
./qp start --mode all

# Check status
./qp status

# View logs
./qp tail backend
```

## Create an Alias

For easier usage, create an alias:

```bash
# Add to ~/.zshrc or ~/.bashrc
alias qp="/path/to/qualityplaybook.dev/qp"

# OR use this to get current directory
alias qp="$(pwd)/qp"

# Reload shell
source ~/.zshrc  # or source ~/.bashrc

# Now use it from anywhere:
qp status
qp start --mode all
qp tail frontend
```

## Commands

### 🚀 `start` - Start services

Start development services with hot reload enabled.

**Modes:**
- `docker` - Start with Docker Compose
- `backend` - Start FastAPI backend only
- `frontend` - Start Vue frontend only
- `all` - Start both backend and frontend (default)

```bash
# Start with Docker
uv run python qp.py start --mode docker

# Start backend only (hot reload enabled)
uv run python qp.py start --mode backend

# Start frontend only (hot reload enabled)
uv run python qp.py start --mode frontend

# Start both (hot reload enabled)
uv run python qp.py start --mode all
```

**Hot Reload:**
- **Backend**: Uvicorn's `--reload` automatically reloads on code changes
- **Frontend**: Vite's dev server has HMR (Hot Module Replacement)

### 🛑 `stop` - Stop services

Stop running services.

**Modes:**
- `docker` - Stop Docker Compose services
- `backend` - Stop backend server
- `frontend` - Stop frontend server
- `all` - Stop all services (default)

```bash
# Stop everything
uv run python qp.py stop

# Stop specific service
uv run python qp.py stop --mode backend
```

### 🔄 `restart` - Restart services

Restart services (stop then start).

```bash
# Restart everything
uv run python qp.py restart

# Restart backend only
uv run python qp.py restart --mode backend
```

### 📊 `status` - Show status

Display a beautiful status table showing all services, ports, PIDs, and URLs.

```bash
uv run python qp.py status
```

**Output:**
```
┌─────────────────────────────────────────────────────────────────┐
│                    🎯 Quality Playbook Status                    │
├─────────┬─────────┬─────────┬──────────┬───────────────────────┤
│ Service │ Port    │ Status  │ PID      │ URL                   │
├─────────┼─────────┼─────────┼──────────┼───────────────────────┤
│ Backend │ 8000    │ Running │ 12345    │ http://localhost:8000 │
│ Frontend│ 5173    │ Running │ 12346    │ http://localhost:5173 │
│ Docker  │ various │ Stopped │ -        │ -                     │
└─────────┴─────────┴─────────┴──────────┴───────────────────────┘
```

### 📜 `tail` - View logs

Tail logs from a service in real-time.

**Services:**
- `backend` - FastAPI backend logs
- `frontend` - Vite dev server logs
- `docker` - Docker Compose logs

```bash
# Tail backend logs
uv run python qp.py tail backend

# Tail frontend logs
uv run python qp.py tail frontend

# Tail docker logs (follow mode)
uv run python qp.py tail docker --follow

# View docker logs without following
uv run python qp.py tail docker --no-follow
```

Press `Ctrl+C` to stop tailing.

## Usage Examples

### Daily Development Workflow

```bash
# Morning: Start everything
qp start --mode all
qp status  # Verify all running

# Work on code... (hot reload handles changes automatically!)

# Check backend logs
qp tail backend

# Check frontend logs
qp tail frontend

# Evening: Stop everything
qp stop
```

### Backend-Only Development

```bash
# Start just the backend
qp start --mode backend

# Watch logs while developing
qp tail backend

# Restart after config changes
qp restart --mode backend
```

### Docker Development

```bash
# Start with Docker Compose
qp start --mode docker

# Check container logs
qp tail docker

# Stop containers
qp stop --mode docker
```

### Troubleshooting

```bash
# Check what's running
qp status

# Port already in use? Stop everything
qp stop --mode all

# Start fresh
qp start --mode all
```

## How It Works

### Port Detection
The CLI checks if services are running by looking for processes on specific ports:
- Backend: port 8000
- Frontend: port 5173
- Docker: checks `docker-compose ps`

### Process Management
- Services are started in the background
- PIDs are tracked via port binding
- Graceful shutdown with `kill` command

### Hot Reload
- **Backend**: Uvicorn watches Python files and auto-reloads
- **Frontend**: Vite HMR updates browser without refresh
- Edit code → See changes instantly!

## Customization

The CLI is in `qp.py`. Easy to extend:

```python
@app.command()
def build():
    """🔨 Build production assets"""
    console.print("[bold cyan]Building...[/bold cyan]")
    run_command("docker build -t my-app .", PROJECT_ROOT)
```

## Tips & Tricks

### 1. Create a Global Command

```bash
# Make it globally available
echo 'alias qp="uv run python ~/projects/qualityplaybook.dev/qp.py"' >> ~/.zshrc
source ~/.zshrc

# Use from anywhere
cd ~/anywhere
qp status
```

### 2. Custom Status Checks

Modify `status()` to add health checks:
```python
# Check if API is responding
result = run_command("curl -s http://localhost:8000/health", capture=True)
if '"status":"healthy"' in result.stdout:
    # API is healthy
```

### 3. Multiple Projects

Copy `qp.py` to other projects and customize:
```python
BACKEND_DIR = PROJECT_ROOT / "api"  # Different structure
```

## Troubleshooting

**"Command not found: qp"**
- Make sure you created the alias
- Or use full command: `uv run python qp.py`

**"Permission denied"**
- Make executable: `chmod +x qp.py`

**"Port already in use"**
- Check what's running: `qp status`
- Stop it: `qp stop --mode all`

**Services not stopping**
- Manually kill: `lsof -ti:8000 | xargs kill -9`
- For port 5173: `lsof -ti:5173 | xargs kill -9`

## Dependencies

The CLI uses:
- **typer** - CLI framework
- **rich** - Terminal formatting
- **watchdog** - File system monitoring (for potential future features)

All managed via uv in `backend/pyproject.toml`.

---

Enjoy your beautiful CLI! 🎨✨
