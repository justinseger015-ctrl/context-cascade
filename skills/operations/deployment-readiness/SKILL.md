---

## CRITICAL: DEPLOYMENT SAFETY GUARDRAILS

**BEFORE any deployment, validate**:
- [ ] All tests passing (unit, integration, E2E, load)
- [ ] Security scan completed (SAST, DAST, dependency audit)
- [ ] Infrastructure capacity verified (CPU, memory, disk, network)
- [ ] Database migrations tested on production-like data volume
- [ ] Rollback procedure documented with time estimates

**NEVER**:
- Deploy without comprehensive monitoring (metrics, logs, traces)
- Skip load testing for high-traffic services
- Deploy breaking changes without backward compatibility
- Ignore security vulnerabilities in production dependencies
- Deploy without incident response plan

**ALWAYS**:
- Validate deployment checklist before proceeding
- Use feature flags for risky changes (gradual rollout)
- Monitor error rates, latency p99, and saturation metrics
- Document deployment in runbook with troubleshooting steps
- Retain deployment artifacts for forensic analysis

**Evidence-Based Techniques for Deployment**:
- **Chain-of-Thought**: Trace deployment flow (code -> artifact -> registry -> cluster -> pods)
- **Program-of-Thought**: Model deployment as state machine (pre-deploy -> deploy -> post-deploy -> verify)
- **Reflection**: After deployment, analyze what worked vs assumptions
- **Retrieval-Augmented**: Query past incidents for similar deployment patterns

name: deployment-readiness
description: Production deployment validation for Deep Research SOP Pipeline H ensuring
  models ready for real-world deployment. Use before deploying to production, creating
  deployment plans, or validating infrastructure requirements. Validates performance
  benchmarks, monitoring setup, incident response plans, rollback strategies, and
  infrastructure scalability for Quality Gate 3.
version: 1.1.0
category: operations
tags:
- operations
- deployment
- infrastructure
author: ruv
cognitive_frame:
  primary: aspectual
  secondary: classifier
  rationale: "Deployment tracking requires explicit state management (aspectual) and type/risk classification (classifier)"
---

# Deployment Readiness

Validate ML models and systems for production deployment, ensuring operational readiness across performance, monitoring, security, and incident management dimensions.

---

## Aspektual'naya Ramka (Deployment State Tracking)

### Tipy Sostoyaniya (State Types)

**Perfective [SV] - Completed Actions**:
- `[SV:ZAVERSHENO]` - Stage fully completed
- `[SV:PROVERENO]` - Validated and verified
- `[SV:ODOBRENO]` - Approved for next stage
- `[SV:RAZVERNUTO]` - Deployed successfully

**Imperfective [NSV] - Ongoing/Incomplete Actions**:
- `[NSV:V_PROTSESSE]` - Stage actively in progress
- `[NSV:VYPOLNYAETSYA]` - Currently executing
- `[NSV:TESTIRUYETSYA]` - Testing in progress
- `[NSV:MONITORITSYA]` - Under monitoring

**Blocked/Special States**:
- `[ZABLOKIROVANO]` - Blocked by dependency
- `[OZHIDAET]` - Waiting for prerequisite
- `[OTKAT]` - Rollback initiated
- `[AVARIYA]` - Emergency state

### Deployment Pipeline States

```
Infrastructure Setup:
  Capacity Planning      [SV|NSV|ZABLOKIROVANO]
  Environment Setup      [SV|NSV|ZABLOKIROVANO]
  Network Configuration  [SV|NSV|ZABLOKIROVANO]
  → Output: [SV:ZAVERSHENO] or [NSV:V_PROTSESSE]

Performance Benchmarking:
  Latency Testing        [SV|NSV|ZABLOKIROVANO]
  Throughput Testing     [SV|NSV|ZABLOKIROVANO]
  Resource Utilization   [SV|NSV|ZABLOKIROVANO]
  → Output: [SV:PROVERENO] or [NSV:TESTIRUYETSYA]

Monitoring Setup:
  Metrics Collection     [SV|NSV|ZABLOKIROVANO]
  Alerting Configuration [SV|NSV|ZABLOKIROVANO]
  Dashboard Creation     [SV|NSV|ZABLOKIROVANO]
  → Output: [SV:ODOBRENO] or [NSV:V_PROTSESSE]

Deployment Execution:
  Staging Deployment     [SV|NSV|ZABLOKIROVANO|OTKAT]
  Production Deployment  [SV|NSV|ZABLOKIROVANO|OTKAT|AVARIYA]
  Post-Deploy Validation [SV|NSV|ZABLOKIROVANO]
  → Output: [SV:RAZVERNUTO] or [OTKAT] or [AVARIYA]
```

