#!/bin/bash

# Security Hooks Setup Script
# Sets up Git hooks for automated secret detection and security validation

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

# Check if we're in a Git repository
if [ ! -d ".git" ]; then
    print_error "Not in a Git repository root directory"
    exit 1
fi

print_status "🔧 Setting up security hooks..."

# Create hooks directory if it doesn't exist
mkdir -p .git/hooks

# Pre-commit hook for secret detection
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# Pre-commit hook for secret detection and security validation
# This hook prevents commits that contain potential secrets or sensitive data

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[SECURITY]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Get list of files to be committed
FILES=$(git diff --cached --name-only --diff-filter=ACM)

if [ -z "$FILES" ]; then
    print_info "No files to check"
    exit 0
fi

print_status "🔍 Running security scan on staged files..."

VIOLATIONS=0

# Function to check for secrets in a file
check_secrets() {
    local file=$1
    local violations=0
    
    # Skip binary files
    if file "$file" | grep -q "binary"; then
        return 0
    fi
    
    # Skip files that should be ignored
    if echo "$file" | grep -qE "\.(example|template|md)$"; then
        return 0
    fi
    
    print_info "Scanning: $file"
    
    # Check for common API key patterns
    if grep -qE "(sk-[a-zA-Z0-9]{32,}|pplx-[a-zA-Z0-9]{40,}|xoxb-[a-zA-Z0-9\-]+|glpat-[a-zA-Z0-9_\-]+|ghp_[a-zA-Z0-9]{36}|gho_[a-zA-Z0-9]{36})" "$file"; then
        print_error "❌ Potential API key detected in $file"
        violations=$((violations + 1))
    fi
    
    # Check for hardcoded secrets
    if grep -qE "(api[_-]?key|secret[_-]?key|password|auth[_-]?token).*[:=]\s*[\"'][^\"']{10,}[\"']" "$file"; then
        print_error "❌ Potential hardcoded secret detected in $file"
        violations=$((violations + 1))
    fi
    
    # Check for database connection strings with credentials
    if grep -qE "(mysql|postgresql|mongodb)://[^@\s]+:[^@\s]+@[^/\s]+" "$file"; then
        print_error "❌ Database connection string with credentials detected in $file"
        violations=$((violations + 1))
    fi
    
    # Check for private keys
    if grep -qE "-----BEGIN [A-Z ]*PRIVATE KEY-----" "$file"; then
        print_error "❌ Private key detected in $file"
        violations=$((violations + 1))
    fi
    
    # Check for AWS access keys
    if grep -qE "AKIA[0-9A-Z]{16}" "$file"; then
        print_error "❌ AWS access key detected in $file"
        violations=$((violations + 1))
    fi
    
    # Check for environment variable assignments with secrets
    if grep -qE "export\s+[A-Z_]*(?:API_KEY|SECRET|PASSWORD|TOKEN)[A-Z_]*\s*=\s*[\"'][^\"']{10,}[\"']" "$file"; then
        print_error "❌ Environment variable with hardcoded secret detected in $file"
        violations=$((violations + 1))
    fi
    
    # Check for common credential file patterns
    if echo "$file" | grep -qE "(\.env$|credentials|secrets|\.pem$|\.key$|id_rsa)"; then
        if [ ! -f ".gitignore" ] || ! grep -q "$(basename "$file")" ".gitignore"; then
            print_error "❌ Potential credential file not in .gitignore: $file"
            violations=$((violations + 1))
        fi
    fi
    
    return $violations
}

# Check each staged file
for file in $FILES; do
    if [ -f "$file" ]; then
        check_secrets "$file"
        VIOLATIONS=$((VIOLATIONS + $?))
    fi
done

# Additional checks
print_info "Running additional security checks..."

# Check if .env files are being committed
if echo "$FILES" | grep -qE "\.env$|\.env\."; then
    print_error "❌ .env file detected in staged files"
    VIOLATIONS=$((VIOLATIONS + 1))
fi

# Check if any config.json files are being committed
if echo "$FILES" | grep -q "config\.json$"; then
    print_warning "⚠️  config.json file detected - ensure it contains no secrets"
fi

# Final verdict
echo ""
if [ $VIOLATIONS -eq 0 ]; then
    print_status "✅ Security scan passed - no secrets detected"
    print_status "🚀 Commit proceeding..."
    exit 0
else
    print_error "🚨 Security scan failed - $VIOLATIONS violation(s) detected"
    echo ""
    print_error "COMMIT BLOCKED - Fix the security issues above before committing"
    echo ""
    print_info "To fix these issues:"
    echo "  1. Remove hardcoded secrets from files"
    echo "  2. Add sensitive files to .gitignore"
    echo "  3. Use environment variables for credentials"
    echo "  4. Create .example files with placeholder values"
    echo ""
    print_info "For help, see SECURITY.md"
    exit 1
fi
EOF

# Make pre-commit hook executable
chmod +x .git/hooks/pre-commit

print_status "✅ Pre-commit hook installed successfully"

# Create a simple post-commit hook for security reminders
cat > .git/hooks/post-commit << 'EOF'
#!/bin/bash

# Post-commit hook for security reminders

echo ""
echo "🔒 Security Reminder:"
echo "   • Verify no secrets were committed"
echo "   • Use environment variables for credentials"
echo "   • Keep .gitignore updated with sensitive file patterns"
echo ""
EOF

chmod +x .git/hooks/post-commit

print_status "✅ Post-commit hook installed successfully"

# Test the pre-commit hook setup
print_status "🧪 Testing hook installation..."

if [ -x ".git/hooks/pre-commit" ]; then
    print_status "✅ Pre-commit hook is executable"
else
    print_error "❌ Pre-commit hook is not executable"
    exit 1
fi

if [ -x ".git/hooks/post-commit" ]; then
    print_status "✅ Post-commit hook is executable"
else
    print_error "❌ Post-commit hook is not executable"
    exit 1
fi

print_status "🎉 Security hooks setup completed!"
print_warning "Next steps:"
echo "  1. Test the hooks with a sample commit"
echo "  2. Review SECURITY.md for additional guidelines"
echo "  3. Ensure team members run this setup script"
echo ""
print_debug "To disable hooks temporarily: git commit --no-verify"
print_debug "To remove hooks: rm .git/hooks/pre-commit .git/hooks/post-commit"