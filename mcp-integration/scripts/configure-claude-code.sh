#!/bin/bash

# Claude Code MCP Configuration Script
# Configures Claude Code to use MCP servers with proper credentials

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

print_debug() {
    echo -e "${BLUE}[DEBUG]${NC} $1"
}

# Load environment variables
if [ -f "../config/.env" ]; then
    export $(cat ../config/.env | grep -v '^#' | xargs)
    print_status "Loaded environment variables from .env"
else
    print_error ".env file not found. Run setup-mcp.sh first."
    exit 1
fi

print_status "🔧 Configuring Claude Code MCP integration..."

# Function to add MCP server to Claude Code
add_mcp_server() {
    local name=$1
    local transport=$2
    shift 2
    local args=("$@")
    
    print_status "Adding $name to Claude Code..."
    
    if [ "$transport" = "http" ]; then
        print_debug "Using HTTP transport for $name"
        claude mcp add --transport http --scope project "$name" "${args[@]}"
    else
        print_debug "Using stdio transport for $name"
        claude mcp add --scope project "$name" "${args[@]}"
    fi
    
    if [ $? -eq 0 ]; then
        print_status "✓ $name added successfully"
    else
        print_warning "✗ Failed to add $name"
    fi
}

# Add Playwright MCP
add_mcp_server "playwright" "stdio" -- npx @playwright/mcp@latest

# Add Perplexity Ask MCP with API key
add_mcp_server "perplexity" "http" -e "PERPLEXITY_API_KEY=$PERPLEXITY_API_KEY" -- npx -y perplexity-ask-mcp

# Add Knowledge Graph MCP with memory path
add_mcp_server "knowledge-graph" "stdio" -- npx -y mcp-knowledge-graph --memory-path "$KNOWLEDGE_GRAPH_MEMORY_PATH"

# Add Memory Bank MCP with storage path
add_mcp_server "memory-bank" "stdio" -e "MEMORY_BANK_PATH=$MEMORY_BANK_PATH" -- npx @movibe/memory-bank-mcp

print_status "✅ Claude Code MCP configuration completed!"

# Show current MCP configuration
print_status "Current MCP servers configured in Claude Code:"
claude mcp list 2>/dev/null || print_warning "Unable to list MCP servers. Use '/mcp' command in Claude Code to check status."

print_warning "Next steps:"
echo "1. Restart Claude Code to load MCP servers"
echo "2. Use '/mcp' command in Claude Code to verify server status"
echo "3. Test MCP functionality with sample commands"