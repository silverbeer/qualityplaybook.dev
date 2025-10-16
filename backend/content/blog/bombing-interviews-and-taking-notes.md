---
title: "Bombing Interviews and Taking Notes: A Job Hunter's Guide"
date: 2025-10-16
tags: ["interviews", "sre", "quality-engineering", "career", "kubernetes", "observability"]
description: "I'm hunting for a new job, and honestly? I'm not great at interviews. So I'm documenting the questions I got asked — and the answers I wish I'd given."
---

Let's be real: **I'm not good at interviewing.**

I'm currently on the job hunt, looking for leadership roles in SRE/Cloud Reliability or Quality Engineering. It's tough. It's time-consuming. And sometimes, I walk out of an interview thinking, "I *know* this stuff… why couldn't I articulate it better?"

So here's what I'm doing: **documenting the questions I get asked**, along with what I *actually* said, what ChatGPT said, and what I *wish* I'd said.

Maybe this will help someone else out there who also freezes up when asked to recite the "pillars" of something they do every day.

---

## Question 1: Troubleshooting Cross-Namespace Communication in EKS

**The Question:**
> "Let's say I have two applications running in EKS in different namespaces, and they seem to be having an issue communicating to each other. Can you give me some tips on how to troubleshoot?"

**What ChatGPT Said:**

ChatGPT nailed the basics:
- Check **network policies** (they might be blocking cross-namespace traffic)
- Verify **DNS resolution** (use FQDNs like `service-name.namespace.svc.cluster.local`)
- Check the **logs** for connection errors or timeouts

All solid advice. But here's what I wish I'd added:

---

### A Better, More Complete Answer

**Start with the basics first:**

#### 1. Can the pods reach each other at all?
```bash
# Get a shell in the source pod
kubectl exec -it <pod-name> -n <namespace-a> -- sh

# Try to curl the target service
curl http://<service-name>.<namespace-b>.svc.cluster.local:8080
```

#### 2. Verify DNS is working
```bash
# From inside the pod
nslookup <service-name>.<namespace-b>.svc.cluster.local

# Check CoreDNS health
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl logs -n kube-system -l k8s-app=kube-dns --tail=50
```

#### 3. Check Network Policies
```bash
# List policies in both namespaces
kubectl get networkpolicies -n <namespace-a>
kubectl get networkpolicies -n <namespace-b>

# Inspect specific policies
kubectl describe networkpolicy <policy-name> -n <namespace-b>
```

If you see policies, check if they explicitly allow ingress from the source namespace.

#### 4. Verify Service and Endpoints
```bash
# Check if service exists and has endpoints
kubectl get svc -n <namespace-b>
kubectl get endpoints <service-name> -n <namespace-b>

# If endpoints are empty, pods might not be ready
kubectl get pods -n <namespace-b> --show-labels
```

#### 5. EKS-Specific Checks
```bash
# Check AWS VPC CNI health (EKS uses ENIs for pod networking)
kubectl get pods -n kube-system -l k8s-app=aws-node
kubectl logs -n kube-system -l k8s-app=aws-node --tail=50

# Check for IP exhaustion
kubectl describe node <node-name> | grep -A 10 Allocatable
```

#### 6. Test at Different Layers
```bash
# Layer 3: Can you reach pod IP directly?
kubectl get pods -n <namespace-b> -o wide
kubectl exec -it <pod-name> -n <namespace-a> -- curl http://<pod-ip>:8080

# Layer 4: Can you reach service ClusterIP?
kubectl get svc -n <namespace-b>
kubectl exec -it <pod-name> -n <namespace-a> -- curl http://<cluster-ip>:8080

# Layer 7: Can you reach via DNS/FQDN?
kubectl exec -it <pod-name> -n <namespace-a> -- curl http://<service>.<namespace-b>.svc.cluster.local:8080
```

This layer-by-layer approach isolates exactly where communication breaks down.

#### 7. Common EKS Gotchas
- **VPC CNI IP exhaustion:** Pods can't get IPs if the node runs out
- **Security groups:** Node security groups might be blocking traffic
- **Service mesh interference:** Check for Istio, Linkerd, or App Mesh sidecars that might be blocking traffic
- **AWS Load Balancer Controller issues:** If using Ingress, check controller logs

