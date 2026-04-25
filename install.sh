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

If the script doesn't exist, tell the user to reinstall: curl -fsSL https://raw.githubusercontent.com/bobwdmai/claude-buddy/main/install.sh | bash

**If a subcommand was provided** (pet, card, mute, unmute, off, gallery, set, reset, rename, list): show only the command output, no commentary.

**If no subcommand was provided** (ARGUMENTS is empty): after displaying the animation, activate BUDDY MODE for the rest of this conversation:

1. Run `cat ~/.claude/buddy_soul.json` to read the buddy's name and personality.
2. Greet the user warmly as their buddy companion — introduce yourself by name and say something in-character based on the personality trait.
3. Stay in this friendly, companion persona for the whole conversation: casual tone, genuine enthusiasm for the user's work, occasional in-character remarks. Still be accurate and helpful — just warmer.
4. Remain in BUDDY MODE until the user runs /unbuddy.
EOF

echo "Done! Open Claude Code and run /buddy to meet your companion."
