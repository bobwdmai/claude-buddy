"""Claude Buddy - terminal pet companion for Claude Code (April Fools 2026)"""

import sys, json, time, getpass
from pathlib import Path
from datetime import datetime

# ── Constants ──────────────────────────────────────────────────────────────────

SALT      = "friend-2026-401"
SOUL_PATH = Path.home() / ".claude" / "buddy_soul.json"

SPECIES = [
    "duck", "goose", "cat", "rabbit", "owl", "penguin",
    "turtle", "snail", "dragon", "octopus", "axolotl",
    "ghost", "robot", "blob", "cactus", "mushroom", "chonk", "capybara"
]

# (name, cumulative_prob_threshold, stars, stat_floor, available_hats)
RARITIES = [
    ("Common",    0.60, 1,  5, []),
    ("Uncommon",  0.85, 2, 15, ["Crown", "Top Hat", "Propeller"]),
    ("Rare",      0.95, 3, 25, ["Halo", "Wizard"]),
    ("Epic",      0.99, 4, 35, ["Beanie"]),
    ("Legendary", 1.00, 5, 50, ["Tiny Duck"]),
]

STATS = ["DEBUGGING", "PATIENCE", "CHAOS", "WISDOM", "SNARK"]

# ANSI
R  = "\033[0m"
BD = "\033[1m"
DM = "\033[2m"
RARITY_COLOR = {
    "Common":    "\033[37m",
    "Uncommon":  "\033[92m",
    "Rare":      "\033[94m",
    "Epic":      "\033[95m",
    "Legendary": "\033[93m",
}
RAINBOW = ["\033[91m", "\033[93m", "\033[92m", "\033[96m", "\033[94m", "\033[95m"]
STAT_BAR_COLOR = {
    "DEBUGGING": "\033[94m",
    "PATIENCE":  "\033[92m",
    "CHAOS":     "\033[91m",
    "WISDOM":    "\033[96m",
    "SNARK":     "\033[95m",
}

HAT_LINE = {
    "Crown":     "  vVv  ",
    "Top Hat":   " [===] ",
    "Propeller": "  ~@>  ",
    "Halo":      "  (o)  ",
    "Wizard":    "  /^\\  ",
    "Beanie":    " [~~~] ",
    "Tiny Duck": '  (")  ',
}

