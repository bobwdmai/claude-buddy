#!/usr/bin/env bash
set -e

REPO="https://raw.githubusercontent.com/bobwdmai/claude-buddy/main"
CLAUDE_DIR="$HOME/.claude"
COMMANDS_DIR="$CLAUDE_DIR/commands"

mkdir -p "$COMMANDS_DIR"

echo "Downloading buddy.py..."
curl -fsSL "$REPO/src/claude_buddy/__main__.py" -o "$CLAUDE_DIR/buddy.py"

echo "Installing command..."
cat > "$COMMANDS_DIR/buddy.md" << 'EOF'
---
description: Your Claude Code terminal pet. Subcommands: pet, card, mute, unmute, off, gallery [species|rarity], set <species> [rarity] [shiny] [hat], reset, rename <name>, list.
---

Run this shell command and display the output exactly as-is, preserving all formatting:

```
python3 ~/.claude/buddy.py $ARGUMENTS
```

Do not add any commentary before or after the output. Just run it and show what comes back.

If the script doesn't exist, tell the user to reinstall: curl -fsSL https://raw.githubusercontent.com/bobwdmai/claude-buddy/main/install.sh | bash
EOF

echo "Done! Open Claude Code and run /buddy to meet your companion."
