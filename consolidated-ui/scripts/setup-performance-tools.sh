#!/bin/bash
#
# Performance Testing Tools Setup Script
# Installs k6, Lighthouse, and other performance testing dependencies
#

set -e

echo "======================================"
echo "Performance Testing Tools Setup"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
  echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
  echo -e "${RED}❌ $1${NC}"
}

print_info() {
  echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Check for Node.js
if ! command -v node &> /dev/null; then
  print_error "Node.js is not installed"
  print_info "Install Node.js from: https://nodejs.org/"
  exit 1
fi

print_success "Node.js found: $(node --version)"

# Check for npm
if ! command -v npm &> /dev/null; then
  print_error "npm is not installed"
  exit 1
fi

print_success "npm found: $(npm --version)"

# Install k6 (load testing)
echo ""
echo "1️⃣  Installing k6 (load testing tool)..."

if command -v k6 &> /dev/null; then
  print_info "k6 already installed: $(k6 version)"
else
  # Detect OS and install k6
  if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    sudo gpg -k
    sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg \
      --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
    echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | \
      sudo tee /etc/apt/sources.list.d/k6.list
    sudo apt-get update
    sudo apt-get install k6
    print_success "k6 installed (Linux)"

  elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if command -v brew &> /dev/null; then
      brew install k6
      print_success "k6 installed (macOS via Homebrew)"
    else
      print_error "Homebrew not found. Install Homebrew first: https://brew.sh/"
      exit 1
    fi

  elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows (Git Bash / MSYS / Cygwin)
    if command -v choco &> /dev/null; then
      choco install k6
      print_success "k6 installed (Windows via Chocolatey)"
    else
      print_error "Chocolatey not found. Install Chocolatey first: https://chocolatey.org/"
      print_info "Or download k6 manually from: https://k6.io/docs/get-started/installation/"
      exit 1
    fi

  else
    print_error "Unsupported OS: $OSTYPE"
    print_info "Install k6 manually from: https://k6.io/docs/get-started/installation/"
    exit 1
  fi
fi

# Install Lighthouse (globally)
echo ""
echo "2️⃣  Installing Lighthouse (performance auditing)..."

if npm list -g lighthouse &> /dev/null; then
  print_info "Lighthouse already installed: $(lighthouse --version)"
else
  npm install -g lighthouse
  print_success "Lighthouse installed globally"
fi

# Install Lighthouse CI
echo ""
echo "3️⃣  Installing Lighthouse CI..."

if npm list -g @lhci/cli &> /dev/null; then
  print_info "Lighthouse CI already installed"
else
  npm install -g @lhci/cli
  print_success "Lighthouse CI installed globally"
fi

# Install frontend dependencies (React Profiler, react-window)
echo ""
echo "4️⃣  Installing frontend performance dependencies..."

cd frontend || exit 1

if [ ! -d "node_modules" ]; then
  print_info "Installing npm dependencies..."
  npm install
fi

# Check if react-window is installed
if ! npm list react-window &> /dev/null; then
  npm install react-window @types/react-window
  print_success "react-window installed"
else
  print_info "react-window already installed"
fi

cd ..

# Install Python dependencies (for backend)
echo ""
echo "5️⃣  Installing backend performance dependencies..."

cd backend || exit 1

if [ ! -d "venv" ]; then
  print_info "Creating Python virtual environment..."
  python3 -m venv venv
fi

source venv/bin/activate || source venv/Scripts/activate

# Install performance-related packages
pip install -q redis aioredis asyncpg

print_success "Backend dependencies installed"

deactivate
cd ..

# Create benchmark results directories
echo ""
echo "6️⃣  Creating directories for benchmark results..."

mkdir -p k6-load-test-scripts/benchmark-results
mkdir -p lighthouse-reports
mkdir -p frontend/lighthouse-reports

print_success "Directories created"

# Make k6 scripts executable
echo ""
echo "7️⃣  Making k6 scripts executable..."

chmod +x k6-load-test-scripts/run-benchmarks.sh

print_success "Scripts are executable"

# Verify installations
echo ""
echo "======================================"
echo "Verification"
echo "======================================"

# Verify k6
if command -v k6 &> /dev/null; then
  print_success "k6: $(k6 version | head -n 1)"
else
  print_error "k6 not found in PATH"
fi

# Verify Lighthouse
if command -v lighthouse &> /dev/null; then
  print_success "Lighthouse: $(lighthouse --version)"
else
  print_error "Lighthouse not found in PATH"
fi

# Verify Lighthouse CI
if command -v lhci &> /dev/null; then
  print_success "Lighthouse CI: installed"
else
  print_error "Lighthouse CI not found in PATH"
fi

# Summary
echo ""
echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "  1. Start the backend: cd backend && python -m uvicorn app.main:app --reload"
echo "  2. Start the frontend: cd frontend && npm run dev"
echo "  3. Run k6 benchmarks: cd k6-load-test-scripts && ./run-benchmarks.sh"
echo "  4. Run Lighthouse audit: npm run lighthouse"
echo ""
echo "Documentation:"
echo "  - Performance benchmarks: docs/performance-benchmarks.md"
echo "  - Optimization changelog: docs/optimization-changelog.md"
echo "  - Lighthouse reports: lighthouse-reports/README.md"
echo ""
print_success "All performance testing tools installed successfully!"