### State Transition Rules

1. **Sequential Progression**: `[NSV] → [SV] → Next Stage [NSV]`
2. **Rollback Path**: `[AVARIYA] → [OTKAT] → Previous [SV]`
3. **Blocking Cascade**: Parent `[ZABLOKIROVANO]` → Children `[OZHIDAET]`
4. **Monitoring Loop**: `[SV:RAZVERNUTO] → [NSV:MONITORITSYA]` (continuous)

### Example State Tracking Output

```markdown
## Deployment Status Report - 2025-12-19 14:32:00

### Infrastructure Validation [SV:ZAVERSHENO]
- Capacity Planning: [SV:ZAVERSHENO] at 2025-12-19 10:15
- Environment Setup: [SV:ZAVERSHENO] at 2025-12-19 12:45
- Network Configuration: [SV:PROVERENO] at 2025-12-19 13:20

### Performance Benchmarking [NSV:TESTIRUYETSYA]
- Latency Testing: [SV:PROVERENO] at 2025-12-19 14:00
- Throughput Testing: [NSV:VYPOLNYAETSYA] started 2025-12-19 14:15
- Resource Utilization: [OZHIDAET] (blocked by throughput test)

### Monitoring Setup [OZHIDAET]
- Blocked by: Performance Benchmarking [NSV:TESTIRUYETSYA]

### Deployment Execution [OZHIDAET]
- Blocked by: All prerequisites must be [SV:ZAVERSHENO]
```

---

## Liangci Kuangjia (Deployment Classification Framework)

### Deployment Type Classifiers

**FEATURE (xin gong-neng)** - New Functionality
- Risk: MEDIUM-HIGH
- Testing: Comprehensive E2E required
- Rollback: Feature flag toggle
- Monitoring: New metrics for feature usage
- Example: "New payment gateway integration"

**HOTFIX (jin-ji xiu-fu)** - Critical Bug Fix
- Risk: HIGH (expedited process)
- Testing: Focused regression on affected area
- Rollback: Immediate revert capability required
- Monitoring: Error rate alerts with 1-min interval
- Example: "Fix authentication bypass vulnerability"

**ROLLBACK (hui-gun)** - Revert to Previous Version
- Risk: LOW-MEDIUM (known good state)
- Testing: Smoke tests only
- Rollback: N/A (is rollback)
- Monitoring: Verify previous metrics restored
- Example: "Revert failed v2.3.0 deployment"

**CONFIG (pei-zhi)** - Configuration-Only Change
- Risk: LOW
- Testing: Config validation, no code changes
- Rollback: Config file revert
- Monitoring: Service health checks
- Example: "Update feature flag percentages"

**MIGRATION (qian-yi)** - Database/Infrastructure Migration
- Risk: CRITICAL
- Testing: Full backup, dry-run in staging
- Rollback: Migration rollback script required
- Monitoring: Database metrics, query performance
- Example: "Migrate PostgreSQL 15 to 16"

### Risk Level Classifiers

**HIGH (gao feng-xian)** - Breaking Changes
- Database migrations with data transformation
- Authentication/authorization changes
- Payment processing modifications
- Third-party API version upgrades
- Multi-service coordination required
- **Gate Requirement**: Manual approval + 24hr monitoring

**MEDIUM (zhong feng-xian)** - Standard Features
- New API endpoints (backward compatible)
- UI component updates
- Non-critical service additions
- Dependency minor version updates
- **Gate Requirement**: Automated tests + smoke tests

**LOW (di feng-xian)** - Minor Updates
- Documentation changes
- Logging improvements
- Configuration tweaks (non-breaking)
- UI copy changes
- **Gate Requirement**: Basic validation only

### Environment Progression Classifier

**DEV (kai-fa huan-jing)** - Development Environment
- Purpose: Rapid iteration, breaking changes allowed
- Deployment: Continuous (on every commit)
- Monitoring: Basic logs, no SLA
- Rollback: Not required

