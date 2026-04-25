"""claude-buddy install / uninstall CLI."""

import sys
import shutil
from pathlib import Path


COMMANDS_DIR = Path.home() / ".claude" / "commands"
DEST         = COMMANDS_DIR / "buddy.md"
DATA_DIR     = Path(__file__).parent / "data"


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"

    if cmd == "install":
        _install()
    elif cmd == "uninstall":
        _uninstall()
    elif cmd == "upgrade":
        _install(upgrade=True)
    else:
        print("Usage: claude-buddy install | uninstall | upgrade")
        sys.exit(0 if cmd in ("help", "--help", "-h") else 1)


def _install(upgrade: bool = False):
    COMMANDS_DIR.mkdir(parents=True, exist_ok=True)

    if DEST.exists() and not upgrade:
        print(f"Already installed at {DEST}")
        print("Run 'claude-buddy upgrade' to overwrite with the latest version.")
        return

    shutil.copy(DATA_DIR / "buddy.md", DEST)
    verb = "Upgraded" if upgrade and DEST.exists() else "Installed"
    print(f"{verb}: {DEST}")
    print("Open Claude Code and run /buddy to meet your companion.")


def _uninstall():
    if DEST.exists():
        DEST.unlink()
        print(f"Removed: {DEST}")
        print("Soul file kept at ~/.claude/buddy_soul.json — delete manually to fully reset.")
    else:
        print("Not installed.")
