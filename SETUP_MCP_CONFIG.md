# 🔧 MCP Configuration Setup

## 🔒 Security Notice
**MCP configuration files with API keys are not tracked in Git for security reasons.**

## 📋 Quick Setup Guide

### 1. Copy Example Files
Run these commands to create your local configuration files:

```bash
# Root MCP configuration
cp .mcp.json.example .mcp.json

# MCP integration configuration  
cp mcp-integration/.mcp.json.example mcp-integration/.mcp.json

# Claude configuration
cp .claude/config.json.example .claude/config.json
```

### 2. Add Your API Key
Replace `YOUR_PERPLEXITY_API_KEY_HERE` with your actual Perplexity API key in:
- `.mcp.json`
- `mcp-integration/.mcp.json`
- `.claude/config.json`

### 3. Verify Setup
After copying and updating the files, your MCP servers should work properly with Claude Code.

## 📁 Configuration Files Overview

| File | Purpose | Required |
|------|---------|----------|
| `.mcp.json` | Root MCP server configuration | ✅ |
| `mcp-integration/.mcp.json` | Local MCP configuration | ✅ |
| `.claude/config.json` | Claude Code settings | ✅ |

## 🛡️ Security Features

- ✅ **Example files are tracked** - Safe templates in version control
- ✅ **Actual config files are ignored** - No secrets committed to Git
- ✅ **Local functionality maintained** - Files work normally once created
- ✅ **Setup instructions provided** - Clear guidance for new users

## ⚠️ Important Notes

1. **Never commit actual config files** - They contain your API keys
2. **Keep example files updated** - When adding new configurations
3. **Environment variables preferred** - For production deployments
4. **Revoke exposed keys** - If any keys were previously committed

## 🔍 Verification

After setup, you can verify your configuration by:
- Checking that MCP servers load in Claude Code
- Testing Perplexity functionality
- Ensuring no Git changes to config files