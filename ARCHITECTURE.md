# Technical Architecture

## Overview
Autonomous CodeGraph Manager (ACGM) is a **self-driving CLI tool** that automates the lifecycle of [CodeGraph](https://github.com/colbymchenry/codegraph) for AI coding agents.

## Components

### 1. **CodeGraphManager**
- **Initialization**: Runs `codegraph init -i` if `.codegraph/` does not exist.
- **Indexing**: Watches for file changes and re-indexes incrementally.
- **MCP Server**: Starts `codegraph serve --mcp` when an AI agent process is detected.
- **Git Sync**: Re-indexes on `git pull` or manual triggers.

### 2. **File Watcher**
- Uses `watchdog` to monitor file changes in the repository.
- Triggers re-indexing on modifications to supported file types (`.py`, `.js`, `.ts`, `.go`, `.rs`, `.java`, `.swift`, `.c`, `.h`, `.cpp`, `.hpp`).

### 3. **Process Monitor**
- Uses `psutil` to detect running AI agent processes (`claude`, `cursor`, `codex`, `opencode`, `hermes`).
- Starts/stops the MCP server based on agent activity.

### 4. **Git Integration**
- Uses `GitPython` to detect `git pull` or dirty working directories.
- Triggers re-indexing when changes are detected.

## Data Flow
```
[Git Repo] → [File Watcher] → [CodeGraphManager] → [CodeGraph CLI] → [MCP Server] → [AI Agent]
```

## Dependencies
- **Python 3.11+**: Core language.
- **click**: CLI interface.
- **watchdog**: File system monitoring.
- **psutil**: Process monitoring.
- **GitPython**: Git repository integration.
- **CodeGraph CLI**: Wrapped via subprocess.