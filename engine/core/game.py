# engine/core/game.py

import os
import sys
import importlib
from engine.data.loader import load_world
from engine.core.dispatcher import EventDispatcher
from engine.core.parser import Parser
from engine.plugins.base import PluginBase

class Game:
    def __init__(self, world):
        self.world = world
        self.parser = Parser()
        self.dispatcher = EventDispatcher()

        # Stato di gioco
        self.state = {
            "current_room": self.world.start_room_id,
            "inventory": [],
            "missions": {},
            "time": self.world.start_time
        }

        # Attiva missioni iniziali
        for mid in getattr(self.world, "initial_missions", []):
            if mid in self.world.missions:
                self.state["missions"][mid] = "In corso"

        # Carica plugin
        self._load_plugins()

    def _load_plugins(self):
        root = os.getcwd()
        plugins_dir = os.path.join(root, "plugins")
        if not os.path.isdir(plugins_dir):
            return
        sys.path.insert(0, root)
        for f in os.listdir(plugins_dir):
            if f.startswith("__") or not f.endswith(".py"):
                continue
            m = importlib.import_module(f"plugins.{f[:-3]}")
            for attr in dir(m):
                cls = getattr(m, attr)
                if isinstance(cls, type) and issubclass(cls, PluginBase) and cls is not PluginBase:
                    plugin = cls()
                    plugin.register(self.dispatcher)

    def run(self):
        if not self.world:
            raise RuntimeError("Mondo non caricato. Chiama load_world() prima di run().")

        # Intro
        if self.world.intro_text:
            print(self.world.intro_text.strip(), "\n")
        print("Benvenuto in TextQuestEngine!\n")

        while True:
            try:
                line = input("> ")
            except (EOFError, KeyboardInterrupt):
                print("\nArrivederci!")
                break

            action = self.parser.parse(line, self.state, self.world)

            # 1) pre_action: cattura output plugin
            pre = self.dispatcher.emit("pre_action", action, self.state, self.world)
            if pre is not None:
                print(pre)
                continue

            if action.command == "exit":
                print("Grazie per aver giocato. Arrivederci!")
                break

            # 2) dispatch comando (ora plugin command_{cmd} viene chiamato PRIMA)
            output = self.dispatcher.dispatch(action, self.state, self.world)

            # 3) Controlla missioni completate
            for mid, m in self.world.missions.items():
                if self.state["missions"].get(mid) == "In corso":
                    req = m.requirements.get("have_item", [])
                    if all(item in self.state["inventory"] for item in req):
                        self.state["missions"][mid] = "Completata"
                        print(m.rewards.get("message", f"Missione '{m.title}' completata!"))

            # 4) Stampa output del comando
            if output:
                print(output)

            # 5) post_action
            self.dispatcher.emit("post_action", action, self.state, self.world)
