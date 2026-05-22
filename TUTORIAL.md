# Reproducible Tutorial: Autonomous CodeGraph Manager

## Prerequisites
- **Python 3.11+**
- **Git**
- **Node.js 18+** (for CodeGraph)
- **CodeGraph CLI** (`npm i -g @colbymchenry/codegraph`)

## Setup
```bash
# Clone the repository
git clone https://github.com/femirins/acgm.git
cd acgm

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage
```bash
# Start autonomous mode in a Git repository
cd /path/to/your/project
acgm start

# Check status
acgm status

# Stop autonomous mode
acgm stop
```

## Expected Output
```
$ acgm start
Initializing CodeGraph...
Indexing CodeGraph...
Starting MCP server...
Watcher: running
MCP server: running
```

## Verification
1. **CodeGraph Initialization**: Check for `.codegraph/` directory.
2. **MCP Server**: Run `ps aux | grep codegraph` to see the server process.
3. **File Watcher**: Modify a file and check for re-indexing logs.