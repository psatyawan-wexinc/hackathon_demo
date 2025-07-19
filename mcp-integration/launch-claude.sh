#!/bin/bash

# Launch Claude with local MCP configuration
# This ensures the local .mcp.json file is used instead of global configs

cd "$(dirname "$0")"
claude --mcp-config .mcp.json "$@"