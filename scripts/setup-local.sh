#!/bin/bash

set -e

echo "🚀 Quality Playbook - Local Development Setup"
echo "=============================================="

# Check prerequisites
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 is required but not installed."; exit 1; }
command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed."; exit 1; }
command -v uv >/dev/null 2>&1 || { echo "❌ uv is required but not installed. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1; }

echo "✅ Prerequisites check passed"

# Setup backend
echo ""
echo "📦 Setting up backend..."
cd backend

echo "Installing Python dependencies with uv..."
uv sync

echo "Creating .env file..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Created .env file"
else
    echo "⚠️  .env file already exists, skipping"
fi

cd ..

# Setup frontend
echo ""
echo "📦 Setting up frontend..."
cd frontend

echo "Installing Node dependencies..."
npm install

echo "Creating .env file..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Created .env file"
else
    echo "⚠️  .env file already exists, skipping"
fi

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start development servers:"
echo ""
echo "Option 1 - Docker Compose (recommended):"
echo "  docker-compose up"
echo ""
echo "Option 2 - Manual:"
echo "  Terminal 1: cd backend && uv run uvicorn app.main:app --reload"
echo "  Terminal 2: cd frontend && npm run dev"
echo ""
echo "Then visit: http://localhost:5173"
echo ""