**STAGING (yan-zheng huan-jing)** - Staging Environment
- Purpose: Production-like validation
- Deployment: Daily or on-demand
- Monitoring: Full observability stack
- Rollback: Required, tested before prod
- **Gate**: Must pass ALL tests before prod promotion

**PRODUCTION (sheng-chan huan-jing)** - Production Environment
- Purpose: Live customer traffic
- Deployment: Scheduled windows only
- Monitoring: 24/7 alerting, SLA tracking
- Rollback: <5 min SLA, tested in staging
- **Gate**: Requires staging validation + approvals

### Deployment Strategy Classifier

**BLUE-GREEN (lan-lv bu-shu)** - Zero-Downtime Switch
- Two identical environments (blue=current, green=new)
- Traffic switch is instantaneous
- Rollback: Switch traffic back to blue
- Best for: HOTFIX, FEATURE with high confidence

**CANARY (jin-si-que bu-shu)** - Gradual Rollout
- Progressive traffic shift: 5% → 25% → 50% → 100%
- Monitor metrics at each stage
- Rollback: Reduce traffic to 0%
- Best for: FEATURE, MIGRATION with uncertainty

**ROLLING (gun-dong bu-shu)** - Instance-by-Instance Update
- Update instances sequentially
- Maintain minimum capacity during update
- Rollback: Reverse instance updates
- Best for: CONFIG, low-risk FEATURE

**BIG-BANG (yi-ci-xing bu-shu)** - All-at-Once Deployment
- Replace all instances simultaneously
- Downtime window required
- Rollback: Full redeployment of previous version
- Best for: MIGRATION (database), scheduled maintenance

### Classification Decision Matrix

```yaml
deployment_classification:
  type: FEATURE
  risk: HIGH
  environments:
    - DEV [SV:RAZVERNUTO]
    - STAGING [NSV:TESTIRUYETSYA]
    - PRODUCTION [OZHIDAET]
  strategy: CANARY
  rollback_plan: blue-green-fallback
  monitoring:
    - error_rate: <5% threshold
    - latency_p95: <200ms threshold
    - saturation: <80% threshold
  gates_passed:
    - tests: [SV:PROVERENO] 100% pass
    - security: [SV:ODOBRENO] zero critical issues
    - performance: [NSV:VYPOLNYAETSYA] benchmarking in progress
```

### Output Template: Deployment Classification Report

```markdown
# Deployment Classification Report

**Deployment ID**: DEPLOY-2025-12-19-001
**Timestamp**: 2025-12-19T14:32:00Z
**Requested By**: platform-team

## Classification

- **Type**: FEATURE (xin gong-neng) - Payment gateway v2
- **Risk Level**: HIGH (gao feng-xian) - Third-party API integration
- **Strategy**: CANARY (jin-si-que bu-shu) - 5% → 25% → 50% → 100%
- **Environment**: STAGING (yan-zheng huan-jing) → PRODUCTION (sheng-chan huan-jing)

## State Tracking

### Infrastructure [SV:ZAVERSHENO]
- Capacity Planning: [SV:ZAVERSHENO] ✓
- Environment Setup: [SV:ZAVERSHENO] ✓
- Load Balancer Config: [SV:PROVERENO] ✓

### Testing [NSV:VYPOLNYAETSYA]
- Unit Tests: [SV:PROVERENO] 100% pass ✓
- Integration Tests: [NSV:VYPOLNYAETSYA] 87/100 pass (in progress)
- Load Tests: [OZHIDAET] (blocked by integration tests)

### Deployment Gates
- Gate 1 (Security): [SV:ODOBRENO] ✓
- Gate 2 (Performance): [NSV:TESTIRUYETSYA] (pending load tests)
- Gate 3 (Approval): [OZHIDAET] (requires Gate 2)

## Rollback Plan

- **Strategy**: Blue-Green fallback
- **RTO**: <5 minutes
- **Procedure**: `kubectl patch service payment-gateway -p '{"spec":{"selector":{"version":"blue"}}}'`
- **Validation**: [SV:PROVERENO] tested in staging

## Risk Mitigation

- **HIGH Risk Items**:
  - Payment processing: Feature flag at 5% initial rollout
  - Database migration: Separate deployment, tested with prod-like data
  - Third-party API: Circuit breaker configured (timeout: 3s, failure threshold: 5)

- **Monitoring Alerts**:
  - Payment failure rate >2%: Auto-rollback
  - API latency p95 >500ms: Alert + manual review
  - Error spike >10x baseline: Auto-rollback

## Recommendation

**Status**: [ZABLOKIROVANO] - DO NOT DEPLOY
**Reason**: Integration tests incomplete (87/100), load tests not started
**Next Steps**:
1. Complete integration tests → [SV:PROVERENO]
2. Run load tests → [SV:PROVERENO]
3. Gate 2 approval → [SV:ODOBRENO]
4. Schedule deployment window (Tuesday 10am-12pm)
```

