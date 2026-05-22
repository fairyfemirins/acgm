# Autonomous CodeGraph Manager (ACGM)

A self-driving CLI tool to **auto-initialize, index, and serve** [CodeGraph](https://github.com/colbymchenry/codegraph) for AI coding agents (Claude Code, Cursor, Codex, OpenCode, Hermes).

## Features
- **Auto-initialize** CodeGraph in any Git repository.
- **Auto-index** code on file changes (watch mode).
- **Auto-serve** the MCP server when an AI agent is active.
- **Auto-update** the index on `git pull` or manual triggers.
- **Zero-config**: Works out of the box with existing CodeGraph installations.

## Installation
```bash
pip install --user acgm
```

## Usage
```bash
# Start autonomous mode in the current Git repo
acgm start

# Stop autonomous mode
acgm stop

# Check status
acgm status
```

## How It Works
1. **Initialization**: Runs `codegraph init -i` if `.codegraph/` does not exist.
2. **Indexing**: Watches for file changes and re-indexes incrementally.
3. **MCP Server**: Starts `codegraph serve --mcp` when an AI agent process is detected.
4. **Git Sync**: Re-indexes on `git pull` or manual triggers.

## License
MIT