---
title: "OpenTofu Ninja Training: Multi-Cloud Kubernetes the Hard Way"
date: 2025-12-11
tags: ["kubernetes", "opentofu", "terraform", "infrastructure", "devops", "quality-engineering", "cloud"]
description: "I open-sourced my infrastructure project — 100% IaC for running production workloads across multiple cloud providers. Here's what I learned becoming an OpenTofu and Kubernetes ninja."
---

For months, I've been quietly building something I'm finally ready to share: a production-grade infrastructure project that deploys real applications across multiple cloud providers using nothing but code.

No ClickOps. No manual steps. Just `tofu apply` and everything comes to life.

Today, I'm open-sourcing it: [missingtable-platform-bootstrap](https://github.com/silverbeer/missingtable-platform-bootstrap)

---

## The Mission

I set out with three goals:

1. **100% Infrastructure as Code** — Create and manage missingtable.com and qualityplaybook.dev in Kubernetes with zero manual steps
2. **Cloud Provider Portability** — Build a process to easily switch between EKS, DOKS, GKE, AKS, or Linode
3. **Become a Ninja** — Actually *understand* Terraform/OpenTofu and Kubernetes, not just copy-paste from tutorials

The ultimate test? `tofu destroy && tofu apply` should recreate *everything* — DNS records, certificates, secrets, deployments — without touching a console.

---

## Why OpenTofu?

OpenTofu is an open-source fork of Terraform, created after HashiCorp changed Terraform's license. It's 100% compatible with existing Terraform configurations but backed by a community-driven foundation.

For a learning project focused on portability and open standards, it was the obvious choice.

---

## The Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions (OIDC)                    │
│              No static credentials anywhere                 │
└─────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┴────────────────────┐
         ▼                                         ▼
┌─────────────────────┐                 ┌─────────────────────┐
│   AWS Global        │                 │   DigitalOcean      │
│   ─────────────     │                 │   ─────────────     │
│   • Route 53 DNS    │                 │   • DOKS Cluster    │
│   • Secrets Manager │────────────────▶│   • Ingress + TLS   │
│   • Lambda Certbot  │   (External     │   • Applications    │
│   • S3 State        │    Secrets)     │                     │
│   • DynamoDB Lock   │                 │                     │
└─────────────────────┘                 └─────────────────────┘
```

**DigitalOcean DOKS** runs the actual workloads — a 2-node Kubernetes cluster hosting both sites.

**AWS** provides the supporting cast — Route 53 for DNS, Secrets Manager for credentials, Lambda for automated certificate renewal, and S3/DynamoDB for remote state management.

---

## The Wins

### True IaC Achieved

The breakthrough was managing DNS records in the same module as infrastructure, with records dynamically referencing the ingress IP instead of hardcoded values. Now when I destroy and recreate, DNS points to the *new* ingress automatically.

### Cost-Effective Learning

| Provider | Monthly Cost |
|----------|-------------|
| DOKS (current) | ~$48 |
| EKS (equivalent) | ~$165 |

That's 70% cheaper for running the same workloads. DOKS provides the control plane free; EKS charges $73/month just for that.

### Automated Certificates

No more manual cert renewals or HTTP-01 challenge gymnastics:

1. EventBridge triggers Lambda daily
2. Lambda runs certbot with DNS-01 validation via Route 53
3. Certificates land in AWS Secrets Manager
4. External Secrets Operator syncs them to DOKS
5. Ingress picks them up automatically

DNS-01 validation was the key insight — HTTP-01 fails during destroy/rebuild cycles when cached DNS causes routing issues.

### GitHub Container Registry Everywhere

GHCR works across EKS, DOKS, GKE, and AKS without modification. Cloud-specific registries (ECR, GCR, ACR) create unnecessary lock-in for multi-cloud projects.

---

## Hard-Won Lessons

**Module Structure Matters**
Separate reusable modules (`modules/aws/vpc`) from environment-specific configs (`clouds/aws/environments/dev`). Modules inherit providers from callers — no provider blocks inside modules.

**NAT Gateways Will Drain Your Wallet**
~$32/month each. VPCs are free. Destroy NAT Gateways when not actively testing.

**Kubernetes Resource Naming**
Use `kubernetes_namespace_v1`, not `kubernetes_namespace`. The non-v1 variants are deprecated and will bite you.

**cert-manager Installation Order**
CRDs must exist before applying ClusterIssuer. Install cert-manager via Helm first, add a `time_sleep` resource, then apply ClusterIssuer.

**Ingress Path Routing**
Verify if your backend expects `/api` in routes or not. Mismatched rewrite rules cause silent 404s that will waste hours of debugging.

---

## The Code

The repo is organized for multi-cloud deployment:

```
missingtable-platform-bootstrap/
├── .github/workflows/    # CI/CD pipelines
│   ├── k8s-infra-pipeline.yml
│   └── lambda-certbot-deploy.yml
├── clouds/
│   ├── aws/              # AWS-specific configs
│   └── digitalocean/     # DOKS environment
├── modules/aws/          # Reusable AWS modules
├── docs/                 # Decision log & learnings
└── scripts/              # Automation helpers
```

Everything is MIT licensed. Clone it, learn from it, adapt it.

---

## What's Next

The foundation is solid. Coming soon:

- **GKE support** — Adding Google Cloud to the rotation
- **AKS support** — Azure Kubernetes Service
- **EKS refinements** — Cost-optimized configuration for when you *need* AWS-native

The goal isn't just running on multiple clouds — it's understanding each one deeply enough to make informed trade-offs.

---

## Why This Matters for Quality Engineering

Infrastructure is software. It deserves the same rigor we apply to application code:

- **Version control** — Every change is tracked
- **Code review** — PRs for infrastructure, not ClickOps
- **Testing** — `tofu plan` before `tofu apply`
- **Reproducibility** — Same input, same output, every time

When your infrastructure is code, your environments are consistent. When environments are consistent, fewer bugs slip through. That's quality engineering at the platform level.

---

## TL;DR

> **Built:** 100% IaC multi-cloud Kubernetes platform
> **Running:** missingtable.com + qualityplaybook.dev
> **Cost:** ~$49/month (70% cheaper than AWS-only)
> **Open source:** [github.com/silverbeer/missingtable-platform-bootstrap](https://github.com/silverbeer/missingtable-platform-bootstrap)

The repo is public. The decisions are documented. The learning continues.

If you're on your own infrastructure journey — or thinking about starting one — I'd love to hear about it. Find me on [LinkedIn](https://www.linkedin.com/in/tomdrake-qe).

---

*This project was built with the help of Claude Code — an AI pair programmer that emphasizes learning over shortcuts. Every architectural decision, every debugging session, every "aha" moment is documented in the repo.*
