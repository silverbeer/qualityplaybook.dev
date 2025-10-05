#!/bin/bash

set -e

echo "🚀 Deploying Quality Playbook to local k3s cluster"
echo "=================================================="

# Check if kubectl is configured
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ kubectl is not configured or k3s is not running"
    exit 1
fi

echo "✅ k3s cluster detected"

# Build Docker images
echo ""
echo "🔨 Building Docker images..."
docker build -t qualityplaybook-backend:latest ./backend
docker build -t qualityplaybook-frontend:latest ./frontend

# Import images to k3s (if using k3s directly)
if command -v k3s &> /dev/null; then
    echo ""
    echo "📦 Importing images to k3s..."
    docker save qualityplaybook-backend:latest | sudo k3s ctr images import -
    docker save qualityplaybook-frontend:latest | sudo k3s ctr images import -
else
    echo "⚠️  k3s command not found, assuming Rancher Desktop (images should be available)"
fi

# Deploy with Helm
echo ""
echo "☸️  Deploying with Helm..."

# Deploy backend
helm upgrade --install qualityplaybook-backend ./helm/backend \
  --set image.repository=qualityplaybook-backend \
  --set image.tag=latest \
  --set image.pullPolicy=Never \
  --wait

# Deploy frontend
helm upgrade --install qualityplaybook-frontend ./helm/frontend \
  --set image.repository=qualityplaybook-frontend \
  --set image.tag=latest \
  --set image.pullPolicy=Never \
  --wait

# Apply local k8s resources
echo ""
echo "🔧 Applying local Kubernetes resources..."
kubectl apply -f k8s/local/

# Wait for pods
echo ""
echo "⏳ Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=qualityplaybook-backend --timeout=120s
kubectl wait --for=condition=ready pod -l app=qualityplaybook-frontend --timeout=120s

# Get status
echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Status:"
kubectl get pods -l 'app in (qualityplaybook-backend,qualityplaybook-frontend)'
echo ""
kubectl get svc -l 'app in (qualityplaybook-backend,qualityplaybook-frontend)'
echo ""
kubectl get ingress qualityplaybook-ingress

echo ""
echo "🌐 Access the application:"
echo ""
echo "Option 1 - Via Ingress:"
echo "  Add to /etc/hosts: 127.0.0.1 qualityplaybook.local"
echo "  Visit: http://qualityplaybook.local"
echo ""
echo "Option 2 - Via Port Forward:"
echo "  kubectl port-forward svc/qualityplaybook-frontend 8080:80"
echo "  Visit: http://localhost:8080"
echo ""
echo "View logs:"
echo "  kubectl logs -f -l app=qualityplaybook-backend"
echo "  kubectl logs -f -l app=qualityplaybook-frontend"
echo ""
