# CI/CD Pipeline Documentation

This document describes the Continuous Integration and Continuous Deployment (CI/CD) pipelines for the RUV SPARC UI Dashboard using GitHub Actions.

## Table of Contents

- [Overview](#overview)
- [Pipeline Architecture](#pipeline-architecture)
- [GitHub Actions Workflows](#github-actions-workflows)
- [Environment Variables and Secrets](#environment-variables-and-secrets)
- [Deployment Strategies](#deployment-strategies)
- [Monitoring and Alerts](#monitoring-and-alerts)
- [Troubleshooting](#troubleshooting)

---

## Overview

The RUV SPARC UI Dashboard uses **GitHub Actions** for automated testing, building, and deployment. The CI/CD pipeline ensures code quality, security, and reliable deployments.

### Key Features

- ✅ **Automated Testing**: Unit, integration, and E2E tests on every PR
- ✅ **Code Quality**: Linting, type checking, and code coverage enforcement
- ✅ **Security Scanning**: Dependency vulnerability checks and SAST
- ✅ **Docker Builds**: Multi-stage builds for frontend and backend
- ✅ **Automated Deployments**: Staging and production deployment automation
- ✅ **Rollback Support**: Automated rollback on deployment failures

---

## Pipeline Architecture

### CI/CD Flow Diagram

```mermaid
graph TB
    subgraph "Developer Workflow"
        Dev[Developer] -->|Push Code| GitHub[GitHub Repository]
        Dev -->|Create PR| GitHub
    end

    subgraph "CI Pipeline (Pull Request)"
        GitHub -->|Trigger| Lint[Lint & Type Check]
        Lint -->|Pass| Test[Unit Tests]
        Test -->|Pass| Coverage[Coverage Check ≥90%]
        Coverage -->|Pass| E2E[E2E Tests]
        E2E -->|Pass| Security[Security Scan]
        Security -->|Pass| Build[Docker Build]
        Build -->|Pass| Approve[PR Approved ✅]
    end

    subgraph "CD Pipeline (Main Branch)"
        Approve -->|Merge to main| Deploy_Staging[Deploy to Staging]
        Deploy_Staging -->|Health Check| Smoke_Tests[Smoke Tests]
        Smoke_Tests -->|Pass| Manual_Approval[Manual Approval]
        Manual_Approval -->|Approved| Deploy_Prod[Deploy to Production]
        Deploy_Prod -->|Health Check| Monitor[Monitor Metrics]
        Monitor -->|Failure| Rollback[Auto Rollback]
    end

    style Dev fill:#e1f5ff
    style Lint fill:#fff9c4
    style Test fill:#c8e6c9
    style Deploy_Prod fill:#81c784
    style Rollback fill:#ff8a65
```

---

## GitHub Actions Workflows

All workflows are located in `.github/workflows/` directory.

### 1. Lint and Type Check (`lint.yml`)

**Trigger**: Pull request, push to `main`

```yaml
name: Lint and Type Check

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  frontend-lint:
    name: Frontend Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        working-directory: ./frontend
        run: npm ci

      - name: Run ESLint
        working-directory: ./frontend
        run: npm run lint

      - name: Check Prettier formatting
        working-directory: ./frontend
        run: npm run format:check

      - name: Type check
        working-directory: ./frontend
        run: npm run typecheck

  backend-lint:
    name: Backend Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
          cache-dependency-path: backend/requirements.txt

      - name: Install dependencies
        working-directory: ./backend
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install black ruff

      - name: Run Black formatter check
        working-directory: ./backend
        run: black --check app/

      - name: Run Ruff linter
        working-directory: ./backend
        run: ruff check app/
```

### 2. Test Suite (`test.yml`)

**Trigger**: Pull request, push to `main`

```yaml
name: Test Suite

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  frontend-tests:
    name: Frontend Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        working-directory: ./frontend
        run: npm ci

      - name: Run unit tests
        working-directory: ./frontend
        run: npm run test:coverage

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          files: ./frontend/coverage/lcov.info
          flags: frontend
          name: frontend-coverage

      - name: Check coverage threshold
        working-directory: ./frontend
        run: |
          COVERAGE=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
          if (( $(echo "$COVERAGE < 90" | bc -l) )); then
            echo "Coverage $COVERAGE% is below 90% threshold"
            exit 1
          fi

  backend-tests:
    name: Backend Tests
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
          cache-dependency-path: backend/requirements.txt

      - name: Install dependencies
        working-directory: ./backend
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov httpx

      - name: Run tests with coverage
        working-directory: ./backend
        env:
          DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379
          SECRET_KEY: test-secret-key-for-ci
          ENVIRONMENT: test
        run: pytest --cov=app --cov-report=xml --cov-report=term --cov-fail-under=90

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          files: ./backend/coverage.xml
          flags: backend
          name: backend-coverage

  e2e-tests:
    name: E2E Tests (Playwright)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        working-directory: ./frontend
        run: npm ci

      - name: Install Playwright browsers
        working-directory: ./frontend
        run: npx playwright install --with-deps chromium

      - name: Start services with Docker Compose
        run: docker compose -f docker-compose.test.yml up -d

      - name: Wait for services to be healthy
        run: |
          timeout 60 bash -c 'until curl -f http://localhost:8000/api/v1/health; do sleep 2; done'

      - name: Run E2E tests
        working-directory: ./frontend
        run: npm run test:e2e:chromium

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: frontend/playwright-report/
          retention-days: 7

      - name: Tear down services
        if: always()
        run: docker compose -f docker-compose.test.yml down
```

### 3. Security Scanning (`security.yml`)

**Trigger**: Pull request, push to `main`, weekly schedule

```yaml
name: Security Scanning

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday

jobs:
  dependency-check:
    name: Dependency Vulnerability Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run npm audit (Frontend)
        working-directory: ./frontend
        run: npm audit --audit-level=moderate

      - name: Run pip-audit (Backend)
        working-directory: ./backend
        run: |
          pip install pip-audit
          pip-audit -r requirements.txt

  trivy-scan:
    name: Trivy Container Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build Docker images
        run: docker compose build

      - name: Run Trivy scan on backend image
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ruv-sparc-backend:latest
          format: 'sarif'
          output: 'trivy-backend-results.sarif'
          severity: 'CRITICAL,HIGH'

      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-backend-results.sarif'

  codeql:
    name: CodeQL SAST Analysis
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - uses: actions/checkout@v4

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: 'python, javascript'

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3
```

### 4. Build and Push (`build.yml`)

**Trigger**: Push to `main`, tag creation

```yaml
name: Build and Push Docker Images

on:
  push:
    branches: [main]
    tags:
      - 'v*'

jobs:
  build-push:
    name: Build and Push Images
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta-backend
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}/backend
          tags: |
            type=ref,event=branch
            type=ref,event=tag
            type=sha,prefix={{branch}}-

      - name: Build and push backend image
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          push: true
          tags: ${{ steps.meta-backend.outputs.tags }}
          labels: ${{ steps.meta-backend.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Extract metadata (frontend)
        id: meta-frontend
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}/frontend
          tags: |
            type=ref,event=branch
            type=ref,event=tag
            type=sha,prefix={{branch}}-

      - name: Build and push frontend image
        uses: docker/build-push-action@v5
        with:
          context: ./frontend
          push: true
          tags: ${{ steps.meta-frontend.outputs.tags }}
          labels: ${{ steps.meta-frontend.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### 5. Deploy to Staging (`deploy-staging.yml`)

**Trigger**: Push to `main`

```yaml
name: Deploy to Staging

on:
  push:
    branches: [main]

jobs:
  deploy:
    name: Deploy to Staging Environment
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.ruv-sparc.io
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy to ECS
        run: |
          # Update ECS task definition with new image
          aws ecs update-service \
            --cluster ruv-sparc-staging \
            --service ruv-sparc-backend \
            --force-new-deployment

          aws ecs update-service \
            --cluster ruv-sparc-staging \
            --service ruv-sparc-frontend \
            --force-new-deployment

      - name: Wait for deployment
        run: |
          aws ecs wait services-stable \
            --cluster ruv-sparc-staging \
            --services ruv-sparc-backend ruv-sparc-frontend

      - name: Health check
        run: |
          curl -f https://staging.ruv-sparc.io/api/v1/health || exit 1

      - name: Run smoke tests
        run: |
          npm ci
          npm run test:smoke -- --base-url https://staging.ruv-sparc.io
```

### 6. Deploy to Production (`deploy-production.yml`)

**Trigger**: Manual approval after staging deployment

```yaml
name: Deploy to Production

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to deploy (e.g., v1.2.3)'
        required: true

jobs:
  deploy:
    name: Deploy to Production Environment
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://ruv-sparc.io
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.inputs.version }}

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Blue-Green Deployment
        run: |
          # Deploy to green environment
          aws ecs update-service \
            --cluster ruv-sparc-production \
            --service ruv-sparc-backend-green \
            --force-new-deployment

          # Wait for green to be healthy
          aws ecs wait services-stable \
            --cluster ruv-sparc-production \
            --services ruv-sparc-backend-green

          # Switch traffic to green
          aws elbv2 modify-listener \
            --listener-arn ${{ secrets.ALB_LISTENER_ARN }} \
            --default-actions \
              Type=forward,TargetGroupArn=${{ secrets.GREEN_TARGET_GROUP_ARN }}

      - name: Health check
        run: |
          for i in {1..10}; do
            if curl -f https://ruv-sparc.io/api/v1/health; then
              exit 0
            fi
            sleep 10
          done
          exit 1

      - name: Rollback on failure
        if: failure()
        run: |
          # Switch traffic back to blue
          aws elbv2 modify-listener \
            --listener-arn ${{ secrets.ALB_LISTENER_ARN }} \
            --default-actions \
              Type=forward,TargetGroupArn=${{ secrets.BLUE_TARGET_GROUP_ARN }}

          echo "Deployment failed, rolled back to previous version"
          exit 1

      - name: Notify deployment success
        if: success()
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK }}
          payload: |
            {
              "text": "✅ Production deployment successful: ${{ github.event.inputs.version }}"
            }
```

---

## Environment Variables and Secrets

### Required GitHub Secrets

Configure these secrets in **Settings → Secrets and variables → Actions**:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `AWS_ACCESS_KEY_ID` | AWS access key for deployment | `AKIAIOSFODNN7EXAMPLE` |
| `AWS_SECRET_ACCESS_KEY` | AWS secret access key | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
| `DOCKER_USERNAME` | Docker Hub username | `ruvnet` |
| `DOCKER_PASSWORD` | Docker Hub password/token | `dckr_pat_...` |
| `SLACK_WEBHOOK` | Slack webhook for notifications | `https://hooks.slack.com/...` |
| `ALB_LISTENER_ARN` | AWS ALB listener ARN | `arn:aws:elasticloadbalancing:...` |
| `BLUE_TARGET_GROUP_ARN` | Blue target group ARN | `arn:aws:elasticloadbalancing:...` |
| `GREEN_TARGET_GROUP_ARN` | Green target group ARN | `arn:aws:elasticloadbalancing:...` |

### Environment-Specific Variables

#### Staging Environment

| Variable | Value |
|----------|-------|
| `DATABASE_URL` | `postgresql://...` (staging database) |
| `REDIS_URL` | `redis://...` (staging Redis) |
| `CORS_ORIGINS` | `["https://staging.ruv-sparc.io"]` |
| `ENVIRONMENT` | `staging` |

#### Production Environment

| Variable | Value |
|----------|-------|
| `DATABASE_URL` | `postgresql://...` (production database) |
| `REDIS_URL` | `redis://...` (production Redis) |
| `CORS_ORIGINS` | `["https://ruv-sparc.io"]` |
| `ENVIRONMENT` | `production` |

---

## Deployment Strategies

### 1. Blue-Green Deployment

```mermaid
graph LR
    subgraph "Current State (Blue Active)"
        ALB1[Application Load Balancer]
        Blue[Blue Environment v1.0]
        Green1[Green Environment Idle]
    end

    subgraph "Deploy New Version"
        ALB2[Application Load Balancer]
        Blue2[Blue Environment v1.0]
        Green2[Green Environment v1.1 Deploying]
    end

    subgraph "Switch Traffic"
        ALB3[Application Load Balancer]
        Blue3[Blue Environment v1.0 Idle]
        Green3[Green Environment v1.1 Active]
    end

    ALB1 -->|100% Traffic| Blue
    ALB2 -->|100% Traffic| Blue2
    ALB2 -.->|Deploy| Green2
    ALB3 -->|100% Traffic| Green3
```

**Benefits**:
- Zero downtime deployments
- Instant rollback capability
- Safe production testing

### 2. Canary Deployment (Advanced)

```mermaid
graph LR
    subgraph "Phase 1: 10% Traffic"
        ALB1[Load Balancer]
        V1_90[v1.0: 90%]
        V2_10[v1.1: 10%]
    end

    subgraph "Phase 2: 50% Traffic"
        ALB2[Load Balancer]
        V1_50[v1.0: 50%]
        V2_50[v1.1: 50%]
    end

    subgraph "Phase 3: 100% Traffic"
        ALB3[Load Balancer]
        V2_100[v1.1: 100%]
    end

    ALB1 --> V1_90
    ALB1 --> V2_10
    ALB2 --> V1_50
    ALB2 --> V2_50
    ALB3 --> V2_100
```

### 3. Rolling Update

Progressive update of instances one by one:

1. Update instance 1 → Health check
2. Update instance 2 → Health check
3. Update instance 3 → Health check
4. Continue until all instances updated

---

## Monitoring and Alerts

### Health Checks

```bash
# Backend health check
curl https://ruv-sparc.io/api/v1/health

# Expected response:
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected",
  "memory_mcp": "operational",
  "websocket": "active",
  "version": "1.0.0"
}
```

### Deployment Metrics

Track these metrics during deployment:

| Metric | Threshold | Alert Condition |
|--------|-----------|-----------------|
| Response Time (p95) | < 500ms | > 1000ms for 5 minutes |
| Error Rate | < 1% | > 5% for 2 minutes |
| CPU Usage | < 70% | > 90% for 5 minutes |
| Memory Usage | < 80% | > 95% for 5 minutes |
| Database Connections | < 80% of pool | > 90% for 2 minutes |

### Slack Notifications

```yaml
- name: Notify on deployment
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {
        "text": "🚀 Deployment started: ${{ github.event.inputs.version }}",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Deployment Status*\n• Environment: Production\n• Version: ${{ github.event.inputs.version }}\n• Author: ${{ github.actor }}"
            }
          }
        ]
      }
```

---

## Troubleshooting

### Common Issues

#### Issue 1: Test Failures in CI

**Symptoms**: Tests pass locally but fail in CI

**Debugging**:
```bash
# Run tests in Docker to match CI environment
docker run -it --rm \
  -v $(pwd):/app \
  -w /app/backend \
  python:3.11 \
  bash -c "pip install -r requirements.txt && pytest"
```

**Solutions**:
- Check for environment-specific issues (timezone, locale)
- Verify test database is properly initialized
- Review GitHub Actions logs for detailed error messages

#### Issue 2: Docker Build Timeout

**Symptoms**: `Error: buildx failed with: context deadline exceeded`

**Solutions**:
```yaml
# Increase timeout in workflow
- name: Build and push
  uses: docker/build-push-action@v5
  with:
    context: ./backend
    timeout: 20m  # Increase timeout
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

#### Issue 3: Deployment Rollback

**Manual rollback**:
```bash
# AWS ECS rollback to previous task definition
aws ecs update-service \
  --cluster ruv-sparc-production \
  --service ruv-sparc-backend \
  --task-definition ruv-sparc-backend:42  # Previous revision

# Kubernetes rollback (if using K8s)
kubectl rollout undo deployment/ruv-sparc-backend
```

---

## Best Practices

1. **Always test in staging** before production deployment
2. **Use environment protection rules** for production
3. **Enable required status checks** on main branch
4. **Tag releases** with semantic versioning (v1.2.3)
5. **Monitor deployments** for at least 30 minutes post-deploy
6. **Keep secrets secure** - never commit to repository
7. **Use Docker layer caching** to speed up builds
8. **Implement gradual rollouts** for high-risk changes

---

## Next Steps

- Set up **AWS CloudWatch** for centralized logging
- Implement **Prometheus + Grafana** for metrics visualization
- Configure **PagerDuty** for on-call alerts
- Add **Sentry** for error tracking
- Enable **Datadog APM** for distributed tracing

---

**Last Updated**: 2025-11-08
**Version**: 1.0.0
