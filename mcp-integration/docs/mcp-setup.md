# MCP Integration Setup Guide

This document provides detailed instructions for setting up and configuring MCP servers with Claude Code.

## Prerequisites

- Node.js 18 or newer
- npm package manager
- Claude Code CLI installed
- Git (for version control)

## Detailed Setup Process

### 1. Project Initialization

Clone or set up the project structure:

```bash
# If cloning from repository
git clone <repository-url>
cd mcp-integration

# If setting up manually
mkdir mcp-integration && cd mcp-integration
# Copy all files from this project
```

### 2. Install Dependencies

```bash
# Run the setup script
npm run setup

# Or install manually
npm install -g @playwright/mcp
npm install -g mcp-knowledge-graph  
npm install -g @movibe/memory-bank-mcp
npm install -g perplexity-ask-mcp

# Install Playwright browsers
npx playwright install
```

### 3. Credential Configuration

#### Step 3.1: Create Environment File

```bash
cp config/.env.example config/.env
```

#### Step 3.2: Obtain Required API Keys

**Perplexity API Key:**
1. Visit [Perplexity AI](https://www.perplexity.ai/)
2. Sign up for an API account
3. Generate an API key from the dashboard
4. Add to `.env` file: `PERPLEXITY_API_KEY=your_key_here`

**GitHub Token (Optional):**
1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate new token with appropriate scopes
3. Add to `.env` file: `GITHUB_TOKEN=your_token_here`

#### Step 3.3: Configure Storage Paths

The system automatically creates storage directories, but you can customize:

```env
# Knowledge Graph storage (JSONL format)
KNOWLEDGE_GRAPH_MEMORY_PATH=./config/credentials/knowledge_graph_memory.jsonl

# Memory Bank storage (directory)
MEMORY_BANK_PATH=./config/credentials/memory_bank
```

### 4. Validate Configuration

```bash
# Run credential validation
npm run validate

# Check validation report
cat config/validation-report.json
```

Expected output:
```
✅ All required credentials validated successfully!
```

### 5. Launch MCP Servers

```bash
# Start all servers
npm run start

# Servers will launch in background
# PIDs stored in /tmp/mcp_pids.txt
```

### 6. Configure Claude Code

```bash
# Auto-configure Claude Code
npm run configure

# Or configure manually:
claude mcp add --scope project playwright -- npx @playwright/mcp@latest
claude mcp add --transport http --scope project perplexity -e PERPLEXITY_API_KEY=$PERPLEXITY_API_KEY -- npx -y perplexity-ask-mcp
claude mcp add --scope project knowledge-graph -- npx -y mcp-knowledge-graph --memory-path $KNOWLEDGE_GRAPH_MEMORY_PATH  
claude mcp add --scope project memory-bank -e MEMORY_BANK_PATH=$MEMORY_BANK_PATH -- npx @movibe/memory-bank-mcp
```

### 7. Verify Integration

#### In Claude Code:
```
/mcp
```

You should see all four MCP servers listed and connected.

#### Test Individual Servers:

**Playwright MCP:**
```
Can you take a screenshot of google.com?
```

**Perplexity Ask:**
```
What's the latest news about AI developments?
```

**Knowledge Graph:**
```
Create an entity called "Project Alpha" of type "software_project"
```

**Memory Bank:**
```
Initialize a memory bank for this project
```

## Advanced Configuration

### Custom Transport Configuration

For streamable HTTP transport, update `config/mcp-servers.json`:

```json
{
  "perplexity": {
    "transport": "http",
    "endpoint": "http://localhost:3001/mcp",
    "healthCheck": "http://localhost:3001/health"
  }
}
```

### Security Enhancements

#### Credential Encryption

Enable credential encryption in `.env`:

```env
ENCRYPT_CREDENTIALS=true
CREDENTIAL_ENCRYPTION_KEY=your_strong_encryption_key
```

#### Access Control

Configure auto-approval settings in `config/mcp-servers.json`:

```json
{
  "playwright": {
    "autoApprove": ["navigate", "click", "screenshot"],
    "requireApproval": ["type", "upload"]
  }
}
```

### Production Deployment

#### Environment-Specific Configuration

Create environment-specific files:

```bash
# Development
config/.env.development

# Production  
config/.env.production

# Staging
config/.env.staging
```

#### Docker Configuration

```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY . .

RUN npm run setup
EXPOSE 3001

CMD ["npm", "run", "start"]
```

## Troubleshooting Guide

### Server Startup Issues

**Issue: MCP servers fail to start**

```bash
# Check Node.js version
node --version  # Should be 18+

# Check npm global packages
npm list -g --depth=0

# Reinstall if needed
npm run setup
```

**Issue: Permission denied on scripts**

```bash
# Make scripts executable
chmod +x scripts/*.sh
chmod +x scripts/*.js
```

### Credential Problems

**Issue: API key validation fails**

```bash
# Test Perplexity API manually
curl -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model":"llama-3.1-sonar-small-128k-online","messages":[{"role":"user","content":"test"}],"max_tokens":1}' \
     https://api.perplexity.ai/chat/completions
```

**Issue: Path creation fails**

```bash
# Check directory permissions
ls -la config/

# Create manually if needed
mkdir -p config/credentials
touch config/credentials/knowledge_graph_memory.jsonl
```

### Claude Code Integration Issues

**Issue: MCP servers not visible in Claude Code**

```bash
# Check Claude Code MCP configuration
claude mcp list

# Restart Claude Code
# Re-run configuration
npm run configure
```

**Issue: Servers show as disconnected**

```bash
# Check server processes
ps aux | grep mcp

# Check server logs
npm run health

# Restart servers
npm run stop
npm run start
```

### Performance Optimization

#### Memory Usage

Monitor memory usage:

```bash
# Check server memory usage
ps aux | grep mcp | awk '{print $4, $11}'

# Adjust server timeouts in config/mcp-servers.json
"timeout": 60000,
"retryAttempts": 2
```

#### Network Configuration

Configure timeouts and retries:

```json
{
  "settings": {
    "timeout": 30000,
    "retryAttempts": 3,
    "retryDelay": 2000,
    "healthCheckInterval": 30000
  }
}
```

## Maintenance

### Regular Tasks

**Weekly:**
- Check server health: `npm run health`
- Validate credentials: `npm run validate`
- Update MCP packages: `npm run setup`

**Monthly:**
- Review validation reports
- Clean up log files
- Update API keys if needed

### Backup Procedures

```bash
# Backup knowledge graph data
cp config/credentials/knowledge_graph_memory.jsonl backup/

# Backup memory bank data  
tar -czf backup/memory_bank_$(date +%Y%m%d).tar.gz config/credentials/memory_bank/

# Backup configuration (without secrets)
cp config/.env.example backup/
cp config/mcp-servers.json backup/
```

## Migration Guide

### From Manual Setup

If you have existing MCP servers configured manually:

1. Export existing configuration:
   ```bash
   claude mcp list > existing_config.txt
   ```

2. Stop existing servers:
   ```bash
   pkill -f "mcp"
   ```

3. Follow setup process above

4. Migrate data:
   ```bash
   # Copy existing memory files
   cp ~/.local/share/knowledge_graph.jsonl config/credentials/knowledge_graph_memory.jsonl
   ```

### Version Updates

When updating MCP servers:

```bash
# Stop current servers
npm run stop

# Update packages
npm run setup

# Validate configuration
npm run validate

# Restart with new versions
npm run start
```

## Support

### Common Resources

- [MCP Protocol Documentation](https://modelcontextprotocol.io/)
- [Claude Code MCP Guide](https://docs.anthropic.com/en/docs/claude-code/mcp)
- [Playwright MCP Repository](https://github.com/microsoft/playwright-mcp)
- [Perplexity API Documentation](https://docs.perplexity.ai/)

### Getting Help

1. Check validation report: `cat config/validation-report.json`
2. Review server logs: `npm run health`
3. Test individual components: `npm run validate`
4. Check Claude Code status: `/mcp` command

### Reporting Issues

When reporting issues, include:

- Validation report output
- Server health status
- Claude Code MCP status
- Error messages and logs
- Environment details (Node.js version, OS, etc.)