SPRITES = {
    "duck": [
        ['  (") ', ">(|||)<", "  ||| ", "  | | ", "       "],
        ['  (") ', ">(|||)<", "  ||| ", "   |  ", "       "],
        ['  (") ', ">(|||)<", "  |~| ", "  | | ", "  ~~~  "],
    ],
    "goose": [
        [" (  ) ", "  )   ", ">(||) ", "  ||  ", " /  \\ "],
        [" (  ) ", "  |   ", ">(||) ", "  ||  ", " /  \\ "],
        [" (  ) ", "  )   ", " (||) ", "  ||  ", " /  \\ "],
    ],
    "cat": [
        ["/\\./\\", "(=^=) ", " (u)  ", " | |  ", "       "],
        ["/\\./\\", "(=^=) ", " (u)  ", "  |   ", "       "],
        ["/\\.^\\", "(>^<) ", " (u)  ", " | |  ", "       "],
    ],
    "rabbit": [
        ["|\\ /| ", "(o_o) ", "( U ) ", " | |  ", "       "],
        ["|/ \\| ", "(o_o) ", "( U ) ", " | |  ", "       "],
        ["|\\ /| ", "(-_-) ", "( U ) ", " | |  ", "  zz   "],
    ],
    "owl": [
        ["(O,O) ", "(   ) ", "(: :) ", "-\"-\"- ", "       "],
        ["(O,O) ", "(   ) ", "(: :) ", " \" \"  ", "       "],
        ["(.,.) ", "(   ) ", "(: :) ", "-\"-\"- ", "       "],
    ],
    "penguin": [
        [" ___ ", "(o o)", " ( ) ", "  |  ", " /_\\ "],
        [" ___ ", "(o o)", " ( ) ", "  |  ", " | | "],
        [" ___ ", "(- -)", " ( ) ", "  |  ", " /_\\ "],
    ],
    "turtle": [
        [" ___ ", "(_8_)", "/|~|\\ ", "\\___/ ", "       "],
        [" ___ ", "(_8_)", " | |  ", "\\___/ ", "       "],
        [" ___ ", "(_0_)", "/|~|\\ ", "\\___/ ", "       "],
    ],
    "snail": [
        [" @@@  ", "(oo)  ", "( ~`- ", "------", "       "],
        [" @@@  ", "(.o)  ", "( ~`- ", "------", "       "],
        [" @@@  ", "(oo)  ", "(  `- ", "------", "  ~    "],
    ],
    "dragon": [
        ["/\\^/\\ ", "(o,o) ", "[   ] ", " |~|  ", " ^ ^  "],
        ["/\\^/\\ ", "(o,o) ", "[   ] ", " | |  ", " ^ ^  "],
        ["/\\*/\\ ", "(@,@) ", "[~~~] ", " |~|  ", " ^ ^  "],
    ],
    "octopus": [
        [" ___ ", "(o_o)", " ||| ", "/|||\\", "       "],
        [" ___ ", "(o_o)", " ||| ", " |||  ", "       "],
        [" ___ ", "(^_^)", " ||| ", "/|||\\", "       "],
    ],
    "axolotl": [
        ["wwwww ", "(o_o) ", ">   < ", " /_\\  ", "       "],
        ["wwwww ", "(o_o) ", ">~  < ", " /_\\  ", "       "],
        ["WWWWW ", "(@_@) ", ">   < ", " /_\\  ", "       "],
    ],
    "ghost": [
        [" ___ ", "( o )", "(   )", " \\_/ ", "  ~  "],
        [" ___ ", "( - )", "(   )", " \\_/ ", "     "],
        [" ___ ", "( o )", "(~~~)", " \\_/ ", "  ~  "],
    ],
    "robot": [
        ["[---] ", "[o_o] ", " |T|  ", " | |  ", "[___] "],
        ["[---] ", "[o-o] ", " |T|  ", " | |  ", "[___] "],
        ["[---] ", "[*_*] ", " |T|  ", " | |  ", "[___] "],
    ],
    "blob": [
        [" ___ ", "(o o)", "(   )", " ~~~ ", "     "],
        [" ___ ", "(o o)", " (  )", " ~~~ ", "     "],
        [" ___ ", "(^ ^)", "(   )", " ~~~ ", "     "],
    ],
    "cactus": [
        ["  |   ", " (|)  ", "  | * ", "  |   ", " /_\\  "],
        ["* |   ", " (|)  ", "  |   ", "  |   ", " /_\\  "],
        ["  |   ", " (|)  ", "* |   ", "  |   ", " /_\\  "],
    ],
    "mushroom": [
        [" _*_ ", "(*.*)", " ||| ", " | | ", "       "],
        [" _*_ ", "(*.*)", " ||| ", "  |  ", "       "],
        [" *** ", "(*o*)", " ||| ", " | | ", "       "],
    ],
    "chonk": [
        [" ___ ", "(o.o)", "( > )", "(___)", "       "],
        [" ___ ", "(o.o)", "(   )", "(___)", "       "],
        [" ___ ", "(-.-)", "( > )", "(___)", "  zz   "],
    ],
    "capybara": [
        [" ___ ", "(o_o)", "(___)", "/ | \\", "       "],
        [" ___ ", "(o_o)", "(___)", "  |  ", "       "],
        [" ___ ", "(-_-)", "(___)", "/ | \\", "  zz   "],
    ],
}

PERSONALITIES = {
    "duck":     "Enthusiastically quacks at merge conflicts.",
    "goose":    "Chaotic neutral. Will honk at your PRs.",
    "cat":      "Judges your variable names silently.",
    "rabbit":   "Hyper-focused, twitches at syntax errors.",
    "owl":      "Wise and patient. Has seen worse codebases.",
    "penguin":  "Cool under pressure. Always in the zone.",
    "turtle":   "Slow and steady. Never ships broken builds.",
    "snail":    "Takes their time. Excellent documentation.",
    "dragon":   "Breathes fire at spaghetti logic.",
    "octopus":  "Handles 8 tasks simultaneously. Naturally.",
    "axolotl":  "Can recover from any runtime error.",
    "ghost":    "Haunts legacy code. Knows where the bugs are.",
    "robot":    "Error-free by design. Allergic to tech debt.",
    "blob":     "Shapeshifts to fit any architecture.",
    "cactus":   "Thrives in dry, hostile review environments.",
    "mushroom": "Grows in the dark parts of the codebase.",
    "chonk":    "Big energy. Bigger commit messages.",
    "capybara": "Calm friend to all. Even to the monorepo.",
}

