#!/usr/bin/env python3
"""
Quality Playbook CLI - Manage your blog development environment
"""
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.text import Text

app = typer.Typer(
    name="qp",
    help="🎯 Quality Playbook CLI - Manage your blog development environment",
    add_completion=False,
)
console = Console()

# Project paths
PROJECT_ROOT = Path(__file__).parent
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"


def run_command(cmd: str, cwd: Optional[Path] = None, capture=False) -> subprocess.CompletedProcess:
    """Run a shell command"""
    return subprocess.run(
        cmd,
        shell=True,
        cwd=cwd or PROJECT_ROOT,
        capture_output=capture,
        text=True
    )


def is_running(service: str) -> bool:
    """Check if a service is running"""
    if service == "backend":
        result = run_command("lsof -ti:8000", capture=True)
        return bool(result.stdout.strip())
    elif service == "frontend":
        result = run_command("lsof -ti:5173", capture=True)
        return bool(result.stdout.strip())
    elif service == "docker":
        result = run_command("docker-compose ps -q", capture=True)
        return bool(result.stdout.strip())
    return False


def get_pid(port: int) -> Optional[str]:
    """Get PID of process running on port"""
    result = run_command(f"lsof -ti:{port}", capture=True)
    return result.stdout.strip() if result.stdout.strip() else None


