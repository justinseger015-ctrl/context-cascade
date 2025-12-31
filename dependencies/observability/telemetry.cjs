/**
 * MCP Observability & Telemetry
 * Phase 6.3 Observability Stack
 *
 * OpenTelemetry-compatible tracing and metrics for MCP operations.
 * Inspired by IBM MCP Context Forge observability features.
 *
 * @module dependencies/observability/telemetry
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// Log directory
const LOG_DIR = path.join(__dirname, '..', '..', 'logs');

/**
 * Telemetry configuration
 */
const TELEMETRY_CONFIG = {
  enabled: true,
  logLevel: 'info',
  traceEnabled: true,
  metricsEnabled: true,
  logFormat: 'json',
  maxLogSize: 10 * 1024 * 1024, // 10MB
  maxLogFiles: 5,
  flushInterval: 5000
};

/**
 * Log levels
 */
const LogLevel = {
  DEBUG: 0,
  INFO: 1,
  WARN: 2,
  ERROR: 3,
  FATAL: 4
};

/**
 * Span status
 */
const SpanStatus = {
  UNSET: 'UNSET',
  OK: 'OK',
  ERROR: 'ERROR'
};

/**
 * Generate trace ID (OpenTelemetry compatible)
 * @returns {string} 32-char hex trace ID
 */
function generateTraceId() {
  return crypto.randomBytes(16).toString('hex');
}

/**
 * Generate span ID (OpenTelemetry compatible)
 * @returns {string} 16-char hex span ID
 */
function generateSpanId() {
  return crypto.randomBytes(8).toString('hex');
}

/**
 * Span class for distributed tracing
 */
class Span {
  constructor(name, options = {}) {
    this.name = name;
    this.traceId = options.traceId || generateTraceId();
    this.spanId = generateSpanId();
    this.parentSpanId = options.parentSpanId || null;
    this.startTime = Date.now();
    this.endTime = null;
    this.status = SpanStatus.UNSET;
    this.attributes = options.attributes || {};
    this.events = [];
    this.links = [];
  }

  /**
   * Set span attribute
   * @param {string} key - Attribute key
   * @param {*} value - Attribute value
   */
  setAttribute(key, value) {
    this.attributes[key] = value;
    return this;
  }

  /**
   * Set multiple attributes
   * @param {Object} attrs - Attributes object
   */
  setAttributes(attrs) {
    Object.assign(this.attributes, attrs);
    return this;
  }

  /**
   * Add event to span
   * @param {string} name - Event name
   * @param {Object} attributes - Event attributes
   */
  addEvent(name, attributes = {}) {
    this.events.push({
      name,
      timestamp: Date.now(),
      attributes
    });
    return this;
  }

  /**
   * Set span status
   * @param {string} status - Status code
   * @param {string} message - Optional message
   */
  setStatus(status, message = null) {
    this.status = status;
    if (message) {
      this.statusMessage = message;
    }
    return this;
  }

  /**
   * End the span
   */
  end() {
    this.endTime = Date.now();
    this.duration = this.endTime - this.startTime;
    return this;
  }

  /**
   * Convert to JSON for export
   * @returns {Object} JSON representation
   */
  toJSON() {
    return {
      traceId: this.traceId,
      spanId: this.spanId,
      parentSpanId: this.parentSpanId,
      name: this.name,
      startTime: this.startTime,
      endTime: this.endTime,
      duration: this.duration,
      status: this.status,
      statusMessage: this.statusMessage,
      attributes: this.attributes,
      events: this.events
    };
  }
}

/**
 * Tracer class for creating and managing spans
 */
class Tracer {
  constructor(serviceName, config = {}) {
    this.serviceName = serviceName;
    this.config = { ...TELEMETRY_CONFIG, ...config };
    this.activeSpans = new Map();
    this.completedSpans = [];
    this.exporters = [];
  }

  /**
   * Start a new span
   * @param {string} name - Span name
   * @param {Object} options - Span options
   * @returns {Span} New span
   */
  startSpan(name, options = {}) {
    const span = new Span(name, options);
    span.setAttribute('service.name', this.serviceName);
    this.activeSpans.set(span.spanId, span);
    return span;
  }

  /**
   * End a span and export it
   * @param {Span} span - Span to end
   */
  endSpan(span) {
    span.end();
    this.activeSpans.delete(span.spanId);
    this.completedSpans.push(span);

    // Export to all exporters
    for (const exporter of this.exporters) {
      exporter.export(span);
    }

    return span;
  }

  /**
   * Create child span
   * @param {Span} parent - Parent span
   * @param {string} name - Child span name
   * @returns {Span} Child span
   */
  startChildSpan(parent, name) {
    return this.startSpan(name, {
      traceId: parent.traceId,
      parentSpanId: parent.spanId
    });
  }