---

## Overview

**Purpose**: Validate production deployment readiness

**When to Use**:
- Before deploying models to production (Phase 3)
- Quality Gate 3 validation required
- Creating deployment plans
- Infrastructure capacity planning
- Production environment testing

**Quality Gate**: Required for Quality Gate 3 APPROVED status

**Prerequisites**:
- Model trained and evaluated (Gate 2 APPROVED)
- Reproducibility audit passed
- Production environment available for testing
- Infrastructure requirements documented

**Outputs**:
- Deployment readiness report (PASS/FAIL)
- Infrastructure requirements specification
- Monitoring plan with alerts and dashboards
- Incident response plan
- Rollback strategy
- Performance benchmarks (production environment)
- Deployment checklist

**Time Estimate**: 1-2 weeks
- Infrastructure setup: 2-3 days
- Performance benchmarking: 1-2 days
- Monitoring setup: 2-3 days
- Security validation: 1-2 days
- Documentation: 1-2 days

**Agents Used**: tester, archivist

---

## Quick Start

### 1. Infrastructure Requirements
```yaml
# deployment/infrastructure_requirements.yaml

compute:
  gpu:
    type: "NVIDIA A100"
    count: 2
    memory: "80GB each"
  cpu:
    cores: 32
    memory: "256GB"

storage:
  model_weights: "50GB"
  datasets: "500GB"
  logs: "100GB"

network:
  ingress_bandwidth: "10Gbps"
  egress_bandwidth: "10Gbps"
  latency_target: "<100ms p95"

scalability:
  min_instances: 2
  max_instances: 10
  autoscaling_metric: "requests_per_second"
  target_utilization: 70%
```

### 2. Performance Benchmarking
```bash
# Benchmark in production environment
python scripts/production_benchmarks.py \
  --model deployment/model.pth \
  --environment production \
  --metrics "latency,throughput,memory,cpu" \
  --duration 3600 \
  --output deployment/benchmarks.json
```

### 3. Monitoring Setup
```bash
# Deploy monitoring stack (Prometheus + Grafana)
docker-compose -f deployment/monitoring/docker-compose.yml up -d

# Configure alerts
kubectl apply -f deployment/monitoring/alerts.yaml

# Test alert pipeline
python scripts/test_alerts.py --alert-manager http://localhost:9093
```

### 4. Deployment Plan
```bash
# Generate deployment plan
python scripts/generate_deployment_plan.py \
  --model deployment/model.pth \
  --infrastructure deployment/infrastructure_requirements.yaml \
  --output deployment/deployment_plan.md
```

### 5. Validate Deployment Readiness
```bash
# Run comprehensive readiness checks
python scripts/validate_deployment_readiness.py \
  --deployment-plan deployment/deployment_plan.md \
  --benchmarks deployment/benchmarks.json \
  --monitoring-config deployment/monitoring/ \
  --output deployment/readiness_report.md
```

---

## Detailed Instructions

### Phase 1: Infrastructure Validation (2-3 days)

**Objective**: Validate production infrastructure meets requirements

**Steps**:

#### 1.1 Capacity Planning
```python
# scripts/capacity_planning.py

def estimate_capacity_requirements(model, workload):
    """Estimate infrastructure requirements."""
    # GPU requirements
    gpu_memory_per_batch = estimate_gpu_memory(model, batch_size=32)
    num_gpus = math.ceil(gpu_memory_per_batch * target_throughput / gpu_capacity)

    # CPU requirements
    cpu_cores = estimate_cpu_usage(model, workload)

    # Storage requirements
    storage_model = model_size_gb
    storage_data = dataset_size_gb
    storage_logs = estimated_logs_per_day_gb * retention_days

    return {
        "gpu": {"count": num_gpus, "memory_per_gpu": gpu_capacity},
        "cpu": {"cores": cpu_cores},
        "storage": {
            "total": storage_model + storage_data + storage_logs
        }
    }

# Run capacity planning
requirements = estimate_capacity_requirements(model, expected_workload)
print(f"Infrastructure Requirements: {requirements}")
```

