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

### 1. Initial Setup

```bash
# Install MCP servers and dependencies
npm run setup

# Configure credentials
cp config/.env.example config/.env
# Edit config/.env with your API keys
```

### 2. Configure Credentials

Edit `config/.env` with your actual credentials:

```env
# Required: Perplexity API Key
PERPLEXITY_API_KEY=your_actual_api_key_here

# Optional: GitHub token for enhanced Playwright features
GITHUB_TOKEN=your_github_token_here

# Paths (auto-created if needed)
KNOWLEDGE_GRAPH_MEMORY_PATH=./config/credentials/knowledge_graph_memory.jsonl
MEMORY_BANK_PATH=./config/credentials/memory_bank
```

### 3. Validate & Launch

```bash
# Validate all credentials
npm run validate

# Launch all MCP servers
npm run start

# Configure Claude Code integration
npm run configure
```

### 4. Verify Setup

```bash
# Check server health
npm run health

# In Claude Code, use:
/mcp
```

## Project Structure

```
mcp-integration/
├── config/
│   ├── .env.example              # Credential template
│   ├── mcp-servers.json         # Server configurations
│   ├── claude-code-config.json  # Claude Code settings
│   └── credentials/             # Git-ignored credential storage
├── scripts/
│   ├── setup-mcp.sh            # Initial setup script
│   ├── launch-mcps.sh          # Auto-launch script
│   ├── stop-mcps.sh            # Stop all servers
│   ├── validate-creds.js       # Credential validation
│   └── configure-claude-code.sh # Claude Code integration
├── docs/
│   └── mcp-setup.md            # Detailed setup guide
└── package.json                # NPM configuration
```

## Security Features

### Credential Protection
- All secrets stored in environment variables
- `.env` files are git-ignored by default
- Template files guide setup without exposing secrets
- Runtime validation prevents startup with invalid credentials

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