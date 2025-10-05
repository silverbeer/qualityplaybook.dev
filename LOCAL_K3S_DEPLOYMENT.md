# Local k3s Deployment Guide

Deploy Quality Playbook to your local Rancher/k3s cluster.

## Prerequisites

- k3s/Rancher Desktop running
- `kubectl` configured for your k3s cluster
- `helm` installed
- Docker for building images

## Quick Start

```bash
# Build and deploy locally
make k3s-deploy
```

Or follow the manual steps below.

## Manual Deployment Steps

### 1. Verify k3s is Running

```bash
kubectl cluster-info
kubectl get nodes
```

### 2. Build Docker Images Locally

Since we're deploying locally, we don't need GCR. Build images for local registry:

```bash
# Build backend
docker build -t qualityplaybook-backend:latest ./backend

# Build frontend
docker build -t qualityplaybook-frontend:latest ./frontend

# If using k3s, import images directly
# (k3s uses containerd, not docker)
docker save qualityplaybook-backend:latest | sudo k3s ctr images import -
docker save qualityplaybook-frontend:latest | sudo k3s ctr images import -
```

### 3. Create Local Helm Values

Create `helm/local-values.yaml`:

```yaml
# Local k3s deployment values
backend:
  image:
    repository: qualityplaybook-backend
    tag: latest
    pullPolicy: Never  # Don't pull, use local image

frontend:
  image:
    repository: qualityplaybook-frontend
    tag: latest
    pullPolicy: Never  # Don't pull, use local image

# Use local paths instead of GCS
mediaStorage:
  type: local
  path: /data/media
```

### 4. Deploy with Helm

```bash
# Deploy backend
helm upgrade --install qualityplaybook-backend ./helm/backend \
  --set image.repository=qualityplaybook-backend \
  --set image.tag=latest \
  --set image.pullPolicy=Never

# Deploy frontend
helm upgrade --install qualityplaybook-frontend ./helm/frontend \
  --set image.repository=qualityplaybook-frontend \
  --set image.tag=latest \
  --set image.pullPolicy=Never
```

### 5. Setup Ingress (Traefik)

k3s comes with Traefik by default. Create ingress:

```bash
kubectl apply -f k8s/local-ingress.yaml
```

### 6. Access the Application

```bash
# Get the ingress IP/hostname
kubectl get ingress

# Add to /etc/hosts if needed
echo "127.0.0.1 qualityplaybook.local" | sudo tee -a /etc/hosts

# Visit http://qualityplaybook.local
```

## Alternative: kubectl apply

If you prefer not using Helm locally:

```bash
# Apply all k8s manifests
kubectl apply -f k8s/local/
```

## Local Storage for Media

### Option 1: HostPath Volume

```yaml
# In k8s/local/persistent-volume.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: media-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteMany
  hostPath:
    path: /var/lib/rancher/k3s/storage/media
```

### Option 2: Local NFS

If you have NFS set up:

```yaml
spec:
  nfs:
    server: 192.168.1.100
    path: /export/media
```

## Development Workflow

### 1. Make Code Changes

Edit your files as normal.

### 2. Rebuild & Redeploy

```bash
# Quick redeploy script
./scripts/k3s-redeploy.sh
```

Or manually:

```bash
# Rebuild image
docker build -t qualityplaybook-frontend:latest ./frontend

# Import to k3s
docker save qualityplaybook-frontend:latest | sudo k3s ctr images import -

# Restart pods to pick up new image
kubectl rollout restart deployment qualityplaybook-frontend
```

### 3. View Logs

```bash
# Backend logs
kubectl logs -f -l app=qualityplaybook-backend

# Frontend logs
kubectl logs -f -l app=qualityplaybook-frontend
```

## Port Forwarding (Alternative to Ingress)

If you don't want to set up ingress locally:

```bash
# Port forward frontend
kubectl port-forward svc/qualityplaybook-frontend 8080:80

# Port forward backend
kubectl port-forward svc/qualityplaybook-backend 8000:8000

# Visit http://localhost:8080
```

## Troubleshooting

### Pods not starting

```bash
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Image pull errors

Make sure `imagePullPolicy: Never` is set in your Helm values.

### Traefik not routing

```bash
# Check Traefik
kubectl get svc -n kube-system traefik

# Check ingress
kubectl describe ingress qualityplaybook-ingress
```

### Can't access via domain

Check `/etc/hosts`:
```bash
cat /etc/hosts | grep qualityplaybook
```

## Comparison: k3s vs GKE

| Feature | k3s (Local) | GKE (Production) |
|---------|-------------|------------------|
| Cost | Free | $$$ |
| Setup | Minutes | Hours |
| SSL/TLS | Manual/Self-signed | cert-manager + Let's Encrypt |
| Storage | HostPath/NFS | GCS |
| Scalability | Single node | Multi-node autoscaling |
| Use Case | Development/Testing | Production |

## Hybrid Approach

You can use k3s for local development and GKE for production:

```bash
# Local development
make k3s-deploy
# Test at http://qualityplaybook.local

# Production deployment
git push origin main
# GitHub Actions deploys to GKE
```

## Next Steps

1. **Test locally on k3s** - Verify everything works
2. **Develop features** - Use k3s for fast iteration
3. **Deploy to GKE when ready** - Follow DEPLOYMENT.md for production

---

For production GKE deployment, see [DEPLOYMENT.md](DEPLOYMENT.md)
