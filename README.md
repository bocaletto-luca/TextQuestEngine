# TextQuestEngine

**Author**: Luca Bocaletto (bocaletto-luca)  
**Repository**: https://github.com/bocaletto-luca/TextQuestEngine  
**License**: GNU GPL v3.0

A Python engine for creating modular, extensible, and standalone text adventures. This repository includes:

- Core engine: parser, dispatcher, loader, plugin system  
- A complete demo: “The Lost Cave”  
- CLI tools to scaffold, run, test, lint, build and package your adventure  

---

## Table of Contents

- [Features](#features)  
- [Prerequisites](#prerequisites)  
- [Installation](#installation)  
- [Usage](#usage)  
  - [CLI Commands](#cli-commands)  
  - [Demo Walkthrough](#demo-walkthrough)  
- [Project Structure](#project-structure)  
- [Demo “The Lost Cave”](#demo-the-lost-cave)  
  - [world.yaml](#worldyaml)  
  - [items.json](#itemsjson)  
  - [Plugin: light_plugin.py](#plugin-light_pluginpy)  
- [Packaging](#packaging)  
- [Contributing](#contributing)  
- [License](#license)  

---

## Features

- Multilingual parser (Italian/English) with synonyms  
- Event-driven dispatcher & plugin hooks (`pre_action`, `command_<cmd>`, `post_action`)  
- World loader from YAML + JSON (`world.yaml` + `items.json`)  
- Built-in support for rooms, items, NPCs, missions, game time  
- Intuitive CLI: `init`, `run`, `test`, `lint`, `build`, `package`  
- Standalone packaging via PyInstaller  

---

## Prerequisites

- Python 3.8+  
- pip  
- (optional) PyInstaller for standalone packaging  

---

## Installation

```bash
git clone https://github.com/bocaletto-luca/TextQuestEngine.git
cd TextQuestEngine
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pip install pyinstaller       # only if you intend to use `tqe package`
```

---

## Usage

### CLI Commands

After installation, the `tqe` command (alias for `python3 -m engine.utils.cli`) provides:

```bash
tqe init <project_name>            # Scaffold a new adventure project
tqe run --world <path/world.yaml>  # Launch the interactive game
tqe test                           # Run unit & integration tests (pytest)
tqe lint                           # Check code style & quality
tqe build                          # Build sdist & wheel packages
tqe package                        # Create a standalone executable (PyInstaller)
```

### Demo Walkthrough

The demo “The Lost Cave” is in `demo_adventure/`. To try it:

```bash
cd demo_adventure
tqe run
```

Sample commands:

```txt
> look
> take torch
> move inside
> use torch
> look
> take gem
> missions
```

---

## Project Structure

```
TextQuestEngine/
├── engine/                   # Core engine code
│   ├── core/
│   │   ├── dispatcher.py
│   │   ├── game.py
│   │   ├── parser.py
│   │   └── cli_commands.py
│   ├── data/
│   │   ├── loader.py
│   │   └── models.py
│   ├── plugins/
│   │   └── base.py
│   └── utils/
│       └── cli.py
├── demo_adventure/           # “The Lost Cave” demo
│   ├── config/
│   │   ├── world.yaml
│   │   └── items.json
│   ├── plugins/
│   │   └── light_plugin.py
│   └── assets/
│       └── map.txt
├── src/                      # PyInstaller entrypoint
│   └── main.py
├── setup.py
└── README.md
```

---

## Demo “The Lost Cave”

### world.yaml

```yaml
# demo_adventure/config/world.yaml

config:
  start_room: house
  start_time: 0
  intro_text: >
    You are an explorer seeking epic adventures… and epically bad jokes.
    If you can keep a grin while risking life and limb, you’re in the right place!
  initial_missions:
    - mission_gem
    - mission_beer

rooms:

  house:
    name: Abandoned House
    desc: >
      A dusty little house filled with creaky furniture and mysterious
      oddities. A torch glints on the table like a miniature sun.
    connections:
      outside: forest
    items:
      - torch

  forest:
    name: Messy Forest
    desc: >
      Trees look like they’ve given each other bad haircuts. A winding path
      leads deeper, where a mysterious cave yawns in darkness.
    connections:
      back: house
      inside: cave
    items: []

  cave:
    name: Dark (and Witty) Cave
    desc: >
      It’s so dark even your brightest ideas struggle to stand out.
      Maybe you need something to light the way… or at least a comedian.
    connections:
      exit: forest
    items: []

  tavern:
    name: Tavern of the Dozy Gnome
    desc: >
      A humble tavern where every patron snores into their pint.
      The bar is lined with bottles—most as empty as your wallet.
    connections:
      outside: house
    items:
      - beer

npcs:

  lazy_gnome:
    name: Lazy Gnome
    location: tavern
    dialogues:
      - text: "Oh, traveler! If you have a beer, we can call it ‘friendship’."
        options:
          - reply: "Here’s a beer"
            text: "Ah, finally! *sneeze*"
            next: end
          - reply: "I have a gem"
            text: "A gem? I prefer frothy mugs, but sure…"
            next: end
      - text: "end"
        options: []

missions:

  mission_gem:
    title: "The Shiny Gem"
    description: >
      Legend speaks of a precious gem hidden in the dark depths of the cave.
      Find it and bring it back… and maybe entertain a gnome!
    requirements:
      have_item: ["gem"]
    steps:
      - "Enter the cave"
      - "Light the torch"
      - "Take the gem"
      - "Return to the Lazy Gnome"
    rewards:
      xp: 50
      message: "You lit up the cave… and one gnome’s spirits!"

  mission_beer:
    title: "Bring the Beer"
    description: >
      The Lazy Gnome is parched. Fetch a cold beer and present it with flair.
    requirements:
      have_item: ["beer"]
    steps:
      - "Find a beer"
      - "Go to the tavern"
      - "Give the beer to the Lazy Gnome"
    rewards:
      xp: 20
      message: "The gnome now sleeps soundly. Mission accomplished!"
```

### items.json

```json
{
  "torch": {
    "names": ["torch", "lantern"],
    "description": "A battery-powered torch that shines brightly—perfect for caves.",
    "weight": 1.0,
    "usable_on": ["cave"]
  },
  "gem": {
    "names": ["gem", "precious stone"],
    "description": "A sparkling gem embedded in the cave wall—brighter than your wits.",
    "weight": 0.2,
    "usable_on": []
  },
  "beer": {
    "names": ["beer", "pint", "bottle"],
    "description": "A frothy pint of beer: liquid consolation for any gnome.",
    "weight": 0.5,
    "usable_on": ["lazy_gnome"]
  }
}
```

### Plugin: `light_plugin.py`

```python
# demo_adventure/plugins/light_plugin.py

from engine.plugins.base import PluginBase
from types import SimpleNamespace

class LightPlugin(PluginBase):
    """
    Handles darkness in the cave and torch usage:
    - Blocks vision until the torch is lit
    - Spawns the gem once lit
    """

    def on_pre_action(self, action: SimpleNamespace, state, world):
        if action.command == "look" and state["current_room"] == "cave":
            if not state.get("torch_lit", False):
                return "It’s too dark to see. Maybe a torch would help!"
        return None

    def on_command_use(self, action: SimpleNamespace, state, world):
        if action.target == "torch":
            state["torch_lit"] = True
            cave = world.rooms["cave"]
            if "gem" not in cave.items:
                cave.items.append("gem")
            return "You light the torch! Warm glow reveals a shiny gem."
        return None
```

---

## Packaging

To build a standalone executable:

```bash
pip install pyinstaller
tqe package
```

The binary (plus `config/` and `assets/`) will appear in `dist/`. Rename it to `tqe` and distribute!

---

## Contributing

1. Fork the repository  
2. Create a feature branch (`feature/your-feature`)  
3. Make changes, run `tqe test` & `tqe lint`  
4. Submit a Pull Request  

---

## License

This project is licensed under **GNU GPL v3.0**.  
See [LICENSE](LICENSE) for details.  