**Deliverable**: Infrastructure requirements specification

---

#### 1.2 Environment Setup
```bash
# Setup production environment
# Using Kubernetes for orchestration

# 1. Create namespace
kubectl create namespace ml-production

# 2. Deploy model serving (TorchServe, TensorFlow Serving, or custom)
kubectl apply -f deployment/kubernetes/model-serving.yaml

# 3. Deploy load balancer
kubectl apply -f deployment/kubernetes/load-balancer.yaml

# 4. Verify deployment
kubectl get pods -n ml-production
kubectl get services -n ml-production
```

**Deliverable**: Production environment deployed

---

### Phase 2: Performance Benchmarking (1-2 days)

**Objective**: Measure performance in production environment

**Steps**:

#### 2.1 Latency Benchmarking
```python
# scripts/benchmark_latency.py
import time
import numpy as np

def benchmark_latency(model, test_inputs, num_runs=1000):
    """Benchmark inference latency."""
    latencies = []

    for _ in range(num_runs):
        start = time.perf_counter()
        output = model(test_inputs)
        end = time.perf_counter()
        latencies.append((end - start) * 1000)  # Convert to ms

    results = {
        "mean": np.mean(latencies),
        "std": np.std(latencies),
        "p50": np.percentile(latencies, 50),
        "p95": np.percentile(latencies, 95),
        "p99": np.percentile(latencies, 99)
    }

    print(f"Latency Results (ms):")
    print(f"  Mean: {results['mean']:.2f}")
    print(f"  P50: {results['p50']:.2f}")
    print(f"  P95: {results['p95']:.2f}")
    print(f"  P99: {results['p99']:.2f}")

    # Check against SLA (e.g., P95 < 100ms)
    sla_p95 = 100.0
    if results['p95'] > sla_p95:
        print(f"⚠️  WARNING: P95 latency {results['p95']:.2f}ms exceeds SLA {sla_p95}ms")
        return False
    else:
        print(f"✅ PASS: P95 latency {results['p95']:.2f}ms within SLA")
        return True

# Run benchmark
benchmark_latency(model, test_inputs)
```

**Deliverable**: Latency benchmarks

---

#### 2.2 Throughput Benchmarking
```python
# scripts/benchmark_throughput.py

def benchmark_throughput(model, duration_seconds=3600):
    """Benchmark queries per second (QPS)."""
    start_time = time.time()
    requests_processed = 0

    while time.time() - start_time < duration_seconds:
        # Simulate request
        output = model(test_input)
        requests_processed += 1

    elapsed = time.time() - start_time
    qps = requests_processed / elapsed

    print(f"Throughput: {qps:.2f} QPS")

    # Check against target (e.g., 100 QPS)
    target_qps = 100.0
    if qps < target_qps:
        print(f"⚠️  WARNING: Throughput {qps:.2f} QPS below target {target_qps}")
        return False
    else:
        print(f"✅ PASS: Throughput {qps:.2f} QPS meets target")
        return True

# Run benchmark
benchmark_throughput(model)
```

**Deliverable**: Throughput benchmarks

---

#### 2.3 Resource Utilization
```bash
# Monitor GPU/CPU/Memory utilization during load test
# Using NVIDIA SMI for GPUs
nvidia-smi dmon -s pucvmet -c 3600 > deployment/gpu_utilization.log &

# Using psutil for CPU/Memory
python scripts/monitor_resources.py --duration 3600 --output deployment/resource_utilization.json &

# Run load test
python scripts/load_test.py --requests-per-second 100 --duration 3600

# Analyze utilization
python scripts/analyze_utilization.py \
  --gpu deployment/gpu_utilization.log \
  --cpu deployment/resource_utilization.json \
  --target-utilization 70 \
  --output deployment/utilization_report.md
```

**Deliverable**: Resource utilization report

---

### Phase 3: Monitoring & Observability (2-3 days)

**Objective**: Set up comprehensive monitoring

**Steps**:

#### 3.1 Metrics Collection
```yaml
# deployment/monitoring/prometheus.yml

global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'model-serving'
    static_configs:
      - targets: ['model-serving:8080']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'gpu-exporter'
    static_configs:
      - targets: ['dcgm-exporter:9400']
```

