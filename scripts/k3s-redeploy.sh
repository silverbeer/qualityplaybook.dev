#!/bin/bash

set -e

echo "🔄 Quick redeploy to k3s"
echo "======================="

# Parse arguments
COMPONENT=${1:-all}

redeploy_backend() {
    echo "🔨 Rebuilding backend..."
    docker build -t qualityplaybook-backend:latest ./backend

    if command -v k3s &> /dev/null; then
        docker save qualityplaybook-backend:latest | sudo k3s ctr images import -
    fi

    echo "🔄 Restarting backend pods..."
    kubectl rollout restart deployment qualityplaybook-backend
    kubectl rollout status deployment qualityplaybook-backend
}

redeploy_frontend() {
    echo "🔨 Rebuilding frontend..."
    docker build -t qualityplaybook-frontend:latest ./frontend

    if command -v k3s &> /dev/null; then
        docker save qualityplaybook-frontend:latest | sudo k3s ctr images import -
    fi

    echo "🔄 Restarting frontend pods..."
    kubectl rollout restart deployment qualityplaybook-frontend
    kubectl rollout status deployment qualityplaybook-frontend
}

case $COMPONENT in
    backend)
        redeploy_backend
        ;;
    frontend)
        redeploy_frontend
        ;;
    all|*)
        redeploy_backend
        redeploy_frontend
        ;;
esac

echo ""
echo "✅ Redeploy complete!"
echo ""
echo "View logs:"
echo "  kubectl logs -f -l app=qualityplaybook-$COMPONENT"
echo ""