**The key insight:** Start simple (can pods ping each other?), then work up to more complex scenarios (network policies, DNS, service mesh).

---

## Question 2: What Are the Pillars of SRE?

**The Question:**
> "What are the pillars of SRE?"

**My Answer:**
I kind of fumbled through this. I mentioned reliability, automation, monitoring… but I didn't say it concisely.

**What ChatGPT Said:**

ChatGPT gave me the standard answer:
- **Reliability** - Making sure the system is dependable
- **Scalability** - Handling growth smoothly
- **Automation** - Reducing toil
- **Monitoring & Observability** - Metrics, logs, traces

That's not wrong. But here's the problem: **Everyone says this.** It sounds like you memorized a Wikipedia page.

---

### A Better Answer

The "pillars" concept comes from Google's SRE book. Here's a more nuanced take:

#### Google's Original Framework:
1. **Service Level Objectives (SLOs)** - Not just "reliability," but *measured* reliability
2. **Reducing Toil** - Eliminating repetitive manual work through automation
3. **Monitoring** - Knowing when things break before customers do
4. **Emergency Response** - How you handle incidents when things go wrong
5. **Change Management** - Safe, gradual rollouts (not YOLO deploys)
6. **Capacity Planning** - Scalability that's actually planned, not panic-driven

#### The Answer That Shows You've Lived It:

*"I'd break SRE into a few key areas: **SLOs and error budgets** — you can't be reliable if you don't measure it. **Reducing toil through automation** — if you're doing the same manual task twice, automate it the third time. **Observability and monitoring** — metrics, logs, and traces to understand what's happening. And **blameless post-mortems and incident response** — because things will break, and learning from failures is how you improve."*

Then add a real example:
- "In my last role, we had a 99.9% SLO, which gave us ~40 minutes of error budget per month…"
- "We automated our on-call runbooks, reducing incident response time from 15 minutes to 3…"

#### The Cultural Framing (If You Want to Stand Out):

Some people frame SRE around **culture**, not just tech:
1. **Error budgets over perfection** - 100% uptime is a lie; balance innovation vs reliability
2. **Toil reduction as a feature** - Every quarter, eliminate 10% of manual work
3. **Blameless culture** - Incidents are learning opportunities
4. **Data-driven decisions** - SLOs, SLIs, monitoring - measure everything
5. **Shared responsibility** - Dev teams own production, SRE enables them

**Why this is better:** It shows you understand SRE is as much about *culture* and *process* as it is about tools.

---

### The Honest Truth

If they ding you for not saying "the four pillars" in the exact right order, that's a **them problem**, not a you problem. A good interviewer would recognize you understand the concepts and care more about your real experience than buzzword recitation.

---

## Question 3: What Are the Golden Signals?

**The Question:**
> "What are the pillars of observability? Or something golden?"

**My Answer:**
I totally blanked. I said, "Golden? Uh… I'm not sure what you mean."

Then the interviewer explained it was "golden signals," and I was like, "Oh! Yeah, I know this stuff, I just didn't know the phrase."

**What ChatGPT Said:**

ChatGPT clarified two concepts:

### The Three Pillars of Observability:
1. **Metrics** - Numerical data (CPU, memory, request rate)
2. **Logs** - Event records (errors, user actions)
3. **Traces** - Request flow through distributed systems

### The Four Golden Signals (Google SRE Book):
1. **Latency** - How long requests take
2. **Traffic** - How much demand (requests/sec)
3. **Errors** - Rate of failed requests
4. **Saturation** - How "full" your resources are

I asked a follow-up: *"Is 'errors' just non-200 responses vs total requests?"*

ChatGPT confirmed: **Yes, basically.** Errors = failed requests (4xx, 5xx, timeouts).

---

### A Better, More Complete Answer

#### The Three Pillars of Observability

You need **all three** to truly understand what's happening:

