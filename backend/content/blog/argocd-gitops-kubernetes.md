---
title: Adding ArgoCD for GitOps Deployments
date: 2025-12-13
tags: [GitOps, ArgoCD, Kubernetes, CI/CD, DevOps]
excerpt: How I implemented GitOps with ArgoCD to automatically deploy missingtable.com and qualityplaybook.dev to DigitalOcean Kubernetes whenever code is merged to main.
author: Quality Playbook
---

# Adding ArgoCD for GitOps Deployments

Today I completed setting up ArgoCD for GitOps-based continuous delivery to my DigitalOcean Kubernetes (DOKS) cluster. This post documents the journey, the problems I solved, and why GitOps is a game-changer for small teams.

## The Problem with Traditional CI/CD

Before ArgoCD, my deployment pipeline looked like this:

```yaml
# Old approach: CI runs helm directly
deploy:
  steps:
    - name: Get kubeconfig
      run: doctl kubernetes cluster config save missingtable-dev

    - name: Deploy to Kubernetes
      run: |
        helm upgrade --install my-app ./helm/my-app \
          --set secrets.databaseUrl="${{ secrets.DATABASE_URL }}" \
          --set secrets.apiKey="${{ secrets.API_KEY }}" \
          --wait
```

**Problems with this approach:**

1. **Secrets in CI** - Sensitive values passed via `--set` flags
2. **CI needs cluster access** - kubeconfig stored as GitHub secret
3. **No drift detection** - Manual changes go unnoticed
4. **No rollback visibility** - Hard to see what's deployed vs what's in Git

## Enter GitOps

GitOps flips the model: instead of CI pushing to the cluster, the cluster pulls from Git.

```
Traditional: Code → CI → Build → CI → Deploy to Cluster
GitOps:      Code → CI → Build → Git ← ArgoCD ← Cluster
```

ArgoCD watches your Git repository and automatically syncs any changes to Kubernetes. The cluster state always matches what's in Git.

## My Architecture

I run two applications on DOKS:

- **missingtable.com** - A full-stack sports analytics app
- **qualityplaybook.dev** - This blog you're reading

Both now use the same GitOps flow:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   GitHub    │────▶│  GitHub CI  │────▶│    GHCR     │
│   (code)    │     │  (build)    │     │  (images)   │
└─────────────┘     └──────┬──────┘     └─────────────┘
                          │
                          │ commits tag update
                          ▼
┌─────────────┐     ┌─────────────┐
│    DOKS     │◀────│   ArgoCD    │◀──── watches Git
│  (cluster)  │     │  (sync)     │
└─────────────┘     └─────────────┘
```

## Implementation Details

### 1. ArgoCD Installation

ArgoCD runs in my cluster, deployed via Terraform:

```hcl
resource "helm_release" "argocd" {
  name       = "argocd"
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argo-cd"
  namespace  = "argocd"
  version    = "7.7.5"

  set {
    name  = "server.insecure"
    value = "true"  # TLS terminated at ingress
  }
}
```

### 2. ArgoCD Applications

Each app is defined as an ArgoCD Application:

```hcl
resource "kubectl_manifest" "argocd_app_qualityplaybook" {
  yaml_body = <<YAML
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: qualityplaybook
  namespace: argocd
spec:
  source:
    repoURL: https://github.com/silverbeer/qualityplaybook.dev
    targetRevision: main
    path: helm/qualityplaybook
  destination:
    server: https://kubernetes.default.svc
    namespace: qualityplaybook
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
YAML
}
```

Key settings:
- **automated sync** - No manual approval needed
- **prune: true** - Deletes resources removed from Git
- **selfHeal: true** - Reverts manual changes to match Git

### 3. CI Updates Image Tags

When code merges to main, CI builds images with a SHA tag, then commits the updated tag to the Helm values:

```yaml
update-helm-values:
  steps:
    - name: Checkout code
      uses: actions/checkout@v4
      with:
        token: ${{ secrets.GH_PAT }}
        ref: main
        fetch-depth: 0

    - name: Pull latest changes
      run: git pull origin main

    - name: Update image tags
      run: |
        SHORT_SHA=$(echo "${{ github.sha }}" | cut -c1-7)
        sed -i "s|tag: \".*\" # frontend-tag|tag: \"${SHORT_SHA}\" # frontend-tag|" values.yaml
        sed -i "s|tag: \".*\" # backend-tag|tag: \"${SHORT_SHA}\" # backend-tag|" values.yaml

    - name: Commit and push
      run: |
        git config user.name "github-actions[bot]"
        git commit -m "chore: Update image tags to ${SHORT_SHA} [skip ci]"
        git push
```

The `[skip ci]` prevents infinite loops.

### 4. External Secrets for Credentials

Secrets come from AWS Secrets Manager, synced to Kubernetes via External Secrets Operator:

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
  namespace: my-app
spec:
  secretStoreRef:
    name: aws-secrets-manager
    kind: ClusterSecretStore
  target:
    name: app-secrets
  data:
    - secretKey: database-url
      remoteRef:
        key: my-app-secrets
        property: database_url
```

No secrets in CI. No secrets in Git. Everything declarative.

## Challenges I Solved

### Branch Protection vs CI Commits

GitHub's branch protection blocked CI from pushing tag updates:

```
error: GH006: Protected branch update failed
Changes must be made through a pull request
```

**Solution:** Create a Fine-grained PAT with `contents: write` permission and use it for the checkout action. The PAT owner's permissions bypass branch protection.

### Race Conditions

When PRs merged while CI was running, the push failed:

```
Updates were rejected because the remote contains work that you do not have locally
```

**Solution:** Pull latest before applying changes:

```yaml
- name: Pull latest changes
  run: git pull origin main
```

### Production Image Command Mismatch

My frontend Docker image uses nginx, but the Helm chart defaulted to `npm run serve`:

```
exec: "npm": executable file not found in $PATH
```

**Solution:** Override the command in values:

```yaml
frontend:
  command: []  # Let nginx's CMD run
```

## Benefits I'm Seeing

1. **Audit trail** - Every deployment is a Git commit
2. **Easy rollback** - `git revert` undoes deployments
3. **Drift detection** - ArgoCD shows when cluster doesn't match Git
4. **No cluster credentials in CI** - CI only needs Git access
5. **Self-healing** - Manual kubectl changes get reverted

## What's Next

- Add Grafana dashboards for ArgoCD metrics
- Implement progressive delivery with Argo Rollouts
- Add notifications for sync failures

---

GitOps has simplified my deployment workflow significantly. The cluster always matches Git, rollbacks are trivial, and I never worry about secrets in CI again.

If you're running Kubernetes, give ArgoCD a try. The initial setup takes a few hours, but the operational benefits are worth it.
