# 🔧 MCP Configuration Setup

## 🔒 Security Notice
**Environment variables and sensitive configuration files are not tracked in Git for security reasons.**

## 🚀 Quick Setup Guide

### 1. Run Environment Setup Script
The easiest way to get started:

```bash
# Run the automated setup script
./scripts/setup-environment.sh
```

This script will:
- Create `.env` from `.env.example`
- Set up data directories
- Generate JWT secret key
- Configure MCP integration files
- Validate your setup

### 2. Configure Your API Keys
Edit the `.env` file with your actual API keys:

```bash
# Edit environment configuration
nano .env  # or your preferred editor

# Required: Add your Perplexity API key
PERPLEXITY_API_KEY=your_actual_perplexity_api_key

# Optional: Add GitHub token for enhanced features
GITHUB_TOKEN=your_github_token
```

### 3. Validate Setup
Verify everything is configured correctly:

```bash
# Validate environment configuration
./scripts/validate-environment.sh

# Load environment variables
source mcp-integration/set-mcp-env.sh
```

## 📁 Configuration Overview

### 🎯 Centralized Environment Management
All secrets and configuration are now managed through a single `.env` file:

| File | Purpose | Status |
|------|---------|--------|
| `.env` | Central configuration (API keys, paths, settings) | ✅ Created from `.env.example` |
| `.env.example` | Template with placeholder values | 📋 Tracked in Git |
| `mcp-integration/` | MCP server configurations | 🔗 References `.env` variables |

### 🔧 Supporting Scripts
| Script | Purpose |
|--------|---------|
| `scripts/setup-environment.sh` | Automated environment setup |
| `scripts/validate-environment.sh` | Validate configuration |
| `mcp-integration/set-mcp-env.sh` | Load environment for MCP |

## 🛡️ Security Features

- ✅ **Single source of truth** - All secrets in one `.env` file
- ✅ **Git-ignored credentials** - `.env` never committed to Git
- ✅ **Template tracked** - `.env.example` provides clear setup guide
- ✅ **Automated validation** - Scripts verify configuration completeness
- ✅ **Environment isolation** - Different configurations for dev/staging/prod

## ⚠️ Important Notes

1. **Never commit `.env` file** - Contains your actual API keys
2. **Use environment variables** - All configurations reference `${VARIABLE_NAME}`
3. **Keep `.env.example` updated** - When adding new environment variables
4. **Run validation scripts** - Ensure your environment is properly configured

## 🔍 Verification Steps

After setup, verify your configuration:

1. **Environment Validation**:
   ```bash
   ./scripts/validate-environment.sh
   ```

2. **MCP Integration Test**:
   ```bash
   source mcp-integration/set-mcp-env.sh
   # Check environment variables are loaded
   echo $PERPLEXITY_API_KEY  # Should show your key (partially hidden)
   ```

3. **Claude Code MCP Test**:
   - Restart Claude Code
   - Use `/mcp` command to check server status
   - Test Perplexity functionality

## 🆘 Troubleshooting

### Common Issues

**`.env file not found`**
```bash
# Run setup script to create .env from template
./scripts/setup-environment.sh
```

**`API key validation failed`**
```bash
# Check your API key in .env file
nano .env
# Validate configuration
./scripts/validate-environment.sh
```

**`MCP servers not loading`**
```bash
# Reload environment variables
source mcp-integration/set-mcp-env.sh
# Restart Claude Code completely
```

## 📚 Additional Resources

- **SECURITY.md** - Security best practices and guidelines
- **mcp-integration/README.md** - Detailed MCP setup documentation
- **.env.example** - Complete list of available environment variables