  /**
   * Add exporter
   * @param {Object} exporter - Exporter instance
   */
  addExporter(exporter) {
    this.exporters.push(exporter);
  }

  /**
   * Get all completed spans
   * @returns {Span[]} Completed spans
   */
  getCompletedSpans() {
    return this.completedSpans;
  }

  /**
   * Clear completed spans
   */
  clearSpans() {
    this.completedSpans = [];
  }
}

/**
 * Metrics collector
 */
class MetricsCollector {
  constructor(serviceName) {
    this.serviceName = serviceName;
    this.counters = new Map();
    this.gauges = new Map();
    this.histograms = new Map();
  }

  /**
   * Increment counter
   * @param {string} name - Counter name
   * @param {number} value - Increment value
   * @param {Object} labels - Labels
   */
  incrementCounter(name, value = 1, labels = {}) {
    const key = this.makeKey(name, labels);
    const current = this.counters.get(key) || { name, labels, value: 0 };
    current.value += value;
    current.lastUpdated = Date.now();
    this.counters.set(key, current);
  }

  /**
   * Set gauge value
   * @param {string} name - Gauge name
   * @param {number} value - Gauge value
   * @param {Object} labels - Labels
   */
  setGauge(name, value, labels = {}) {
    const key = this.makeKey(name, labels);
    this.gauges.set(key, {
      name,
      labels,
      value,
      lastUpdated: Date.now()
    });
  }

  /**
   * Record histogram value
   * @param {string} name - Histogram name
   * @param {number} value - Value to record
   * @param {Object} labels - Labels
   */
  recordHistogram(name, value, labels = {}) {
    const key = this.makeKey(name, labels);
    const histogram = this.histograms.get(key) || {
      name,
      labels,
      values: [],
      count: 0,
      sum: 0,
      min: Infinity,
      max: -Infinity
    };

    histogram.values.push(value);
    histogram.count++;
    histogram.sum += value;
    histogram.min = Math.min(histogram.min, value);
    histogram.max = Math.max(histogram.max, value);
    histogram.lastUpdated = Date.now();

    this.histograms.set(key, histogram);
  }

  /**
   * Generate metrics key
   */
  makeKey(name, labels) {
    const labelStr = Object.entries(labels).sort().map(([k, v]) => `${k}=${v}`).join(',');
    return `${name}{${labelStr}}`;
  }

  /**
   * Get all metrics
   * @returns {Object} All metrics
   */
  getMetrics() {
    return {
      counters: Object.fromEntries(this.counters),
      gauges: Object.fromEntries(this.gauges),
      histograms: Object.fromEntries(this.histograms)
    };
  }

  /**
   * Export metrics in Prometheus format
   * @returns {string} Prometheus format
   */
  toPrometheus() {
    let output = '';

    // Counters
    for (const [, counter] of this.counters) {
      const labels = this.formatLabels(counter.labels);
      output += `# TYPE ${counter.name} counter\n`;
      output += `${counter.name}${labels} ${counter.value}\n`;
    }

    // Gauges
    for (const [, gauge] of this.gauges) {
      const labels = this.formatLabels(gauge.labels);
      output += `# TYPE ${gauge.name} gauge\n`;
      output += `${gauge.name}${labels} ${gauge.value}\n`;
    }

    // Histograms
    for (const [, hist] of this.histograms) {
      const labels = this.formatLabels(hist.labels);
      output += `# TYPE ${hist.name} histogram\n`;
      output += `${hist.name}_count${labels} ${hist.count}\n`;
      output += `${hist.name}_sum${labels} ${hist.sum}\n`;
    }

    return output;
  }

  formatLabels(labels) {
    if (Object.keys(labels).length === 0) return '';
    const pairs = Object.entries(labels).map(([k, v]) => `${k}="${v}"`);
    return `{${pairs.join(',')}}`;
  }
}

/**
 * Structured logger
 */
class StructuredLogger {
  constructor(serviceName, config = {}) {
    this.serviceName = serviceName;
    this.config = { ...TELEMETRY_CONFIG, ...config };
    this.logFile = null;
    this.buffer = [];
    this.flushTimer = null;

    // Ensure log directory exists
    if (!fs.existsSync(LOG_DIR)) {
      fs.mkdirSync(LOG_DIR, { recursive: true });
    }

    // Start flush timer
    this.startFlushTimer();
  }