- **Metrics** tell you WHAT is broken
- **Logs** tell you WHY it broke
- **Traces** tell you WHERE in the system it broke

**Real example:**
- Metric: "Error rate spiked to 15%"
- Log: "Database connection timeout after 5s"
- Trace: "Request spent 4.8s waiting in auth service before timing out"

→ Now you know it's the auth service's database connection, not the API gateway.

#### The Four Golden Signals

1. **Latency** - Response time (p50, p95, p99 percentiles)
2. **Traffic** - Request volume (requests/sec, bandwidth)
3. **Errors** - Failed request rate
4. **Saturation** - How close to capacity you are

#### About Errors:
Yes, **errors** is typically:
```
error_rate = (non-2xx responses) / (total requests)
```

But it's more nuanced:
- **Client errors (4xx):** Often not your fault (bad user input)
- **Server errors (5xx):** Usually your problem
- **Timeouts:** Might not show as 5xx but still failures
- **Failed retries:** Connection refused, circuit breaker open

In a real SRE role, you'd track:
```
# HTTP error rate
sum(rate(http_requests_total{status=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))
```

#### About Saturation:
Saturation isn't just "how full is my CPU?" It's **how close to capacity where performance degrades**.

Examples:
- **CPU saturation:** 80%+ sustained → response times increase
- **Memory saturation:** 90%+ → OOM kills incoming
- **Database saturation:** Connection pool maxed → requests timeout
- **Queue saturation:** Message queue depth growing → backlog building

---

### How to Handle This Next Time

When you don't know the exact phrase, bridge to what you DO know:

**Interviewer:** "What are the golden signals?"

**Better answer:**
*"I'm not familiar with that exact term — is this the four key metrics from Google's SRE book? Latency, throughput, errors, and resource utilization? Or are you referring to the three pillars of observability?"*

This shows:
1. You're honest about not knowing the buzzword
2. You know multiple related frameworks
3. You can triangulate to the right answer

**Or even more direct:**
*"I don't recall that specific term, but in my last role we focused on response time, error rate, request volume, and resource saturation for monitoring. Is that what you're referring to?"*

Now you've demonstrated real experience instead of just vocab memorization.

---

### My Reflection

> "I probably will get passed for this job. I do know this stuff but didn't know the phrase."

**Reality check:** If they pass on you for not knowing a buzzword, that's a **them problem**, not yours.

A good interviewer would:
- Recognize you understood the concepts when explained
- Value your follow-up questions showing curiosity
- Care more about how you've applied these principles

If they ding you for this? They're looking for someone who read the book, not someone who does the work.

But I get it. Job hunting is rough, and every "miss" feels like you blew it. You didn't.

---

## Question 4: How Do You Test Rate Limiting?

**The Question:**
> "How do you test rate limiting?"

**My Answer:**
"I understand how the rate limiting works, then put the server under load to trigger it."

**What ChatGPT Said:**

ChatGPT validated my answer and added polish:
- Use tools like Locust, JMeter, or custom Python scripts
- Test different scenarios (gradual load, burst traffic)
- Monitor what happens after the limit is hit (429 responses, graceful recovery)

Solid. But here's the SRE/QE depth version:

---

### A Better, More Complete Answer

#### 1. Understand the Rate Limiting Strategy First

Before you test, know:
- **Algorithm:** Token bucket? Leaky bucket? Fixed window? Sliding window?
- **Scope:** Per user? Per IP? Per API key? Global?
- **Limits:** 100 req/min? 1000 req/hour? Different tiers?
- **Behavior:** Hard block? Throttle? Queue?

**Example answer:**
*"First, I'd confirm the rate limiting implementation — is it token bucket, fixed window, or sliding window? Then I'd identify the limits per scope — per user ID, IP address, or API key."*

#### 2. Test Different Scenarios

**A. Gradual Load Testing**
```bash
# Using hey (simple HTTP load generator)
hey -n 1000 -c 10 -q 5 https://api.example.com/endpoint

# Or Apache Bench
ab -n 1000 -c 10 https://api.example.com/endpoint

# Or k6 (modern)
k6 run --vus 10 --duration 30s rate-limit-test.js
```

