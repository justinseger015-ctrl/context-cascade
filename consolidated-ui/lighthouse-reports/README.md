# Lighthouse Reports Directory

This directory contains Lighthouse audit reports for performance, accessibility, best practices, and SEO analysis.

## Running Lighthouse Audits

### Via CLI (Local)

```bash
# Install Lighthouse globally
npm install -g lighthouse

# Run audit on specific page
lighthouse http://localhost:3000 --output html --output-path ./lighthouse-reports/home-$(date +%Y%m%d-%H%M%S).html

# Run with mobile emulation
lighthouse http://localhost:3000 --output html --output-path ./lighthouse-reports/home-mobile.html --emulated-form-factor=mobile

# Run with specific categories
lighthouse http://localhost:3000 --only-categories=performance,accessibility --output html --output-path ./lighthouse-reports/perf-a11y.html
```

### Via npm Script

Add to `package.json`:

```json
{
  "scripts": {
    "lighthouse": "lighthouse http://localhost:3000 --output html --output-path ./lighthouse-reports/report.html",
    "lighthouse:ci": "lhci autorun"
  }
}
```

### Via Playwright (Automated)

```typescript
import { test } from '@playwright/test';
import { playAudit } from 'playwright-lighthouse';

test('Lighthouse audit', async ({ page }) => {
  await page.goto('http://localhost:3000');

  await playAudit({
    page,
    thresholds: {
      performance: 90,
      accessibility: 100,
      'best-practices': 90,
      seo: 90,
    },
    reports: {
      formats: {
        html: true,
      },
      directory: './lighthouse-reports',
    },
  });
});
```

## Performance Thresholds

Target scores for production:

| Category | Threshold | Priority |
|----------|-----------|----------|
| Performance | ≥90 | Critical |
| Accessibility | 100 | Critical |
| Best Practices | ≥90 | High |
| SEO | ≥90 | High |

## Core Web Vitals Targets

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | ≤2.5s | 2.5-4.0s | >4.0s |
| FID (First Input Delay) | ≤100ms | 100-300ms | >300ms |
| CLS (Cumulative Layout Shift) | ≤0.1 | 0.1-0.25 | >0.25 |
| INP (Interaction to Next Paint) | ≤200ms | 200-500ms | >500ms |
| TTFB (Time to First Byte) | ≤600ms | 600-1800ms | >1800ms |
| FCP (First Contentful Paint) | ≤1.8s | 1.8-3.0s | >3.0s |

## Report Naming Convention

```
[page]-[device]-[timestamp].html

Examples:
- home-desktop-20251108-143022.html
- tasks-mobile-20251108-143045.html
- projects-desktop-20251108-143100.html
```

## Continuous Lighthouse CI

### Setup Lighthouse CI

```bash
npm install -g @lhci/cli

# Initialize
lhci wizard
```

### Configuration (lighthouserc.json)

```json
{
  "ci": {
    "collect": {
      "url": [
        "http://localhost:3000",
        "http://localhost:3000/tasks",
        "http://localhost:3000/projects"
      ],
      "numberOfRuns": 3,
      "settings": {
        "preset": "desktop"
      }
    },
    "assert": {
      "assertions": {
        "categories:performance": ["error", {"minScore": 0.9}],
        "categories:accessibility": ["error", {"minScore": 1.0}],
        "categories:best-practices": ["error", {"minScore": 0.9}],
        "categories:seo": ["error", {"minScore": 0.9}]
      }
    },
    "upload": {
      "target": "filesystem",
      "outputDir": "./lighthouse-reports"
    }
  }
}
```

### GitHub Actions Integration

```yaml
name: Lighthouse CI

on:
  pull_request:
    branches: [main]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Build app
        run: npm run build

      - name: Run Lighthouse CI
        run: |
          npm install -g @lhci/cli
          lhci autorun

      - name: Upload reports
        uses: actions/upload-artifact@v3
        with:
          name: lighthouse-reports
          path: ./lighthouse-reports
```

## Analyzing Reports

### Key Metrics to Monitor

1. **Performance**
   - First Contentful Paint (FCP)
   - Largest Contentful Paint (LCP)
   - Total Blocking Time (TBT)
   - Cumulative Layout Shift (CLS)
   - Speed Index

2. **Opportunities**
   - Eliminate render-blocking resources
   - Properly size images
   - Defer offscreen images
   - Minify JavaScript/CSS
   - Enable text compression

3. **Diagnostics**
   - Minimize main-thread work
   - Reduce JavaScript execution time
   - Avoid enormous network payloads
   - Use HTTP/2
   - Serve static assets with efficient cache policy

### Common Issues & Fixes

**Issue: Low Performance Score**
- ✅ Enable code splitting
- ✅ Lazy load images and components
- ✅ Compress images (WebP, lazy loading)
- ✅ Use CDN for static assets
- ✅ Enable HTTP/2 and compression (gzip/brotli)

**Issue: Low Accessibility Score**
- ✅ Add alt text to images
- ✅ Ensure proper color contrast (4.5:1 for text)
- ✅ Use semantic HTML (header, nav, main, footer)
- ✅ Add ARIA labels where needed
- ✅ Ensure keyboard navigation works

**Issue: Low Best Practices Score**
- ✅ Use HTTPS
- ✅ Fix console errors
- ✅ Use proper image aspect ratios (prevent CLS)
- ✅ Avoid deprecated APIs
- ✅ Ensure permissions policy is set

**Issue: Low SEO Score**
- ✅ Add meta description
- ✅ Ensure viewport meta tag exists
- ✅ Use descriptive link text
- ✅ Add canonical URLs
- ✅ Ensure robots.txt exists

## Trend Analysis

Track performance over time:

```bash
# Generate report with timestamp
DATE=$(date +%Y%m%d-%H%M%S)
lighthouse http://localhost:3000 \
  --output html \
  --output-path ./lighthouse-reports/trend-$DATE.html

# Compare reports
# Use tools like lighthouse-ci or custom scripts to compare scores
```

## Resources

- [Lighthouse Documentation](https://developer.chrome.com/docs/lighthouse/)
- [Web.dev Performance](https://web.dev/performance/)
- [Core Web Vitals](https://web.dev/vitals/)
- [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci)
- [playwright-lighthouse](https://github.com/abhinaba-ghosh/playwright-lighthouse)
