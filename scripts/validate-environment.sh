#!/bin/bash

# Environment Validation Script for Hackathon Demo
# Validates that all required environment variables are properly configured

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Validation counters
ERRORS=0
WARNINGS=0
CHECKS=0

print_banner() {
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║                🔍 ENVIRONMENT VALIDATION                 ║${NC}"
    echo -e "${CYAN}║              Checking Configuration Status               ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
    WARNINGS=$((WARNINGS + 1))
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
    ERRORS=$((ERRORS + 1))
}

print_info() {
    echo -e "${BLUE}[ℹ]${NC} $1"
}

print_section() {
    echo ""
    echo -e "${CYAN}▶ $1${NC}"
    echo "────────────────────────────────────────"
}

# Load environment variables from .env file
load_env() {
    if [ -f ".env" ]; then
        export $(cat .env | grep -v '^#' | grep -v '^$' | xargs)
        print_status ".env file loaded"
    else
        print_error ".env file not found. Run scripts/setup-environment.sh first."
        exit 1
    fi
}

# Check if a required environment variable is set and non-empty
check_required_var() {
    local var_name=$1
    local var_value=${!var_name}
    local description=$2
    
    CHECKS=$((CHECKS + 1))
    
    if [ -z "$var_value" ]; then
        print_error "Required variable $var_name is not set ($description)"
        return 1
    elif [ "$var_value" = "your_${var_name,,}_here" ] || [[ "$var_value" == *"your_"* ]]; then
        print_error "Variable $var_name contains placeholder value ($description)"
        return 1
    else
        print_status "$var_name is configured ($description)"
        return 0
    fi
}

# Check if an optional environment variable is set
check_optional_var() {
    local var_name=$1
    local var_value=${!var_name}
    local description=$2
    
    CHECKS=$((CHECKS + 1))
    
    if [ -z "$var_value" ]; then
        print_warning "Optional variable $var_name is not set ($description)"
        return 1
    elif [ "$var_value" = "your_${var_name,,}_here" ] || [[ "$var_value" == *"your_"* ]]; then
        print_warning "Variable $var_name contains placeholder value ($description)"
        return 1
    else
        print_status "$var_name is configured ($description)"
        return 0
    fi
}