**Key Metrics**:
- **Inference Metrics**: Latency (P50, P95, P99), throughput (QPS), error rate
- **Resource Metrics**: GPU utilization, CPU utilization, memory usage
- **Business Metrics**: Requests per user, predictions per day, model drift

---

#### 3.2 Alerting
```yaml
# deployment/monitoring/alerts.yaml

groups:
  - name: model_serving_alerts
    interval: 30s
    rules:
      # High latency alert
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(inference_duration_seconds_bucket[5m])) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High inference latency"
          description: "P95 latency {{ $value }}s exceeds 100ms threshold"

      # Low throughput alert
      - alert: LowThroughput
        expr: rate(inference_requests_total[5m]) < 50
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Low throughput"
          description: "QPS {{ $value }} below 50 threshold"

      # High error rate alert
      - alert: HighErrorRate
        expr: rate(inference_errors_total[5m]) / rate(inference_requests_total[5m]) > 0.05
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "High error rate"
          description: "Error rate {{ $value | humanizePercentage }} exceeds 5%"

      # GPU out of memory alert
      - alert: GPUOutOfMemory
        expr: DCGM_FI_DEV_FB_FREE / DCGM_FI_DEV_FB_USED < 0.1
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "GPU out of memory"
          description: "GPU memory usage > 90%"
```

**Deliverable**: Alerting configuration

---

#### 3.3 Dashboards
```json
// deployment/monitoring/grafana_dashboard.json

{
  "dashboard": {
    "title": "ML Model Production Monitoring",
    "panels": [
      {
        "title": "Inference Latency (P95)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(inference_duration_seconds_bucket[5m]))"
          }
        ]
      },
      {
        "title": "Requests Per Second",
        "targets": [
          {
            "expr": "rate(inference_requests_total[1m])"
          }
        ]
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(inference_errors_total[5m]) / rate(inference_requests_total[5m])"
          }
        ]
      },
      {
        "title": "GPU Utilization",
        "targets": [
          {
            "expr": "DCGM_FI_DEV_GPU_UTIL"
          }
        ]
      }
    ]
  }
}
```

**Deliverable**: Monitoring dashboards

---

### Phase 4: Incident Response (1-2 days)

**Objective**: Prepare incident response plan

**Steps**:

#### 4.1 Incident Response Plan
```markdown
# Incident Response Plan

## Severity Levels

### P0 - Critical (Production Down)
- **Response Time**: 15 minutes
- **Resolution Time**: 2 hours
- **Escalation**: Immediate page on-call engineer

### P1 - High (Degraded Performance)
- **Response Time**: 30 minutes
- **Resolution Time**: 4 hours
- **Escalation**: Email + Slack alert

### P2 - Medium (Minor Issues)
- **Response Time**: 2 hours
- **Resolution Time**: 24 hours
- **Escalation**: Create ticket

## Runbooks

### High Latency Runbook
1. Check current load (QPS)
2. Check GPU/CPU utilization
3. Scale up instances if utilization >80%
4. Check for model drift (retrain if needed)
5. Roll back to previous version if issue persists

### High Error Rate Runbook
1. Check error logs
2. Identify error type (input validation, OOM, model error)
3. If input validation: Update input schema
4. If OOM: Reduce batch size or add GPU
5. If model error: Roll back to previous version

### GPU Out of Memory Runbook
1. Reduce batch size
2. Enable gradient checkpointing
3. Use mixed precision (FP16)
4. Scale up to larger GPU (A100 80GB)
5. Implement model parallelism
```

**Deliverable**: Incident response plan

---

#### 4.2 Rollback Strategy
```bash
# deployment/rollback.sh

#!/bin/bash
set -e

# Rollback strategy: Blue-Green Deployment

echo "Starting rollback to previous version..."

# 1. Verify previous version exists
if [ ! -f "deployment/previous_version.yaml" ]; then
    echo "ERROR: Previous version not found"
    exit 1
fi

# 2. Deploy previous version (green)
kubectl apply -f deployment/previous_version.yaml

# 3. Wait for deployment to be ready
kubectl wait --for=condition=available --timeout=300s deployment/model-serving-green

# 4. Switch traffic to green (previous version)
kubectl patch service model-serving -p '{"spec":{"selector":{"version":"green"}}}'

# 5. Verify rollback successful
python scripts/verify_deployment.py --expected-version green

# 6. Terminate blue (failed version)
kubectl delete deployment model-serving-blue

echo "✅ Rollback completed successfully"
```