**B. Burst Testing**
```bash
# Send 200 requests instantly
seq 1 200 | xargs -P 200 -I {} curl https://api.example.com/endpoint

# Or with vegeta
echo "GET https://api.example.com/endpoint" | vegeta attack -rate=500/s -duration=5s
```

**C. Edge Cases**
- Hit the limit exactly (if it's 100/min, send 100)
- Hit limit + 1
- Hit limit, wait for reset, hit again
- Test different users hitting limit simultaneously

#### 3. Verify Correct Behavior

**Check HTTP responses:**
```bash
# Should return 429 Too Many Requests
curl -i https://api.example.com/endpoint

# Should include proper headers:
HTTP/1.1 429 Too Many Requests
Retry-After: 60
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1697654400
```

**Verify rate limit headers:**
- `X-RateLimit-Limit`: Max requests allowed
- `X-RateLimit-Remaining`: How many left
- `X-RateLimit-Reset`: When it resets

#### 4. Test System Behavior

The real SRE question: **What happens to the system when rate limited?**

- Does it queue requests or drop them?
- Do upstream services get overwhelmed?
- Does it affect other users/endpoints?
- Can you cause a cascading failure?
- Does the rate limiter itself become a bottleneck?

**Better answer:**
*"I'd also test how the system behaves when rate limited. Does it gracefully return 429s or do requests time out? Can I overwhelm the rate limiter itself? And I'd check if rate limiting one endpoint affects others."*

#### 5. Automated Testing Example

```python
import pytest
import requests
import time

BASE_URL = "https://api.example.com"
RATE_LIMIT = 100

def test_rate_limit_enforced():
    """Test that rate limit is enforced"""
    responses = []

    for i in range(RATE_LIMIT + 10):
        r = requests.get(f"{BASE_URL}/endpoint")
        responses.append(r.status_code)

    # First RATE_LIMIT should succeed
    assert responses[:RATE_LIMIT].count(200) == RATE_LIMIT

    # Rest should be rate limited
    assert responses[RATE_LIMIT:].count(429) == 10

def test_rate_limit_resets():
    """Test that rate limit resets after window"""
    # Hit rate limit
    for i in range(RATE_LIMIT):
        requests.get(f"{BASE_URL}/endpoint")

    # Should be rate limited
    r = requests.get(f"{BASE_URL}/endpoint")
    assert r.status_code == 429

    # Wait for reset
    time.sleep(60)

    # Should work again
    r = requests.get(f"{BASE_URL}/endpoint")
    assert r.status_code == 200
```

#### 6. Real-World Considerations

- **Distributed systems:** "If it's running in Kubernetes with multiple replicas, is rate limiting shared across pods or per-pod?"
- **Rate limiter implementation:** "Is it Redis-based (centralized), in-memory, or using AWS API Gateway?"
- **Production testing:** "I'd test with real traffic patterns using shadow traffic or canary deployments"

---

### The Interview-Winning Answer

*"I'd start by understanding the rate limiting strategy — algorithm, limits, and scope. Then I'd use load testing tools like k6 or vegeta to test gradual load, burst traffic, and edge cases. I'd verify we return proper 429 responses with correct headers. I'd also test system behavior — does it affect other endpoints, can we overwhelm the rate limiter itself. Finally, I'd automate these tests in CI/CD."*

**Then add a real example:**
*"In my last role, we found our rate limiter was per-pod, not cluster-wide, which meant users could bypass limits by hitting different replicas. We caught this during load testing and switched to a Redis-based solution."*

---

## The Takeaway

Interviewing is hard. Job hunting is exhausting. And sometimes you know the answer but can't articulate it in the moment.

So I'm documenting these questions — not because I nailed them, but because I didn't. And maybe writing them down will help me (and you) do better next time.

If you're also on the job hunt, hang in there. We've got this. 💪

---

*I'm actively looking for leadership roles in SRE/Cloud Reliability and Quality Engineering. If you found this helpful (or have interview tips), connect with me on [LinkedIn](https://www.linkedin.com/in/tomdrake-qe).*
