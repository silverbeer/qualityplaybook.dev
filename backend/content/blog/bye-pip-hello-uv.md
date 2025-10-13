---
title: "Bye pip 👋 — Hello uv 🚀"
date: 2025-10-13
tags: ["python", "tooling", "uv", "pip", "pyproject", "quality-engineering"]
description: "After years of wrestling with pip, venv, and dependency drift, I'm switching my Python projects to uv — and it feels like stepping into the future."
---

For years, every Python project started the same way:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

And then… *you’d forget which virtual env you were in, pip would hang on dependency resolution, and CI would rebuild the world from scratch.*

We’ve all been there.

---

## Enter `uv` 🪄

[`uv`](https://github.com/astral-sh/uv) is the **next-gen Python package manager and environment tool** from the same team behind `ruff` and `astral`.  
It’s *fast*, *hermetic*, and *batteries-included*. Think of it as Cargo or npm — but for Python that actually respects reproducibility.

```bash
uv init myproject
uv add pytest requests pydantic
uv run pytest
```

That’s it.  
No virtualenv juggling. No “did I install this with pipx?” existential crisis.

---

## Why it clicked for me

- **🧠 Smart isolation:** Each project has a dedicated environment — no `.venv` clutter.  
- **⚡ Blazing speed:** Dependency resolution and installs are *orders of magnitude faster* than pip.  
- **🔒 Reproducible:** A single `uv.lock` guarantees identical installs locally and in CI.  
- **🌍 Consistent CLI:** `uv run`, `uv add`, `uv sync`, `uv lock` — clear verbs, predictable behavior.  
- **🧩 Compatible:** Works fine with existing `requirements.txt` until you migrate.

---

## Real world: my `missing-table` stack

When I pointed my FastAPI backend + pytest suite to `uv`, install time dropped from **48 s → 5 s**.  
CI builds are leaner, and local dev onboarding went from “install Python, create venv, hope pip cooperates” to one command:

```bash
uv sync
```

---

## Tips for switching

1. **Install uv globally**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
2. **Run `uv init`** in a fresh repo (or existing one).  
3. **Migrate dependencies:**
   ```bash
   uv add -r requirements.txt
   ```
4. **Update CI:** replace `pip install -r requirements.txt` with:
   ```bash
   uv sync
   ```

That’s it. You’re done.

---

## Why it matters for Quality Engineering

Faster, deterministic environments mean:
- CI/CD pipelines hit “green” sooner.  
- Less variance between developer machines.  
- Dependency drift bugs disappear.  
- Easier to cache or snapshot test environments.

And that’s not just convenience — that’s **quality at the system level**.

---

## BTW… `pyproject.toml` is pretty cool too 😎

It’s the beating heart of modern Python packaging — defining your dependencies, build system, and metadata in one clean file.  
No more `setup.py` chaos or mystery `MANIFEST.in` rules. Combine `pyproject.toml` + `uv` and you’ve got the modern Python dev experience we’ve all wanted since 3.6.

> Modern Python to the moon 🚀🐍

---

## TL;DR

> **pip**: our dependable but tired old friend.  
> **uv**: fast, reproducible, and ready for CI in 2025.  
> **pyproject.toml**: the unsung hero that makes it all clean.

So yeah…  
No more pip.  
Hello uv.  
And long live modern Python. ✨

---

*If you’ve tried uv or switched your projects to `pyproject.toml`, I’d love to hear how it went — drop a comment or tag me on [LinkedIn](https://www.linkedin.com/in/tomdrakecloud).*
