# TextQuestEngine

**Autore**: Luca Bocaletto (bocaletto-luca)  
**Repository**: https://github.com/bocaletto-luca/TextQuestEngine  
**Licenza**: GNU GPL v3.0

Engine Python per creare avventure testuali modulari, estensibili e stand-alone. Questo repository include:

- Il motore core: parser, dispatcher, loader, plugin system  
- Una demo completa: “La Grotta Perduta”  
- Strumenti CLI per creare, gestire, testare e impacchettare la tua avventura  

---

## Indice

- [Caratteristiche](#caratteristiche)  
- [Prerequisiti](#prerequisiti)  
- [Installazione](#installazione)  
- [Uso](#uso)  
  - [Comandi CLI](#comandi-cli)  
  - [Esempio con la demo](#esempio-con-la-demo)  
- [Struttura del progetto](#struttura-del-progetto)  
- [Demo “La Grotta Perduta”](#demo-la-grotta-perduta)  
  - [world.yaml](#worldyaml)  
  - [items.json](#itemsjson)  
  - [Plugin: light_plugin.py](#plugin-light_pluginpy)  
- [Packaging](#packaging)  
- [Contribuire](#contribuire)  
- [Licenza](#licenza)  

---

## Caratteristiche

- Parser multilingue (italiano/inglese) con sinonimi  
- Dispatcher configurabile con plugin (eventi `pre_action`, `command_<cmd>`, `post_action`)  
- Loader per mondi definiti in YAML e JSON (`world.yaml` + `items.json`)  
- Gestione di stanze, oggetti, NPC, missioni e tempo di gioco  
- CLI intuitiva: `init`, `run`, `test`, `lint`, `build`, `package`  
- Stand-alone packaging con PyInstaller  

---

## Prerequisiti

- Python 3.8 o superiore  
- pip  
- (opzionale) PyInstaller per `tqe package`  

---

## Installazione

```bash
git clone https://github.com/bocaletto-luca/TextQuestEngine.git
cd TextQuestEngine
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pip install pyinstaller       # necessario solo per il packaging standalone
```

---

## Uso

### Comandi CLI

Dopo l’installazione, `tqe` (alias `python3 -m engine.utils.cli`) mette a disposizione:

```bash
tqe init <nome_progetto>           # Crea lo scaffolding di una nuova avventura
tqe run --world <path/world.yaml>  # Avvia il gioco in modalità interattiva
tqe test                           # Esegue i test (pytest)
tqe lint                           # Controlla stile e qualità del codice
tqe build                          # Genera sdist & wheel del pacchetto
tqe package                        # Crea un eseguibile standalone (PyInstaller)
```

### Esempio con la demo

La demo “La Grotta Perduta” è inclusa in `demo_adventure/`.  
Per avviarla:

```bash
cd demo_adventure
tqe run
```

Sequenza di prova:

```txt
> guarda
> prendi torcia
> vai dentro
> usa torcia
> guarda
> prendi gemma
> missioni
```

---

## Struttura del progetto

```
TextQuestEngine/
├── engine/                   # Core engine
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
├── demo_adventure/           # Gioco demo “La Grotta Perduta”
│   ├── config/
│   │   ├── world.yaml
│   │   └── items.json
│   ├── plugins/
│   │   └── light_plugin.py
│   └── assets/
│       └── map.txt
├── src/                      # Wrapper per PyInstaller
│   └── main.py
├── setup.py
└── README.md
```

---

## Demo “La Grotta Perduta”

### world.yaml

```yaml
# demo_adventure/config/world.yaml

config:
  start_room: casa
  start_time: 0
  intro_text: >
    Sei un esploratore in cerca di avventure epiche… e di battute epicamente stupide.
    Se riesci a mantenere un sorriso mentre rischi la pelle, sei nel posto giusto!
  initial_missions:
    - missione_gemma
    - missione_birra

rooms:

  casa:
    name: Casa Abbandonata
    desc: >
      Una casetta polverosa piena di mobili arrugginiti. Sul tavolo brilla una torcia.
    connections:
      fuori: foresta
    items:
      - torcia

  foresta:
    name: Bosco Spettinato
    desc: >
      Radici dispettose e sentieri tortuosi. Un passaggio conduce alla grotta buia.
    connections:
      indietro: casa
      dentro: grotta
    items: []

  grotta:
    name: Grotta Buia (e Scherzosa)
    desc: >
      È così buia che neanche le tue idee fanno luce. Forse ti serve una torcia.
    connections:
      fuori: foresta
    items: []

  taverna:
    name: Taverna del Ghiro
    desc: >
      Qui ogni cliente si accompagna ad una pinta… e a un sonoro russare.
    connections:
      fuori: casa
    items:
      - birra

npcs:

  gnomo_fannullone:
    name: Gnomo Fannullone
    location: taverna
    dialogues:
      - text: "Oh, ciao viandante! Se hai una birra, potremmo chiamarla ‘amicizia’."
        options:
          - reply: "Ecco la birra"
            text: "Finalmente! *starnuto*"
            next: fine
          - reply: "No, ho una gemma"
            text: "Bello, ma bevo birra, non gemme."
            next: fine
      - text: "fine"
        options: []

missions:

  missione_gemma:
    title: "La Gemma Luccicante"
    description: >
      Trova la gemma nella grotta buia e riportala al Gnomo Fannullone.
    requirements:
      have_item: ["gemma"]
    steps:
      - "Entra nella grotta"
      - "Accendi la torcia"
      - "Prendi la gemma"
      - "Riporta la gemma al Gnomo"
    rewards:
      xp: 50
      message: "Missione completata: hai illuminato il giorno (e il morale)!"

  missione_birra:
    title: "Porta la Birra"
    description: >
      Il Gnomo Fannullone è assetato. Trova una birra e portagliela.
    requirements:
      have_item: ["birra"]
    steps:
      - "Trova una birra"
      - "Vai alla taverna"
      - "Dai la birra al Gnomo"
    rewards:
      xp: 20
      message: "Il Gnomo ora è felice… e forse leggermente ubriaco!"
```

### items.json

```json
{
  "torcia": {
    "names": ["torcia", "lanterna"],
    "description": "Torcia a batteria: illumina il buio e le tue prospettive.",
    "weight": 1.0,
    "usable_on": ["grotta"]
  },
  "gemma": {
    "names": ["gemma", "pietra preziosa"],
    "description": "Gemma splendente, brilla più delle tue idee improvvisate.",
    "weight": 0.2,
    "usable_on": []
  },
  "birra": {
    "names": ["birra", "pinta", "bottiglia"],
    "description": "Pinta di birra spumeggiante: consolazione liquida.",
    "weight": 0.5,
    "usable_on": ["gnomo_fannullone"]
  }
}
```

### Plugin `light_plugin.py`

```python
# demo_adventure/plugins/light_plugin.py

from engine.plugins.base import PluginBase
from types import SimpleNamespace

class LightPlugin(PluginBase):

    def on_pre_action(self, action: SimpleNamespace, state, world):
        if action.command == "look" and state["current_room"] == "grotta":
            if not state.get("torch_lit", False):
                return "È troppo buio per vedere. Usa la torcia!"
        return None

    def on_command_use(self, action: SimpleNamespace, state, world):
        if action.target == "torcia":
            state["torch_lit"] = True
            grotta = world.rooms["grotta"]
            if "gemma" not in grotta.items:
                grotta.items.append("gemma")
            return "Hai acceso la torcia! Ora vedi la gemma luccicante."
        return None
```

---

## Packaging

Per creare un eseguibile stand-alone:

```bash
pip install pyinstaller
tqe package
```

Il binario verrà generato in `dist/` includendo `config/` e `assets/`. Rinominalo in `tqe` e distribuisci!

---

## Contribuire

1. Forka il repository  
2. Crea un branch `feature/tuo-todo`  
3. Apporta modifiche e testa con `tqe test` / `tqe lint`  
4. Apri una Pull Request  

---

## Licenza

Questo progetto è distribuito sotto GNU GPL v3.0.  
Vedi [LICENSE](LICENSE) per i dettagli.  