  /**
   * Log message
   * @param {string} level - Log level
   * @param {string} message - Log message
   * @param {Object} context - Additional context
   */
  log(level, message, context = {}) {
    const levelNum = LogLevel[level.toUpperCase()] || LogLevel.INFO;
    const configLevel = LogLevel[this.config.logLevel.toUpperCase()] || LogLevel.INFO;

    if (levelNum < configLevel) return;

    const entry = {
      timestamp: new Date().toISOString(),
      level: level.toUpperCase(),
      service: this.serviceName,
      message,
      ...context
    };

    // Add trace context if present
    if (context.traceId) {
      entry.trace_id = context.traceId;
    }
    if (context.spanId) {
      entry.span_id = context.spanId;
    }

    this.buffer.push(entry);

    // Console output
    if (this.config.logFormat === 'json') {
      console.log(JSON.stringify(entry));
    } else {
      console.log(`[${entry.timestamp}] ${entry.level} ${entry.message}`);
    }
  }

  debug(message, context = {}) { this.log('debug', message, context); }
  info(message, context = {}) { this.log('info', message, context); }
  warn(message, context = {}) { this.log('warn', message, context); }
  error(message, context = {}) { this.log('error', message, context); }
  fatal(message, context = {}) { this.log('fatal', message, context); }

  /**
   * Start flush timer
   */
  startFlushTimer() {
    this.flushTimer = setInterval(() => {
      this.flush();
    }, this.config.flushInterval);
  }

  /**
   * Stop flush timer
   */
  stopFlushTimer() {
    if (this.flushTimer) {
      clearInterval(this.flushTimer);
      this.flushTimer = null;
    }
  }

  /**
   * Flush buffer to file
   */
  flush() {
    if (this.buffer.length === 0) return;

    const logPath = path.join(LOG_DIR, `${this.serviceName}.log`);

    try {
      const content = this.buffer.map(e => JSON.stringify(e)).join('\n') + '\n';
      fs.appendFileSync(logPath, content);
      this.buffer = [];

      // Rotate if needed
      this.rotateIfNeeded(logPath);
    } catch (err) {
      console.error(`[Logger] Flush failed: ${err.message}`);
    }
  }

  /**
   * Rotate log file if too large
   */
  rotateIfNeeded(logPath) {
    try {
      const stats = fs.statSync(logPath);
      if (stats.size > this.config.maxLogSize) {
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const rotatedPath = logPath.replace('.log', `-${timestamp}.log`);
        fs.renameSync(logPath, rotatedPath);

        // Clean old logs
        this.cleanOldLogs();
      }
    } catch (err) {
      // File doesn't exist or other error
    }
  }

  /**
   * Clean old log files
   */
  cleanOldLogs() {
    try {
      const files = fs.readdirSync(LOG_DIR)
        .filter(f => f.startsWith(this.serviceName) && f.endsWith('.log'))
        .sort()
        .reverse();

      for (let i = this.config.maxLogFiles; i < files.length; i++) {
        fs.unlinkSync(path.join(LOG_DIR, files[i]));
      }
    } catch (err) {
      // Ignore cleanup errors
    }
  }

  /**
   * Shutdown logger
   */
  shutdown() {
    this.stopFlushTimer();
    this.flush();
  }
}

/**
 * Console exporter for spans
 */
class ConsoleSpanExporter {
  export(span) {
    console.log(JSON.stringify({
      type: 'span',
      ...span.toJSON()
    }));
  }
}

/**
 * File exporter for spans
 */
class FileSpanExporter {
  constructor(filePath) {
    this.filePath = filePath || path.join(LOG_DIR, 'traces.jsonl');
  }

  export(span) {
    try {
      const content = JSON.stringify(span.toJSON()) + '\n';
      fs.appendFileSync(this.filePath, content);
    } catch (err) {
      console.error(`[Exporter] Export failed: ${err.message}`);
    }
  }
}

/**
 * Create telemetry instance
 * @param {string} serviceName - Service name
 * @param {Object} config - Configuration
 * @returns {Object} Telemetry instance
 */
function createTelemetry(serviceName, config = {}) {
  const tracer = new Tracer(serviceName, config);
  const metrics = new MetricsCollector(serviceName);
  const logger = new StructuredLogger(serviceName, config);

  // Add default exporters
  tracer.addExporter(new FileSpanExporter());

  return {
    tracer,
    metrics,
    logger,

    // Convenience methods
    startSpan: (name, options) => tracer.startSpan(name, options),
    endSpan: (span) => tracer.endSpan(span),
    increment: (name, value, labels) => metrics.incrementCounter(name, value, labels),
    gauge: (name, value, labels) => metrics.setGauge(name, value, labels),
    histogram: (name, value, labels) => metrics.recordHistogram(name, value, labels),
    log: (level, message, context) => logger.log(level, message, context),

    shutdown: () => {
      logger.shutdown();
    }
  };
}

// Export
module.exports = {
  Span,
  SpanStatus,
  Tracer,
  MetricsCollector,
  StructuredLogger,
  ConsoleSpanExporter,
  FileSpanExporter,
  LogLevel,
  TELEMETRY_CONFIG,
  generateTraceId,
  generateSpanId,
  createTelemetry
};