# ── PRNG (Mulberry32) ──────────────────────────────────────────────────────────

def fnv1a_32(s: str) -> int:
    h = 0x811C9DC5
    for c in s.encode():
        h ^= c
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h

class Mulberry32:
    def __init__(self, seed: int):
        self.s = seed & 0xFFFFFFFF

    def next(self) -> float:
        self.s = (self.s + 0x6D2B79F5) & 0xFFFFFFFF
        z = self.s
        z = ((z ^ (z >> 15)) * (z | 1)) & 0xFFFFFFFF
        z ^= (z + ((z ^ (z >> 7)) * (z | 61))) & 0xFFFFFFFF
        z = (z ^ (z >> 14)) & 0xFFFFFFFF
        return z / 0xFFFFFFFF

    def rand_int(self, n: int) -> int:
        return int(self.next() * n)

# ── Generation ─────────────────────────────────────────────────────────────────

def get_user_id() -> str:
    try:
        return getpass.getuser()
    except Exception:
        return "user"

def generate_bones(user_id: str) -> dict:
    seed = fnv1a_32(user_id + SALT)
    rng  = Mulberry32(seed)

    r = rng.next()
    rarity_name, stars, stat_floor, hats = "Common", 1, 5, []
    for name, threshold, s, floor, available_hats in RARITIES:
        if r < threshold:
            rarity_name, stars, stat_floor, hats = name, s, floor, available_hats
            break

    species = SPECIES[rng.rand_int(len(SPECIES))]
    shiny   = rng.next() < 0.01

    peak = rng.rand_int(len(STATS))
    dump = rng.rand_int(len(STATS) - 1)
    if dump >= peak:
        dump += 1
    stats = {}
    for i, stat in enumerate(STATS):
        if i == peak:
            val = min(100, stat_floor + 50 + int(rng.next() * 20))
        elif i == dump:
            val = max(0, stat_floor - 10 + int(rng.next() * 15))
        else:
            val = stat_floor + int(rng.next() * (100 - stat_floor))
        stats[stat] = val

    hat = hats[rng.rand_int(len(hats))] if hats else None

    return {"species": species, "rarity": rarity_name, "stars": stars,
            "shiny": shiny, "stats": stats, "hat": hat}

def _make_bones_for(species: str, rarity: str, shiny: bool, hat) -> dict:
    seed = fnv1a_32(get_user_id() + SALT + species + rarity)
    rng  = Mulberry32(seed)
    star, floor = 1, 5
    for rname, _, s, f, _ in RARITIES:
        if rname == rarity:
            star, floor = s, f
            break
    peak = rng.rand_int(len(STATS))
    dump = rng.rand_int(len(STATS) - 1)
    if dump >= peak:
        dump += 1
    stats = {}
    for i, stat in enumerate(STATS):
        if i == peak:
            val = min(100, floor + 50 + int(rng.next() * 20))
        elif i == dump:
            val = max(0, floor - 10 + int(rng.next() * 15))
        else:
            val = floor + int(rng.next() * (100 - floor))
        stats[stat] = val
    return {"species": species, "rarity": rarity, "stars": star,
            "shiny": shiny, "hat": hat, "stats": stats}

# ── Soul persistence ───────────────────────────────────────────────────────────

def load_soul() -> dict:
    if SOUL_PATH.exists():
        try:
            return json.loads(SOUL_PATH.read_text())
        except Exception:
            pass
    return {}

def save_soul(soul: dict):
    SOUL_PATH.parent.mkdir(parents=True, exist_ok=True)
    SOUL_PATH.write_text(json.dumps(soul, indent=2))

def get_buddy() -> dict:
    user_id = get_user_id()
    soul    = load_soul()

    bones = soul["override"] if "override" in soul else generate_bones(user_id)

    if "name" not in soul:
        soul["name"]        = bones["species"].capitalize()
        soul["hatch_date"]  = datetime.now().strftime("%Y-%m-%d")
        soul["muted"]       = False
        soul["visible"]     = True
        soul["personality"] = PERSONALITIES.get(bones["species"], "A mysterious companion.")
        save_soul(soul)

    return {**soul, **bones}

# ── Rendering ──────────────────────────────────────────────────────────────────

