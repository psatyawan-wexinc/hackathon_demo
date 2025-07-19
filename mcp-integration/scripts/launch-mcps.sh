#!/bin/bash

# MCP Launch Script
# Automatically launches all configured MCP servers with credential validation

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

# Function to validate credentials
validate_credentials() {
    print_status "Validating credentials..."
    
    local has_errors=false
    
    # Check Perplexity API Key
    if [ -z "$PERPLEXITY_API_KEY" ]; then
        print_error "PERPLEXITY_API_KEY is not set in .env"
        has_errors=true
    else
        print_status "✓ Perplexity API key found"
    fi
    
    # Check knowledge graph memory path
    if [ -z "$KNOWLEDGE_GRAPH_MEMORY_PATH" ]; then
        print_error "KNOWLEDGE_GRAPH_MEMORY_PATH is not set in .env"
        has_errors=true
    else
        # Create directory if it doesn't exist
        mkdir -p "$(dirname "$KNOWLEDGE_GRAPH_MEMORY_PATH")"
        touch "$KNOWLEDGE_GRAPH_MEMORY_PATH"
        print_status "✓ Knowledge graph memory path configured"
    fi
    
    # Check memory bank path
    if [ -z "$MEMORY_BANK_PATH" ]; then
        print_error "MEMORY_BANK_PATH is not set in .env"
        has_errors=true
    else
        mkdir -p "$MEMORY_BANK_PATH"
        print_status "✓ Memory bank path configured"
    fi
    
    if [ "$has_errors" = true ]; then
        print_error "Credential validation failed. Please check your .env file."
        exit 1
    fi
    
    print_status "✅ All credentials validated successfully"
}

# Function to check if MCP server is running
check_mcp_server() {
    local server_name=$1
    local port=$2
    
    if [ -n "$port" ]; then
        if nc -z localhost "$port" 2>/dev/null; then
            print_status "✓ $server_name is running on port $port"
            return 0
        else
            print_warning "✗ $server_name is not running on port $port"
            return 1
        fi
    fi
}

# Function to launch MCP server
launch_mcp_server() {
    local server_name=$1
    local command=$2
    shift 2
    local args=("$@")
    
    print_status "Launching $server_name..."
    print_debug "Command: $command ${args[*]}"
    
    # Launch in background and capture PID
    "$command" "${args[@]}" &
    local pid=$!
    
    # Store PID for cleanup
    echo "$pid" >> /tmp/mcp_pids.txt
    
    print_status "✓ $server_name launched with PID $pid"
}

# Create PID file for cleanup
echo "" > /tmp/mcp_pids.txt

# Validate credentials before launching
validate_credentials

print_status "🚀 Launching MCP servers..."

# Launch Playwright MCP (stdio transport)
launch_mcp_server "Playwright MCP" "npx" "@playwright/mcp@latest"

# Launch Knowledge Graph MCP (stdio transport)
launch_mcp_server "Knowledge Graph MCP" "npx" "-y" "mcp-knowledge-graph" "--memory-path" "$KNOWLEDGE_GRAPH_MEMORY_PATH"

# Launch Memory Bank MCP (stdio transport)
launch_mcp_server "Memory Bank MCP" "npx" "@movibe/memory-bank-mcp"

# Launch Perplexity Sonar MCP (stdio transport)
PERPLEXITY_API_KEY="$PERPLEXITY_API_KEY" launch_mcp_server "Perplexity Sonar MCP" "npx" "-y" "server-perplexity-ask"

# Wait a moment for servers to start
sleep 3

print_status "✅ All MCP servers launched successfully!"
print_status "📝 Server PIDs stored in /tmp/mcp_pids.txt"
print_warning "To stop all servers, run: ./stop-mcps.sh"

# Optional: Show server status
if command -v ps &> /dev/null; then
    print_status "Active MCP server processes:"
    while read -r pid; do
        if [ -n "$pid" ] && ps -p "$pid" > /dev/null 2>&1; then
            ps -p "$pid" -o pid,cmd --no-headers | sed 's/^/  /'
        fi
    done < /tmp/mcp_pids.txt
fi