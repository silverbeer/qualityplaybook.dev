# Deployment Guide

Complete guide for deploying Quality Playbook to GKE Autopilot.

## Prerequisites

- GCP account with billing enabled
- `gcloud` CLI installed and configured
- `kubectl` installed
- `helm` installed
- Domain registered (qualityplaybook.dev)

## 1. GCP Setup

### Create GKE Autopilot Cluster

```bash
export PROJECT_ID="your-project-id"
export CLUSTER_NAME="qualityplaybook-cluster"
export REGION="us-central1"

gcloud config set project $PROJECT_ID

# Create Autopilot cluster
gcloud container clusters create-auto $CLUSTER_NAME \
  --region=$REGION \
  --release-channel=regular

# Get credentials
gcloud container clusters get-credentials $CLUSTER_NAME --region=$REGION
```

### Create GCS Bucket for Media

```bash
export BUCKET_NAME="qualityplaybook-media"

# Create bucket
gsutil mb -p $PROJECT_ID -l $REGION gs://$BUCKET_NAME

# Make bucket publicly readable (for media files)
gsutil iam ch allUsers:objectViewer gs://$BUCKET_NAME
```

### Setup Service Account for CI/CD

```bash
export SA_NAME="qualityplaybook-deployer"

# Create service account
gcloud iam service-accounts create $SA_NAME \
  --display-name="Quality Playbook Deployer"

# Grant necessary permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/container.developer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"

# Create and download key
gcloud iam service-accounts keys create ~/qualityplaybook-sa-key.json \
  --iam-account=$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com
```

## 2. Install Ingress Controller

```bash
# Install nginx-ingress
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm install nginx-ingress ingress-nginx/ingress-nginx \
  --set controller.service.type=LoadBalancer \
  --set controller.service.externalTrafficPolicy=Local
```

Wait for external IP:
```bash
kubectl get svc nginx-ingress-ingress-nginx-controller -w
```

## 3. Install cert-manager

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Wait for cert-manager to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=cert-manager -n cert-manager --timeout=300s
```

### Create ClusterIssuer

```yaml
# Save as cert-manager-issuer.yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
```

```bash
kubectl apply -f cert-manager-issuer.yaml
```

## 4. DNS Configuration

Point your domain to the nginx-ingress external IP:

```
A     qualityplaybook.dev      <EXTERNAL_IP>
A     www.qualityplaybook.dev  <EXTERNAL_IP>
```

## 5. Update Helm Values

Edit `helm/backend/values.yaml`:
```yaml
image:
  repository: gcr.io/YOUR_PROJECT_ID/qualityplaybook-backend
```

Edit `helm/frontend/values.yaml`:
```yaml
image:
  repository: gcr.io/YOUR_PROJECT_ID/qualityplaybook-frontend
```

## 6. GitHub Secrets

Add the following secrets to your GitHub repository:

```
GCP_PROJECT_ID      = your-project-id
GCP_SA_KEY          = <contents of qualityplaybook-sa-key.json>
GKE_CLUSTER         = qualityplaybook-cluster
GKE_ZONE            = us-central1
GCS_MEDIA_BUCKET    = qualityplaybook-media
```

## 7. Initial Deployment

### Option A: Via GitHub Actions (Recommended)

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

GitHub Actions will automatically deploy.

### Option B: Manual Deployment

```bash
# Build images
docker build -t gcr.io/$PROJECT_ID/qualityplaybook-backend:latest ./backend
docker build -t gcr.io/$PROJECT_ID/qualityplaybook-frontend:latest ./frontend

# Configure Docker for GCR
gcloud auth configure-docker

# Push images
docker push gcr.io/$PROJECT_ID/qualityplaybook-backend:latest
docker push gcr.io/$PROJECT_ID/qualityplaybook-frontend:latest

# Deploy with Helm
helm upgrade --install qualityplaybook-backend ./helm/backend \
  --set image.repository=gcr.io/$PROJECT_ID/qualityplaybook-backend \
  --set image.tag=latest

helm upgrade --install qualityplaybook-frontend ./helm/frontend \
  --set image.repository=gcr.io/$PROJECT_ID/qualityplaybook-frontend \
  --set image.tag=latest
```

## 8. Verify Deployment

```bash
# Check pods
kubectl get pods

# Check services
kubectl get svc

# Check ingress
kubectl get ingress

# Check certificate
kubectl get certificate
```

Visit https://qualityplaybook.dev - you should see your site!

## 9. Monitoring & Logs

### View Logs

```bash
# Backend logs
kubectl logs -l app=qualityplaybook-backend -f

# Frontend logs
kubectl logs -l app=qualityplaybook-frontend -f
```

### Check Resource Usage

```bash
kubectl top pods
kubectl top nodes
```

## Troubleshooting

### Certificate Not Issued

```bash
# Check certificate status
kubectl describe certificate qualityplaybook-tls

# Check cert-manager logs
kubectl logs -n cert-manager -l app=cert-manager
```

### 502 Bad Gateway

```bash
# Check backend health
kubectl exec -it <backend-pod> -- curl localhost:8000/health

# Check service endpoints
kubectl get endpoints
```

### Images Not Pulling

```bash
# Verify GCR permissions
gcloud projects get-iam-policy $PROJECT_ID

# Check image exists
gcloud container images list --repository=gcr.io/$PROJECT_ID
```

## Cost Optimization

- Use Autopilot for automatic resource optimization
- Configure appropriate resource requests/limits
- Use regional (not multi-regional) GCS bucket
- Enable GCS lifecycle policies for old media

## Backup Strategy

### Backup Content

```bash
# Backup blog content
git commit -am "Backup content"
git push

# Backup media from GCS
gsutil -m cp -r gs://$BUCKET_NAME ./backup/
```

## Scaling

Autopilot automatically scales based on resource requests. To handle more traffic:

```yaml
# In helm/*/values.yaml
replicaCount: 3  # Increase replicas

resources:
  requests:
    cpu: 200m      # Adjust as needed
    memory: 256Mi
```

## Updates

### Update Application

```bash
# Commit changes
git commit -am "Update feature"
git push origin main
```

GitHub Actions handles the rest!

### Update Kubernetes

```bash
# Update cluster
gcloud container clusters upgrade $CLUSTER_NAME --region=$REGION
```

---

Questions? Open an issue or check the [README.md](README.md).