def colorize_shiny(lines: list[str]) -> list[str]:
    return [f"{RAINBOW[i % len(RAINBOW)]}{line}{R}" for i, line in enumerate(lines)]

def render_sprite(buddy: dict, frame: int = 0) -> list[str]:
    frames     = SPRITES.get(buddy["species"], SPRITES["blob"])
    frame_lines = list(frames[frame % 3])
    w = max(len(l) for l in frame_lines)
    frame_lines = [l.ljust(w) for l in frame_lines]

    hat = buddy.get("hat")
    if hat and hat in HAT_LINE:
        frame_lines = [HAT_LINE[hat].center(w)] + frame_lines

    if buddy.get("shiny"):
        return colorize_shiny(frame_lines)
    color = RARITY_COLOR.get(buddy["rarity"], "")
    return [f"{color}{l}{R}" for l in frame_lines]

def stars_str(n: int) -> str:
    return "★" * n + "☆" * (5 - n)

def stat_bar(val: int, color: str, width: int = 20) -> str:
    filled = int(val / 100 * width)
    return f"{color}{'█' * filled}{'░' * (width - filled)}{R} {BD}{val:3d}{R}"

# ── Commands ───────────────────────────────────────────────────────────────────

def cmd_show(buddy: dict):
    soul = load_soul()
    if not soul.get("visible", True):
        print(f"{DM}(Your buddy is hidden. Run /buddy to bring them back.){R}")
        return
    color     = RARITY_COLOR.get(buddy["rarity"], "")
    shiny_tag = f" {RAINBOW[0]}✦ SHINY{R}" if buddy["shiny"] else ""
    for frame in range(3):
        print("\033[H\033[J", end="")
        print()
        for line in render_sprite(buddy, frame):
            print(f"  {line}")
        print()
        print(f"  {BD}{color}{buddy['name']}{R}{shiny_tag}")
        print(f"  {color}{buddy['species'].upper()}{R}  {stars_str(buddy['stars'])}")
        print(f"  {DM}hatched {buddy.get('hatch_date', '?')}{R}")
        sys.stdout.flush()
        time.sleep(0.4)
    print()

def cmd_card(buddy: dict):
    color     = RARITY_COLOR.get(buddy["rarity"], "")
    shiny_tag = f" {RAINBOW[0]}✦ SHINY{R}" if buddy["shiny"] else ""
    sprite    = render_sprite(buddy, 1)

    print()
    print(f"  ╔══════════════════════════════╗")
    print(f"  ║  {BD}{color}{buddy['name']:^26}{R}  ║")
    print(f"  ║  {color}{buddy['species'].upper():^26}{R}  ║")
    print(f"  ║  {stars_str(buddy['stars']):^28}  ║")
    print(f"  ║  {color}{buddy['rarity']:^26}{R}  ║")
    if buddy["shiny"]:
        print(f"  ║  {RAINBOW[0]}{'✦ SHINY VARIANT':^26}{R}  ║")
    print(f"  ╠══════════════════════════════╣")
    print()
    for line in sprite:
        print(f"    {line}")
    if buddy.get("hat"):
        print(f"  {DM}Wearing: {buddy['hat']}{R}")
    print()
    print(f"  ╔══════════════════════════════╗")
    print(f"  ║  STATS{'':23}║")
    print(f"  ╠══════════════════════════════╣")
    for stat in STATS:
        val    = buddy["stats"][stat]
        scolor = STAT_BAR_COLOR.get(stat, "")
        print(f"  ║  {BD}{stat:<10}{R} {stat_bar(val, scolor, 14)} ║")
    print(f"  ╠══════════════════════════════╣")
    print(f"  ║  {DM}{'Personality:':^26}{R}  ║")
    words, line_buf, lines_p = buddy.get("personality", "").split(), [], []
    for w in words:
        if sum(len(x) + 1 for x in line_buf) + len(w) > 26:
            lines_p.append(" ".join(line_buf))
            line_buf = [w]
        else:
            line_buf.append(w)
    if line_buf:
        lines_p.append(" ".join(line_buf))
    for pl in lines_p:
        print(f"  ║  {pl:<28}║")
    print(f"  ╠══════════════════════════════╣")
    print(f"  ║  {DM}hatched {buddy.get('hatch_date', '?'):^22}{R}  ║")
    print(f"  ╚══════════════════════════════╝")
    print()

