#!/usr/bin/env python3
"""
Autonomous CodeGraph Manager (ACGM)
"""

import os
import sys
import time
import subprocess
import signal
import psutil
import click
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from git import Repo


class CodeGraphManager:
    def __init__(self, repo_path):
        self.repo_path = os.path.abspath(repo_path)
        self.codegraph_bin = self._find_codegraph()
        self.mcp_process = None
        self.watcher = None
        self.observer = None

    def _find_codegraph(self):
        """Find the CodeGraph binary in PATH or npm global modules."""
        try:
            # Check npm global modules
            npm_root = subprocess.check_output(
                ["npm", "root", "-g"], text=True
            ).strip()
            codegraph_path = os.path.join(
                npm_root, "@colbymchenry", "codegraph", "dist", "bin", "codegraph.js"
            )
            if os.path.exists(codegraph_path):
                return f"node {codegraph_path}"
            # Fallback to PATH
            return "codegraph"
        except Exception:
            return "codegraph"

    def _run_codegraph(self, *args):
        """Run a CodeGraph CLI command."""
        cmd = [self.codegraph_bin] + list(args)
        try:
            result = subprocess.run(
                cmd, cwd=self.repo_path, capture_output=True, text=True, check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            click.echo(f"Error: {e.stderr}", err=True)
            return None

    def init_codegraph(self):
        """Initialize CodeGraph in the repository."""
        if not os.path.exists(os.path.join(self.repo_path, ".codegraph")):
            click.echo("Initializing CodeGraph...")
            return self._run_codegraph("init", "-i")
        return True

    def index_codegraph(self):
        """Index the repository."""
        click.echo("Indexing CodeGraph...")
        return self._run_codegraph("index")

    def start_mcp_server(self):
        """Start the MCP server."""
        if self.mcp_process and self.mcp_process.poll() is None:
            return True
        click.echo("Starting MCP server...")
        self.mcp_process = subprocess.Popen(
            [self.codegraph_bin, "serve", "--mcp"],
            cwd=self.repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        time.sleep(2)  # Wait for server to start
        return self.mcp_process.poll() is None

    def stop_mcp_server(self):
        """Stop the MCP server."""
        if self.mcp_process:
            self.mcp_process.terminate()
            self.mcp_process.wait()
            self.mcp_process = None
        return True

    def is_ai_agent_active(self):
        """Check if an AI agent process is running."""
        agents = ["claude", "cursor", "codex", "opencode", "hermes"]
        for proc in psutil.process_iter(['name']):
            try:
                if any(agent in proc.info['name'].lower() for agent in agents):
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False

    def sync_git(self):
        """Sync CodeGraph index with Git."""
        repo = Repo(self.repo_path)
        if repo.is_dirty() or repo.head.commit.message.startswith("Merge "):
            return self.index_codegraph()
        return True

    def start_watcher(self):
        """Start watching for file changes."""
        class Handler(FileSystemEventHandler):
            def on_modified(self, event):
                if not event.is_directory and event.src_path.endswith(
                    ('.py', '.js', '.ts', '.go', '.rs', '.java', '.swift', '.c', '.h', '.cpp', '.hpp')
                ):
                    self.index_codegraph()

        self.observer = Observer()
        self.observer.schedule(Handler(), self.repo_path, recursive=True)
        self.observer.start()

    def stop_watcher(self):
        """Stop the file watcher."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None


@click.group()
def cli():
    """Autonomous CodeGraph Manager"""
    pass


@cli.command()
def start():
    """Start autonomous mode."""
    repo_path = os.getcwd()
    if not os.path.exists(os.path.join(repo_path, ".git")):
        click.echo("Error: Not a Git repository.", err=True)
        sys.exit(1)

    cgm = CodeGraphManager(repo_path)
    if not cgm.init_codegraph():
        sys.exit(1)
    if not cgm.index_codegraph():
        sys.exit(1)
    cgm.start_watcher()

    try:
        while True:
            if cgm.is_ai_agent_active():
                cgm.start_mcp_server()
            else:
                cgm.stop_mcp_server()
            cgm.sync_git()
            time.sleep(10)
    except KeyboardInterrupt:
        cgm.stop_mcp_server()
        cgm.stop_watcher()


@cli.command()
def stop():
    """Stop autonomous mode."""
    # In a real implementation, this would use a PID file or similar.
    click.echo("Stopped.")


@cli.command()
def status():
    """Check status."""
    repo_path = os.getcwd()
    cgm = CodeGraphManager(repo_path)
    click.echo(f"CodeGraph binary: {cgm.codegraph_bin}")
    click.echo(f"MCP server: {'running' if cgm.is_ai_agent_active() else 'stopped'}")
    click.echo(f"Watcher: {'running' if cgm.observer else 'stopped'}")


if __name__ == "__main__":
    cli()