**Deliverable**: Rollback strategy

---

### Phase 5: Security Validation (1-2 days)

**Objective**: Validate security posture

**Criteria**:

#### 5.1 Authentication & Authorization
- [ ] API requires authentication (API keys, OAuth)
- [ ] Role-based access control (RBAC) implemented
- [ ] Rate limiting configured (prevent abuse)

#### 5.2 Data Security
- [ ] Data encrypted in transit (TLS 1.3)
- [ ] Data encrypted at rest (AES-256)
- [ ] PII handling compliant with GDPR/HIPAA

#### 5.3 Model Security
- [ ] Model weights access controlled
- [ ] Adversarial input detection enabled
- [ ] Input validation implemented

#### 5.4 Infrastructure Security
- [ ] Network policies configured (Kubernetes NetworkPolicy)
- [ ] Container security scanning enabled (Trivy, Aqua)
- [ ] Secrets management (Vault, Kubernetes Secrets)

**Deliverable**: Security validation checklist

---

### Phase 6: Documentation (1-2 days)

**Objective**: Document deployment procedures

**Deliverables**:

#### 6.1 Deployment Checklist
```markdown
# Deployment Checklist

## Pre-Deployment
- [ ] Model trained and Gate 2 APPROVED
- [ ] Reproducibility audit passed
- [ ] Performance benchmarks meet SLA
- [ ] Monitoring configured and tested
- [ ] Alerts configured and tested
- [ ] Incident response plan documented
- [ ] Rollback strategy tested
- [ ] Security validation passed

## Deployment
- [ ] Deploy to staging environment
- [ ] Run smoke tests in staging
- [ ] Deploy to production (canary or blue-green)
- [ ] Monitor metrics for 24 hours
- [ ] Gradually ramp traffic (10% → 50% → 100%)

## Post-Deployment
- [ ] Verify all metrics within SLA
- [ ] Check error logs
- [ ] Confirm alerts working
- [ ] Update documentation
- [ ] Notify stakeholders
```

#### 6.2 Operations Manual
- Deployment procedures
- Scaling procedures
- Monitoring procedures
- Troubleshooting guide
- Runbooks for common issues

**Deliverable**: Complete deployment documentation

---

## Integration with Deep Research SOP

### Pipeline Integration
- **Pipeline H (Deployment Readiness)**: This skill validates production deployment readiness
- **Quality Gate 3**: Deployment readiness PASS required for Gate 3 APPROVED

### Agent Coordination
```
tester agent performs performance benchmarking and monitoring setup
  ↓
archivist agent documents deployment procedures
  ↓
evaluator agent validates Gate 3
```

---

## Troubleshooting

### Issue: High latency (>100ms P95)
**Solution**: Scale up instances, optimize model (quantization, pruning), use faster hardware

### Issue: Low throughput (<100 QPS)
**Solution**: Increase batch size, use model parallelism, optimize data loading

### Issue: Gate 3 validation fails
**Solution**: Ensure all deployment readiness criteria met (performance, monitoring, incident response)

---

## Related Skills and Commands

### Prerequisites
- `holistic-evaluation` - Performance evaluation complete
- `reproducibility-audit` - Reproducibility validated

### Next Steps
- `research-publication` - Academic publication
- `gate-validation --gate 3` - Gate 3 validation

---

## References

### Deployment Best Practices
- Google SRE Handbook
- AWS Well-Architected Framework
- Kubernetes Best Practices

### Monitoring Standards
- Prometheus Best Practices
- OpenTelemetry
- The Four Golden Signals (Latency, Traffic, Errors, Saturation)

---

## Changelog

### Version 1.1.0 (2025-12-19)

**Added**:
- Cognitive lensing framework with aspectual (Russian) and classifier (Mandarin) frames
- Aspektual'naya Ramka section for explicit deployment state tracking
  - Perfective/Imperfective/Blocked state markers (SV/NSV/ZABLOKIROVANO)
  - Deployment pipeline state tracking with transition rules
  - Example state tracking output templates