def cmd_pet(buddy: dict):
    soul      = load_soul()
    color     = RARITY_COLOR.get(buddy["rarity"], "")
    hearts    = ["♡", "♥", "❤", "♥", "❤", "♡"]
    sprite    = render_sprite(buddy, 2)
    print()
    for i, h in enumerate(hearts):
        print("\033[H\033[J", end="")
        print()
        for line in sprite:
            print(f"  {line}")
        print()
        print(f"{'  ' + '  ' * (i % 3)}{RAINBOW[i % len(RAINBOW)]}{h} {h} {h}{R}")
        sys.stdout.flush()
        time.sleep(0.25)
    print(f"\n  {BD}{color}{buddy['name']}{R} feels loved! 🐾\n")
    if not soul.get("muted"):
        speeches = [
            f"*happy {buddy['species']} noises*",
            "That was nice. Don't stop.",
            "I will debug twice as hard for you.",
            "( appreciation unlocked )",
        ]
        print(f"  {DM}\"{speeches[hash(buddy['name']) % len(speeches)]}\"{R}\n")

def cmd_mute(buddy: dict):
    soul = load_soul()
    soul["muted"] = True
    save_soul(soul)
    print(f"\n  {buddy['name']} is now quiet. {DM}(/buddy unmute to restore){R}\n")

def cmd_unmute(buddy: dict):
    soul = load_soul()
    soul["muted"] = False
    save_soul(soul)
    print(f"\n  {buddy['name']} is ready to talk again.\n")

def cmd_off(buddy: dict):
    soul = load_soul()
    soul["visible"] = False
    save_soul(soul)
    print(f"\n  {buddy['name']} is hiding. {DM}(/buddy to bring them back){R}\n")

def cmd_gallery(args: list):
    species_arg = None
    rarity_arg  = None
    for a in args:
        al = a.lower()
        if al in SPECIES:
            species_arg = al
        for rname, *_ in RARITIES:
            if rname.lower() == al:
                rarity_arg = rname

    if species_arg:
        print(f"\n  {BD}{species_arg.upper()}{R} — all rarities\n")
        for rname, _, stars, _, hats in RARITIES:
            rcolor  = RARITY_COLOR.get(rname, "")
            hat     = hats[0] if hats else None
            fake    = {"species": species_arg, "rarity": rname, "stars": stars,
                       "shiny": False, "hat": hat}
            hat_tag = f"  hat: {hat}" if hat else ""
            print(f"  {rcolor}{BD}{rname:<10}{R} {stars_str(stars)}{hat_tag}")
            for line in render_sprite(fake, 1):
                print(f"    {line}")
            print()
        shiny = {"species": species_arg, "rarity": "Legendary", "stars": 5,
                 "shiny": True, "hat": "Tiny Duck"}
        print(f"  {RAINBOW[2]}{BD}Legendary ✦ SHINY{R}  hat: Tiny Duck")
        for line in render_sprite(shiny, 2):
            print(f"    {line}")
        print()
        print(f"  {DM}'/buddy set {species_arg} legendary shiny' to adopt{R}\n")
        return

    display_rarity = rarity_arg or "Common"
    _, _, stars, _, hats = next(r for r in RARITIES if r[0] == display_rarity)
    hat = hats[0] if hats else None

    for idx, sp in enumerate(SPECIES):
        fake  = {"species": sp, "rarity": display_rarity, "stars": stars,
                 "shiny": False, "hat": hat}
        color = RARITY_COLOR.get(display_rarity, "")
        print("\033[H\033[J", end="")
        print()
        for line in render_sprite(fake, 1):
            print(f"  {line}")
        print()
        print(f"  {BD}{color}{sp.capitalize()}{R}")
        print(f"  {color}{sp.upper()}{R}  {stars_str(stars)}")
        print(f"  {DM}({idx + 1}/{len(SPECIES)}) — Ctrl+C to stop{R}")
        sys.stdout.flush()
        time.sleep(0.5)

    print(f"\n  {DM}'/buddy gallery <species>' — all rarities for one species")
    print(f"  '/buddy gallery <rarity>'  — all species at that rarity")
    print(f"  '/buddy set <species> [rarity] [shiny] [hat]' — adopt any{R}\n")

