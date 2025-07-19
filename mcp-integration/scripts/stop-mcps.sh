#!/bin/bash

# MCP Stop Script
# Stops all running MCP servers

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_status "🛑 Stopping MCP servers..."

# Check if PID file exists
if [ ! -f "/tmp/mcp_pids.txt" ]; then
    print_warning "No PID file found. MCP servers may not be running."
    exit 0
fi

# Stop each process
stopped_count=0
while read -r pid; do
    if [ -n "$pid" ] && ps -p "$pid" > /dev/null 2>&1; then
        print_status "Stopping process $pid..."
        kill "$pid" 2>/dev/null || print_warning "Failed to stop process $pid"
        stopped_count=$((stopped_count + 1))
    fi
done < /tmp/mcp_pids.txt

# Clean up PID file
rm -f /tmp/mcp_pids.txt

print_status "✅ Stopped $stopped_count MCP server(s)"

# Optional: Kill any remaining MCP processes
if command -v pkill &> /dev/null; then
    print_status "Cleaning up any remaining MCP processes..."
    pkill -f "playwright.*mcp" 2>/dev/null || true
    pkill -f "knowledge-graph" 2>/dev/null || true
    pkill -f "memory-bank-mcp" 2>/dev/null || true
    pkill -f "perplexity-ask-mcp" 2>/dev/null || true
fi

print_status "🏁 All MCP servers stopped"