# Validate API key format
validate_api_key() {
    local key_name=$1
    local key_value=${!key_name}
    local expected_prefix=$2
    local min_length=$3
    
    if [ -n "$key_value" ] && [ "$key_value" != "your_${key_name,,}_here" ]; then
        if [[ "$key_value" == "$expected_prefix"* ]] && [ ${#key_value} -ge $min_length ]; then
            print_status "$key_name format appears valid"
        else
            print_warning "$key_name format may be invalid (expected prefix: $expected_prefix, min length: $min_length)"
        fi
    fi
}

# Check file/directory paths
check_path() {
    local path_var=$1
    local path_value=${!path_var}
    local description=$2
    local should_exist=$3
    
    CHECKS=$((CHECKS + 1))
    
    if [ -n "$path_value" ]; then
        if [ "$should_exist" = "true" ]; then
            if [ -e "$path_value" ]; then
                print_status "$path_var path exists: $path_value"
            else
                print_warning "$path_var path does not exist: $path_value ($description)"
            fi
        else
            print_status "$path_var path configured: $path_value ($description)"
        fi
    else
        print_warning "$path_var is not set ($description)"
    fi
}

# Test API connectivity
test_perplexity_api() {
    if [ -n "$PERPLEXITY_API_KEY" ] && [ "$PERPLEXITY_API_KEY" != "your_perplexity_api_key_here" ]; then
        print_info "Testing Perplexity API connectivity..."
        
        # Simple API test (if curl is available)
        if command -v curl >/dev/null 2>&1; then
            response=$(curl -s -w "%{http_code}" -o /dev/null \
                -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
                -H "Content-Type: application/json" \
                -d '{"model":"llama-3.1-sonar-small-128k-online","messages":[{"role":"user","content":"test"}],"max_tokens":1}' \
                https://api.perplexity.ai/chat/completions 2>/dev/null || echo "000")
            
            if [ "$response" = "200" ]; then
                print_status "Perplexity API connection successful"
            elif [ "$response" = "401" ]; then
                print_error "Perplexity API authentication failed - check your API key"
            elif [ "$response" = "000" ]; then
                print_warning "Could not test Perplexity API (network/curl issue)"
            else
                print_warning "Perplexity API returned status: $response"
            fi
        else
            print_warning "curl not available - skipping API connectivity test"
        fi
    else
        print_warning "Perplexity API key not configured - skipping connectivity test"
    fi
}

# Main validation function
run_validation() {
    print_banner
    
    # Check if we're in the right directory
    if [ ! -f ".env.example" ]; then
        print_error "Not in project root directory. Please run from /workspaces/hackathon_demo/"
        exit 1
    fi
    
    load_env
    
    # Core MCP Requirements
    print_section "Core MCP Requirements"
    check_required_var "PERPLEXITY_API_KEY" "Perplexity Sonar API for web search"
    validate_api_key "PERPLEXITY_API_KEY" "pplx-" 20
    
    # MCP Storage Paths
    print_section "MCP Storage Configuration"
    check_optional_var "KNOWLEDGE_GRAPH_MEMORY_PATH" "Knowledge graph storage"
    check_optional_var "MEMORY_BANK_PATH" "Memory bank storage"
    check_path "KNOWLEDGE_GRAPH_MEMORY_PATH" "Knowledge graph storage" "false"
    check_path "MEMORY_BANK_PATH" "Memory bank storage" "false"
    
    # Security Configuration
    print_section "Security Configuration"
    check_optional_var "JWT_SECRET_KEY" "JWT token signing"
    if [ -n "$JWT_SECRET_KEY" ] && [ "$JWT_SECRET_KEY" != "your_jwt_secret_key_here" ]; then
        if [ ${#JWT_SECRET_KEY} -ge 32 ]; then
            print_status "JWT secret key length is adequate"
        else
            print_warning "JWT secret key should be at least 32 characters"
        fi
    fi
    
    # Optional Integrations
    print_section "Optional Integrations"
    check_optional_var "GITHUB_TOKEN" "GitHub API access"
    if [ -n "$GITHUB_TOKEN" ] && [ "$GITHUB_TOKEN" != "your_github_token_here" ]; then
        validate_api_key "GITHUB_TOKEN" "ghp_" 36
    fi
    
    # Application Configuration
    print_section "Application Configuration"
    check_optional_var "APP_ENV" "Application environment"
    check_optional_var "DATABASE_URL" "Database connection"
    check_optional_var "API_BASE_URL" "API base URL"
    check_optional_var "FRONTEND_URL" "Frontend URL for CORS"
    
    # Directory Structure
    print_section "Directory Structure"
    check_path "PWD/data" "Data directory" "false"
    check_path "PWD/logs" "Logs directory" "false"
    
    # API Connectivity Tests
    print_section "API Connectivity Tests"
    test_perplexity_api
    
    # Summary
    print_section "Validation Summary"
    echo "Total checks performed: $CHECKS"
    echo -e "Errors: ${RED}$ERRORS${NC}"
    echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"
    echo -e "Passed: ${GREEN}$((CHECKS - ERRORS - WARNINGS))${NC}"
    echo ""
    
    if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
        print_status "🎉 All validation checks passed! Environment is fully configured."
        echo ""
        echo -e "${GREEN}Your environment is ready for development!${NC}"
        return 0
    elif [ $ERRORS -eq 0 ]; then
        print_warning "⚠️  Validation completed with warnings. Environment is functional but has optional configurations missing."
        echo ""
        echo -e "${YELLOW}Environment is ready, but consider addressing the warnings above.${NC}"
        return 0
    else
        print_error "❌ Validation failed with errors. Please fix the issues above."
        echo ""
        echo -e "${RED}Next steps:${NC}"
        echo "1. Edit .env file to fix the errors above"
        echo "2. Run this validation script again: ./scripts/validate-environment.sh"
        echo "3. See SECURITY.md for security guidelines"
        return 1
    fi
}

# Handle script arguments
case "${1:-}" in
    --help|-h)
        echo "Environment Validation Script"
        echo ""
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --help, -h      Show this help message"
        echo "  --quiet, -q     Suppress non-error output"
        echo "  --api-only      Only test API connectivity"
        echo ""
        echo "This script validates:"
        echo "  • Required environment variables are set"
        echo "  • API keys have valid formats"
        echo "  • File paths are configured"
        echo "  • API connectivity (if possible)"
        ;;
    --quiet|-q)
        run_validation >/dev/null 2>&1
        exit $?
        ;;
    --api-only)
        load_env
        test_perplexity_api
        ;;
    *)
        run_validation
        ;;
esac