@app.command()
def start(
    mode: str = typer.Option(
        "docker",
        "--mode",
        "-m",
        help="Start mode: docker, backend, frontend, or all"
    )
):
    """🚀 Start the development environment"""

    if mode == "docker":
        console.print("\n[bold cyan]🐳 Starting with Docker Compose...[/bold cyan]")
        run_command("docker-compose up -d")

        # Wait a moment for services to start
        with console.status("[bold green]Waiting for services..."):
            time.sleep(3)

        console.print("[bold green]✅ Services started![/bold green]")
        console.print("\n📍 Access points:")
        console.print("   Frontend: [link=http://localhost:5173]http://localhost:5173[/link]")
        console.print("   Backend API: [link=http://localhost:8000/docs]http://localhost:8000/docs[/link]")

    elif mode == "backend":
        if is_running("backend"):
            console.print("[yellow]⚠️  Backend is already running on port 8000[/yellow]")
            return

        console.print("\n[bold cyan]🔧 Starting Backend (FastAPI)...[/bold cyan]")
        console.print("[dim]Run 'qp tail backend' in another terminal to see logs[/dim]\n")

        # Start backend in background
        subprocess.Popen(
            "uv run uvicorn app.main:app --reload --port 8000",
            shell=True,
            cwd=BACKEND_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        console.print("[bold green]✅ Backend started![/bold green]")
        console.print("   API Docs: [link=http://localhost:8000/docs]http://localhost:8000/docs[/link]")

    elif mode == "frontend":
        if is_running("frontend"):
            console.print("[yellow]⚠️  Frontend is already running on port 5173[/yellow]")
            return

        console.print("\n[bold cyan]🎨 Starting Frontend (Vue)...[/bold cyan]")
        console.print("[dim]Run 'qp tail frontend' in another terminal to see logs[/dim]\n")

        # Start frontend in background
        subprocess.Popen(
            "npm run dev",
            shell=True,
            cwd=FRONTEND_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        console.print("[bold green]✅ Frontend started![/bold green]")
        console.print("   Dev Server: [link=http://localhost:5173]http://localhost:5173[/link]")

    elif mode == "all":
        console.print("\n[bold cyan]🚀 Starting All Services...[/bold cyan]\n")

        # Start backend
        if not is_running("backend"):
            subprocess.Popen(
                "uv run uvicorn app.main:app --reload --port 8000",
                shell=True,
                cwd=BACKEND_DIR,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            console.print("[green]✓[/green] Backend starting...")
        else:
            console.print("[yellow]⚠[/yellow] Backend already running")

        # Start frontend
        if not is_running("frontend"):
            subprocess.Popen(
                "npm run dev",
                shell=True,
                cwd=FRONTEND_DIR,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            console.print("[green]✓[/green] Frontend starting...")
        else:
            console.print("[yellow]⚠[/yellow] Frontend already running")

        console.print("\n[bold green]✅ Services started![/bold green]")
        console.print("\n📍 Access points:")
        console.print("   Frontend: [link=http://localhost:5173]http://localhost:5173[/link]")
        console.print("   Backend API: [link=http://localhost:8000/docs]http://localhost:8000/docs[/link]")


@app.command()
def stop(
    mode: str = typer.Option(
        "all",
        "--mode",
        "-m",
        help="Stop mode: docker, backend, frontend, or all"
    )
):
    """🛑 Stop the development environment"""

    if mode == "docker":
        console.print("\n[bold yellow]🐳 Stopping Docker Compose...[/bold yellow]")
        run_command("docker-compose down")
        console.print("[bold green]✅ Docker services stopped![/bold green]")

    elif mode == "backend":
        pid = get_pid(8000)
        if pid:
            console.print(f"\n[bold yellow]🔧 Stopping Backend (PID: {pid})...[/bold yellow]")
            run_command(f"kill {pid}")
            console.print("[bold green]✅ Backend stopped![/bold green]")
        else:
            console.print("[yellow]⚠️  Backend is not running[/yellow]")

    elif mode == "frontend":
        pid = get_pid(5173)
        if pid:
            console.print(f"\n[bold yellow]🎨 Stopping Frontend (PID: {pid})...[/bold yellow]")
            run_command(f"kill {pid}")
            console.print("[bold green]✅ Frontend stopped![/bold green]")
        else:
            console.print("[yellow]⚠️  Frontend is not running[/yellow]")

    elif mode == "all":
        console.print("\n[bold yellow]🛑 Stopping All Services...[/bold yellow]\n")

        stopped = False

        # Stop backend
        pid = get_pid(8000)
        if pid:
            run_command(f"kill {pid}")
            console.print("[green]✓[/green] Backend stopped")
            stopped = True

        # Stop frontend
        pid = get_pid(5173)
        if pid:
            run_command(f"kill {pid}")
            console.print("[green]✓[/green] Frontend stopped")
            stopped = True

        # Stop docker
        result = run_command("docker-compose ps -q", capture=True)
        if result.stdout.strip():
            run_command("docker-compose down")
            console.print("[green]✓[/green] Docker services stopped")
            stopped = True

        if stopped:
            console.print("\n[bold green]✅ All services stopped![/bold green]")
        else:
            console.print("\n[yellow]⚠️  No services were running[/yellow]")


@app.command()
def status():
    """📊 Show status of all services"""

    table = Table(
        title="🎯 Quality Playbook Status",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan"
    )

    table.add_column("Service", style="bold")
    table.add_column("Port")
    table.add_column("Status")
    table.add_column("PID")
    table.add_column("URL")

    # Check backend
    backend_pid = get_pid(8000)
    if backend_pid:
        table.add_row(
            "Backend",
            "8000",
            "[green]Running[/green]",
            backend_pid,
            "http://localhost:8000/docs"
        )
    else:
        table.add_row(
            "Backend",
            "8000",
            "[red]Stopped[/red]",
            "-",
            "-"
        )

    # Check frontend
    frontend_pid = get_pid(5173)
    if frontend_pid:
        table.add_row(
            "Frontend",
            "5173",
            "[green]Running[/green]",
            frontend_pid,
            "http://localhost:5173"
        )
    else:
        table.add_row(
            "Frontend",
            "5173",
            "[red]Stopped[/red]",
            "-",
            "-"
        )

    # Check docker
    docker_result = run_command("docker-compose ps --format json", capture=True)
    if docker_result.stdout.strip():
        table.add_row(
            "Docker",
            "various",
            "[green]Running[/green]",
            "multiple",
            "-"
        )
    else:
        table.add_row(
            "Docker",
            "various",
            "[red]Stopped[/red]",
            "-",
            "-"
        )

    console.print("\n")
    console.print(table)
    console.print("\n")


@app.command()
def tail(
    service: str = typer.Argument(
        ...,
        help="Service to tail: backend, frontend, or docker"
    ),
    follow: bool = typer.Option(
        True,
        "--follow/--no-follow",
        "-f",
        help="Follow log output"
    )
):
    """📜 Tail logs from a service"""

    console.print(f"\n[bold cyan]📜 Tailing {service} logs...[/bold cyan]")
    console.print("[dim]Press Ctrl+C to stop[/dim]\n")

    if service == "backend":
        if not is_running("backend"):
            console.print("[red]❌ Backend is not running[/red]")
            sys.exit(1)

        try:
            subprocess.run(
                "uv run uvicorn app.main:app --reload --port 8000",
                shell=True,
                cwd=BACKEND_DIR
            )
        except KeyboardInterrupt:
            console.print("\n[yellow]Stopped tailing backend logs[/yellow]")

    elif service == "frontend":
        if not is_running("frontend"):
            console.print("[red]❌ Frontend is not running[/red]")
            sys.exit(1)

        try:
            subprocess.run(
                "npm run dev",
                shell=True,
                cwd=FRONTEND_DIR
            )
        except KeyboardInterrupt:
            console.print("\n[yellow]Stopped tailing frontend logs[/yellow]")

    elif service == "docker":
        if not is_running("docker"):
            console.print("[red]❌ Docker services are not running[/red]")
            sys.exit(1)

        try:
            flag = "-f" if follow else ""
            subprocess.run(f"docker-compose logs {flag}", shell=True)
        except KeyboardInterrupt:
            console.print("\n[yellow]Stopped tailing docker logs[/yellow]")
    else:
        console.print(f"[red]❌ Unknown service: {service}[/red]")
        console.print("Available services: backend, frontend, docker")
        sys.exit(1)


@app.command()
def restart(
    mode: str = typer.Option(
        "all",
        "--mode",
        "-m",
        help="Restart mode: docker, backend, frontend, or all"
    )
):
    """🔄 Restart services"""
    console.print(f"\n[bold cyan]🔄 Restarting {mode}...[/bold cyan]\n")

    # Use the context object to call other commands
    ctx = typer.Context(stop)
    ctx.invoke(stop, mode=mode)
    time.sleep(1)
    ctx = typer.Context(start)
    ctx.invoke(start, mode=mode)


if __name__ == "__main__":
    app()