- Liangci Kuangjia section for deployment classification
  - Deployment type classifiers: FEATURE, HOTFIX, ROLLBACK, CONFIG, MIGRATION
  - Risk level classifiers: HIGH, MEDIUM, LOW with gate requirements
  - Environment progression classifiers: DEV, STAGING, PRODUCTION
  - Deployment strategy classifiers: BLUE-GREEN, CANARY, ROLLING, BIG-BANG
  - Classification decision matrix with YAML template
  - Complete deployment classification report template
- State transition rules for deployment lifecycle management
- Risk mitigation patterns integrated with state tracking

**Changed**:
- Version bumped from 1.0.0 to 1.1.0
- Added cognitive_frame metadata to YAML frontmatter

**Rationale**:
Deployment tracking requires explicit state management to avoid ambiguity about deployment readiness. The aspectual frame (borrowed from Russian grammar) provides perfective/imperfective markers that make state completion explicit - critical when deciding whether to proceed to production. The classifier frame (inspired by Mandarin measure words) enables systematic categorization by deployment type, risk level, and environment, ensuring appropriate validation gates and rollback strategies are applied. This cognitive lensing reduces deployment failures by forcing explicit state reasoning and systematic risk classification.

---

## Core Principles

Deployment Readiness operates on 3 fundamental principles:

### Principle 1: Production Performance Differs From Development
Models that run fast on development machines (1 GPU, synthetic data, no network latency) often fail performance SLAs in production (shared GPUs, real data volumes, network overhead). Benchmarking in production-like environments is non-negotiable.

In practice:
- Benchmark on production hardware (same GPU type, same instance size)
- Use production data volumes (1M records, not 1000)
- Simulate production network latency and concurrent requests

### Principle 2: Monitoring Precedes Deployment
Deploying without monitoring is deploying blind - you won't know when failures occur or what caused them. Monitoring infrastructure (metrics, logs, alerts) must be operational BEFORE first production request.

In practice:
- Prometheus + Grafana deployed and configured before model deployment
- Alerts tested by triggering synthetic failures (kill pod, inject latency)
- Dashboards validated with realistic load (not just healthy system metrics)

### Principle 3: Rollback Speed Determines Incident Impact
The difference between a 5-minute incident and a 4-hour incident is rollback readiness. Blue-green deployments enable instant traffic switching to previous version without debugging failed deployment.

In practice:
- Blue-green deployment: Both versions running, instant traffic switch
- Rollback tested in staging (verify <5 minute rollback time)
- Rollback decision criteria defined before deployment (error rate >5%, latency >200ms P95)

## Common Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **"Works On My Machine"** | Model runs fast on developer laptop (local GPU, no network calls, synthetic data). Production deployment has 10x higher latency due to shared GPUs and real data volumes. | Benchmark in production environment with production hardware, data volumes, and network conditions. Validate P95 latency <100ms with 100 QPS load. |
| **"We'll Add Monitoring Later"** | Deploy model without metrics/alerts. Production issue discovered by user complaints after 2 hours of degraded performance. | Deploy monitoring stack BEFORE model deployment. Test alerts by killing pods or injecting latency. Verify alerts fire within 2 minutes of synthetic failures. |
| **"Hotfix In Production"** | Deployment fails, team debugs in production. 4 hours later, issue identified but requires code changes. No way to revert to previous working version. | Document and TEST rollback procedure in staging. Blue-green deployment enables instant traffic switch to previous version. Rollback first, debug later. |

## Conclusion

Deployment Readiness provides systematic validation that ML models and systems are operationally ready for production deployment. The skill coordinates performance benchmarking, monitoring setup, incident response planning, and rollback testing across production-like environments.

Use this skill as Quality Gate 3 in the Deep Research SOP pipeline, or as the final validation before any production ML deployment. The 1-2 week investment in deployment readiness prevents weeks of incident response and emergency fixes - 90% of production ML failures stem from inadequate operational readiness, not model accuracy.

The framework enforces three critical validations: production performance benchmarks (not development machine performance), monitoring infrastructure operational before deployment (not added reactively after incidents), and tested rollback procedures (not improvised during outages). These validations are often skipped under deadline pressure, creating technical debt that manifests as extended production incidents.

Success requires treating deployment readiness as non-negotiable - partial passes are failures. The difference between reliable ML systems and incident-prone systems is operational discipline, not model sophistication. This skill ensures operational readiness meets the same rigorous standards as model accuracy.
