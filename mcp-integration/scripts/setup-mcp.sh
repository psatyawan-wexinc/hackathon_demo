#!/bin/bash

# MCP Setup Script
# Installs and configures MCP servers for the project

set -e

echo "🚀 Setting up MCP servers..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 18 or newer."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    print_error "Node.js version 18 or newer is required. Current version: $(node --version)"
    exit 1
fi

print_status "Node.js version check passed: $(node --version)"

# Check if npm is available
if ! command -v npm &> /dev/null; then
    print_error "npm is not installed"
    exit 1
fi

# Create directories if they don't exist
mkdir -p ../config/credentials

# Install MCP servers
print_status "Installing Playwright MCP..."
npm install -g @playwright/mcp

print_status "Installing Playwright browsers..."
npx playwright install

print_status "Installing Knowledge Graph MCP..."
npm install -g mcp-knowledge-graph

print_status "Installing Memory Bank MCP..."
npm install -g @movibe/memory-bank-mcp

print_status "Installing Perplexity MCP..."
npm install -g server-perplexity-ask

# Create environment file if it doesn't exist
if [ ! -f "../config/.env" ]; then
    print_warning "Creating .env file from template..."
    cp ../config/.env.example ../config/.env
    print_warning "Please edit ../config/.env with your actual credentials"
fi

# Create memory storage files
mkdir -p ../config/credentials/memory_bank
touch ../config/credentials/knowledge_graph_memory.jsonl

print_status "✅ MCP server installation completed!"
print_warning "Next steps:"
echo "1. Edit config/.env with your API keys"
echo "2. Run ./launch-mcps.sh to start MCP servers"
echo "3. Configure Claude Code with ./configure-claude-code.sh"