def cmd_set(args: list):
    hat_names_lower    = {k.lower(): k for k in HAT_LINE}
    rarity_names_lower = {r[0].lower(): r[0] for r in RARITIES}

    if not args or args[0].lower() not in SPECIES:
        print(f"\n  {BD}Usage:{R} /buddy set <species> [rarity] [shiny] [hat]")
        print(f"\n  {DM}Species:{R}  {', '.join(SPECIES)}")
        print(f"  {DM}Rarities:{R} {', '.join(r[0] for r in RARITIES)}")
        print(f"  {DM}Hats:{R}     {', '.join(HAT_LINE)}")
        print(f"\n  {DM}Example: /buddy set dragon legendary shiny{R}\n")
        return

    sp     = args[0].lower()
    rarity = "Common"
    shiny  = False
    hat    = None
    for a in args[1:]:
        al = a.lower()
        if al in rarity_names_lower:
            rarity = rarity_names_lower[al]
        elif al == "shiny":
            shiny = True
        elif al in hat_names_lower:
            hat = hat_names_lower[al]

    if hat is None:
        for rname, _, _, _, hats in RARITIES:
            if rname == rarity and hats:
                hat = hats[0]
                break

    bones = _make_bones_for(sp, rarity, shiny, hat)
    soul  = load_soul()
    soul["override"]    = bones
    soul["name"]        = sp.capitalize()
    soul["personality"] = PERSONALITIES.get(sp, "A mysterious companion.")
    soul["hatch_date"]  = datetime.now().strftime("%Y-%m-%d")
    soul.setdefault("muted",   False)
    soul.setdefault("visible", True)
    save_soul(soul)

    color     = RARITY_COLOR.get(rarity, "")
    shiny_tag = f" {RAINBOW[0]}✦ SHINY{R}" if shiny else ""
    hat_tag   = f", hat: {hat}" if hat else ""
    print(f"\n  Adopted {BD}{color}{sp.capitalize()}{R}{shiny_tag}!")
    print(f"  {DM}{rarity}{hat_tag} — run /buddy to meet them.{R}\n")

def cmd_reset():
    if SOUL_PATH.exists():
        SOUL_PATH.unlink()
        print(f"\n  Buddy released. {DM}(soul file deleted)")
        print(f"  Run /buddy to hatch a new companion.{R}\n")
    else:
        print(f"\n  {DM}No buddy to reset.{R}\n")

def cmd_rename(buddy: dict, args: list):
    if not args:
        print(f"\n  {BD}Usage:{R} /buddy rename <name>\n")
        return
    new_name = " ".join(args)
    soul     = load_soul()
    old_name = soul.get("name", buddy["name"])
    soul["name"] = new_name
    save_soul(soul)
    print(f"\n  {old_name} is now known as {BD}{new_name}{R}.\n")

def cmd_list():
    print(f"\n  {BD}Species ({len(SPECIES)}):{R}")
    for i, sp in enumerate(SPECIES):
        end = "\n" if (i + 1) % 6 == 0 or i == len(SPECIES) - 1 else "  "
        print(f"  {sp:<12}", end=end)
    print(f"\n  {BD}Rarities:{R}")
    for rname, _, stars, floor, hats in RARITIES:
        color   = RARITY_COLOR.get(rname, "")
        hat_str = ", ".join(hats) if hats else "none"
        print(f"  {color}{rname:<10}{R} {stars_str(stars)}  floor:{floor:3d}  hats: {hat_str}")
    print(f"\n  {BD}Hats:{R}")
    for hat, art in HAT_LINE.items():
        print(f"  {hat:<12} {art.strip()}")
    print()

# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    sub  = args[0].lower() if args else ""
    rest = args[1:]

    if sub == "gallery": cmd_gallery(rest); return
    if sub == "set":     cmd_set(rest);     return
    if sub == "reset":   cmd_reset();       return
    if sub == "list":    cmd_list();        return

    buddy = get_buddy()

    if   sub == "card":   cmd_card(buddy)
    elif sub == "pet":    cmd_pet(buddy)
    elif sub == "mute":   cmd_mute(buddy)
    elif sub == "unmute": cmd_unmute(buddy)
    elif sub == "off":    cmd_off(buddy)
    elif sub == "rename": cmd_rename(buddy, rest)
    else:
        soul = load_soul()
        if not soul.get("visible", True):
            soul["visible"] = True
            save_soul(soul)
        cmd_show(buddy)

if __name__ == "__main__":
    main()
