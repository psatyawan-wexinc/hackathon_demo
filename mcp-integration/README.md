# MCP Integration with Secure Credential Management

A comprehensive solution for integrating multiple Model Context Protocol (MCP) servers with Claude Code, featuring automatic launch capabilities and secure credential storage.

## Features

- 🔐 **Secure Credential Management** - Environment-based storage with git-ignore protection
- 🚀 **Auto-Launch System** - Automated MCP server startup with health checks
- 🔍 **Credential Validation** - Pre-flight validation of all required API keys and paths
- 🌐 **Streamable HTTP Support** - Uses updated MCP protocol where applicable
- 📊 **Health Monitoring** - Real-time server status monitoring
- 🛠️ **Claude Code Integration** - Seamless configuration for Claude Code

## Supported MCP Servers

| Server | Description | Transport | Status |
|--------|-------------|-----------|--------|
| **Playwright MCP** | Browser automation capabilities | stdio | ✅ |
| **Perplexity Ask** | Real-time web search via Sonar API | http | ✅ |
| **Knowledge Graph** | Persistent memory through local graph | stdio | ✅ |
| **Memory Bank** | Cross-session context preservation | stdio | ✅ |

## Quick Start

### 🔒 Security Notice
**API keys and sensitive configuration files are not tracked in this repository for security.**

### 1. Copy Example Files
Copy the example configuration files and replace placeholders with actual values:

```bash
cd mcp-integration/

# Copy example files to actual config files
cp claude-settings.json.example claude-settings.json
cp set-mcp-env.sh.example set-mcp-env.sh
cp fix-mcp-config.sh.example fix-mcp-config.sh
cp INSTALLATION_SUMMARY.md.example INSTALLATION_SUMMARY.md
```

### 2. Configure API Keys
Replace `YOUR_PERPLEXITY_API_KEY_HERE` with your actual Perplexity API key in:
- `claude-settings.json`
- `set-mcp-env.sh`
- `fix-mcp-config.sh`
- `INSTALLATION_SUMMARY.md`

### 3. Set Environment Variables
```bash
# Set MCP environment variables
source set-mcp-env.sh

# Verify variables are set
env | grep -E "(PERPLEXITY|CLAUDE|MEMORY)"
```

### 4. Test Configuration
```bash
# Run configuration fix if needed
./fix-mcp-config.sh

# Restart Claude Code to load MCP servers
```

### 5. Verify Setup
```bash
# Test MCP functionality in Claude Code
# The servers should be automatically loaded
```

## Project Structure

```
mcp-integration/
├── README.md                           # Setup guide (this file)
├── claude-settings.json.example        # MCP server configuration template
├── set-mcp-env.sh.example             # Environment variables template  
├── fix-mcp-config.sh.example          # Configuration fix script template
├── INSTALLATION_SUMMARY.md.example    # Installation documentation template
├── config/
│   ├── mcp-servers.json               # Server configurations
│   ├── claude-code-config.json        # Claude Code settings
│   └── credentials/                   # Git-ignored credential storage
├── scripts/                           # Setup and management scripts
├── docs/                              # Additional documentation
└── package.json                       # NPM configuration
```

## Security Features

### Credential Protection
- ✅ **Never commit actual API keys** to version control
- ✅ **Use environment variables** for all sensitive configuration  
- ✅ **Keep example files for documentation** purposes
- ✅ **Actual config files are in .gitignore** to prevent accidental commits

### Access Control
- Project-scoped MCP configuration
- Auto-approval only for trusted operations
- Credential encryption support (optional)

## NPM Scripts

| Command | Description |
|---------|-------------|
| `npm run setup` | Install MCP servers and create structure |
| `npm run validate` | Validate credentials before launch |
| `npm run start` | Launch all MCP servers |
| `npm run stop` | Stop all running servers |
| `npm run configure` | Configure Claude Code integration |
| `npm run health` | Check server health status |

## Claude Code Integration

The system integrates with Claude Code using the official MCP protocol:

```bash
# Add servers with environment variables
claude mcp add --scope project playwright -- npx @playwright/mcp@latest
claude mcp add --transport http --scope project perplexity -e PERPLEXITY_API_KEY=xxx -- npx -y perplexity-ask-mcp

# List configured servers
claude mcp list

# Check server status in Claude Code
/mcp
```

## Streamable HTTP Protocol

This implementation uses the updated streamable HTTP protocol where supported:

- **Perplexity Ask MCP**: HTTP transport with Server-Sent Events
- **Other servers**: stdio transport for reliability
- **Health checks**: HTTP endpoints for monitoring

## Troubleshooting

### Common Issues

1. **Credential Validation Fails**
   ```bash
   npm run validate
   # Check output for specific credential issues
   ```

2. **MCP Servers Won't Start**
   ```bash
   # Check Node.js version (requires 18+)
   node --version
   
   # Reinstall dependencies
   npm run setup
   ```

3. **Claude Code Integration Issues**
   ```bash
   # Reconfigure Claude Code
   npm run configure
   
   # Check server status
   /mcp
   ```

### Health Monitoring

```bash
# Check all server statuses
npm run health

# View validation report
cat config/validation-report.json
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `PERPLEXITY_API_KEY` | ✅ | Perplexity Sonar API key |
| `GITHUB_TOKEN` | ❌ | GitHub personal access token |
| `KNOWLEDGE_GRAPH_MEMORY_PATH` | ✅ | Local storage path for knowledge graph |
| `MEMORY_BANK_PATH` | ✅ | Local storage path for memory bank |
| `MCP_TIMEOUT` | ❌ | Server startup timeout (default: 30000ms) |

## Contributing

1. Follow existing code patterns
2. Update documentation for new features
3. Test with `npm run validate` before committing
4. Ensure credentials are never committed

## License

MIT License - see LICENSE file for details