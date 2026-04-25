# claude-buddy

Terminal pet companion for [Claude Code](https://claude.ai/code) — Anthropic's April Fools 2026 surprise.

18 species · 5 rarity tiers · shiny variants · deterministic generation

## Install

```bash
pip install git+https://github.com/bobwdmai/claude-buddy.git
claude-buddy install
```

Or without pip:

```bash
curl -fsSL https://raw.githubusercontent.com/bobwdmai/claude-buddy/main/install.sh | bash
```

Then open Claude Code and run `/buddy`.

## Commands

| Command | Description |
|---|---|
| `/buddy` | Meet your companion — activates BUDDY MODE for the conversation |
| `/unbuddy` | Deactivate BUDDY MODE and return to normal behavior |
| `/buddy card` | Stat card with rarity, species, and all stats |
| `/buddy pet` | Pet your buddy |
| `/buddy gallery` | Slideshow of all 18 species |
| `/buddy gallery <species>` | One species at every rarity tier |
| `/buddy gallery <rarity>` | All species at a given rarity |
| `/buddy set <species> [rarity] [shiny] [hat]` | Adopt any combination |
| `/buddy list` | Print all valid species, rarities, and hats |
| `/buddy rename <name>` | Rename your buddy |
| `/buddy mute` | Toggle speech bubbles off |
| `/buddy unmute` | Toggle speech bubbles on |
| `/buddy off` | Hide buddy |
| `/buddy reset` | Release buddy and start fresh |

## Upgrade

```bash
pip install --upgrade git+https://github.com/bobwdmai/claude-buddy.git
claude-buddy upgrade
```

## Uninstall

```bash
claude-buddy uninstall
pip uninstall claude-buddy --yes
```
