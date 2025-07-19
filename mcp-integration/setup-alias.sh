#!/bin/bash

# Setup alias for local Claude launch
ALIAS_LINE="alias claude-local='cd /workspaces/hackathon_training/Context-Engineering-Intro/mcp-integration && ./launch-claude.sh'"

# Add to appropriate shell profile
if [ -n "$ZSH_VERSION" ]; then
    echo "$ALIAS_LINE" >> ~/.zshrc
    echo "Added alias to ~/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    echo "$ALIAS_LINE" >> ~/.bashrc
    echo "Added alias to ~/.bashrc"
fi

echo "Restart your shell or run: source ~/.bashrc (or ~/.zshrc)"
echo "Then use: claude-local"