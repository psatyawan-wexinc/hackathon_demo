#!/bin/bash

# Environment Setup Script for Hackathon Demo
# This script helps new developers quickly configure their environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_banner() {
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║                  🚀 ENVIRONMENT SETUP                    ║${NC}"
    echo -e "${CYAN}║              Hackathon Demo Configuration                ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[ℹ]${NC} $1"
}

print_step() {
    echo -e "${CYAN}[→]${NC} $1"
}

# Check if we're in the project root
check_project_root() {
    if [ ! -f ".env.example" ]; then
        print_error "Not in project root directory. Please run from /workspaces/hackathon_demo/"
        exit 1
    fi
}

# Create .env file from .env.example
setup_env_file() {
    print_step "Setting up environment configuration..."
    
    if [ -f ".env" ]; then
        print_warning ".env file already exists. Creating backup..."
        cp .env .env.backup.$(date +%Y%m%d_%H%M%S)
        print_status "Backup created"
    fi
    
    # Copy .env.example to .env
    cp .env.example .env
    print_status ".env file created from .env.example"
    
    print_info "You need to edit .env with your actual values:"
    echo ""
    echo -e "${YELLOW}   Required API Keys:${NC}"
    echo "   • PERPLEXITY_API_KEY - Get from https://www.perplexity.ai/settings/api"
    echo ""
    echo -e "${YELLOW}   Optional but Recommended:${NC}"
    echo "   • GITHUB_TOKEN - For enhanced features"
    echo "   • JWT_SECRET_KEY - Generate a strong random string"
    echo ""
}

# Create data directories
setup_directories() {
    print_step "Creating data directories..."
    
    mkdir -p data
    mkdir -p logs
    mkdir -p data/memory_bank
    mkdir -p data/knowledge_graph
    
    print_status "Data directories created"
}

# Validate environment variables
validate_setup() {
    print_step "Validating setup..."
    
    if [ ! -f ".env" ]; then
        print_error ".env file not found"
        return 1
    fi
    
    # Check if PERPLEXITY_API_KEY is set to a non-placeholder value
    PERPLEXITY_KEY=$(grep "PERPLEXITY_API_KEY=" .env | cut -d'=' -f2)
    
    if [ "$PERPLEXITY_KEY" = "your_perplexity_api_key_here" ] || [ -z "$PERPLEXITY_KEY" ]; then
        print_warning "PERPLEXITY_API_KEY still contains placeholder value"
        echo "   Please edit .env and add your actual Perplexity API key"
        return 1
    fi
    
    print_status "Environment validation passed"
    return 0
}

# Generate JWT secret key
generate_jwt_secret() {
    print_step "Generating JWT secret key..."
    
    # Generate a random 64-character string
    JWT_SECRET=$(openssl rand -hex 32 2>/dev/null || python3 -c "import secrets; print(secrets.token_hex(32))" 2>/dev/null || echo "change_this_jwt_secret_in_production_$(date +%s)")
    
    # Update .env file with generated secret
    if grep -q "JWT_SECRET_KEY=your_jwt_secret_key_here" .env; then
        sed -i "s/JWT_SECRET_KEY=your_jwt_secret_key_here/JWT_SECRET_KEY=$JWT_SECRET/" .env
        print_status "JWT secret key generated and added to .env"
    else
        print_info "JWT secret key already configured"
    fi
}

# Setup MCP integration
setup_mcp_integration() {
    print_step "Setting up MCP integration..."
    
    # Check if MCP configuration directory exists
    if [ -d "mcp-integration" ]; then
        print_status "MCP integration directory found"
        
        # Copy example files if they don't exist
        cd mcp-integration
        
        if [ ! -f "set-mcp-env.sh" ] && [ -f "set-mcp-env.sh.example" ]; then
            cp set-mcp-env.sh.example set-mcp-env.sh
            chmod +x set-mcp-env.sh
            print_status "Created set-mcp-env.sh from example"
        fi
        
        if [ ! -f "fix-mcp-config.sh" ] && [ -f "fix-mcp-config.sh.example" ]; then
            cp fix-mcp-config.sh.example fix-mcp-config.sh
            chmod +x fix-mcp-config.sh
            print_status "Created fix-mcp-config.sh from example"
        fi
        
        if [ ! -f "claude-settings.json" ] && [ -f "claude-settings.json.example" ]; then
            cp claude-settings.json.example claude-settings.json
            print_status "Created claude-settings.json from example"
        fi
        
        cd ..
    else
        print_warning "MCP integration directory not found"
    fi
}

# Display next steps
show_next_steps() {
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║                    🎯 NEXT STEPS                         ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${YELLOW}1. Configure API Keys:${NC}"
    echo "   nano .env  # or your preferred editor"
    echo "   • Add your Perplexity API key"
    echo "   • Optionally add GitHub token"
    echo ""
    echo -e "${YELLOW}2. Validate Configuration:${NC}"
    echo "   ./scripts/validate-environment.sh"
    echo ""
    echo -e "${YELLOW}3. Set Environment Variables:${NC}"
    echo "   source mcp-integration/set-mcp-env.sh"
    echo ""
    echo -e "${YELLOW}4. Test MCP Integration:${NC}"
    echo "   # In Claude Code, use: /mcp"
    echo ""
    echo -e "${GREEN}📖 For detailed help, see:${NC}"
    echo "   • README.md - Project overview"
    echo "   • SECURITY.md - Security guidelines"
    echo "   • mcp-integration/README.md - MCP setup details"
    echo ""
}

# Main execution
main() {
    print_banner
    
    print_info "This script will set up your development environment"
    echo ""
    
    check_project_root
    setup_env_file
    setup_directories
    generate_jwt_secret
    setup_mcp_integration
    
    echo ""
    if validate_setup; then
        print_status "🎉 Environment setup completed successfully!"
    else
        print_warning "⚠️  Environment setup completed with warnings"
        print_info "Please review the warnings above and configure missing values"
    fi
    
    show_next_steps
}

# Script options
case "${1:-}" in
    --help|-h)
        echo "Environment Setup Script"
        echo ""
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --help, -h     Show this help message"
        echo "  --validate     Only run validation"
        echo "  --silent       Run without interactive prompts"
        echo ""
        echo "This script:"
        echo "  • Creates .env from .env.example"
        echo "  • Sets up data directories"
        echo "  • Generates JWT secret key"
        echo "  • Configures MCP integration"
        echo "  • Validates the setup"
        ;;
    --validate)
        check_project_root
        if validate_setup; then
            print_status "✅ Environment validation passed"
            exit 0
        else
            print_error "❌ Environment validation failed"
            exit 1
        fi
        ;;
    *)
        main
        ;;
esac