# engine/core/dispatcher.py

from types import SimpleNamespace

class EventDispatcher:
    """
    Gestisce la dispatch dei comandi e l’emissione di eventi per i plugin.
    """

    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_name: str, callback):
        """
        Registra un callback su un evento (es. "command_take", "pre_action", ecc.).
        """
        self.subscribers.setdefault(event_name, []).append(callback)

    def emit(self, event_name: str, *args, **kwargs):
        """
        Emette un evento ai callback registrati.
        Restituisce il primo valore non-None ritornato da un callback.
        """
        for callback in self.subscribers.get(event_name, []):
            result = callback(*args, **kwargs)
            if result is not None:
                return result
        return None

    def dispatch(self, action: SimpleNamespace, state: dict, world) -> str:
        """
        Esegue il comando action.command e restituisce l’output testuale.
        Notifica prima i plugin su "command_{cmd}", poi gestisce i comandi core.
        """
        cmd = action.command
        tgt = action.target
        ind = getattr(action, "indirect", None)

        # 1) Plugin hook command_{cmd} prima dei comandi core
        for callback in self.subscribers.get(f"command_{cmd}", []):
            out = callback(action, state, world)
            if out is not None:
                return out

        # 2) Comandi core
        if cmd == "help":
            return self._handle_help()

        if cmd == "look":
            return self._handle_look(tgt, state, world)

        if cmd == "inventory":
            return self._handle_inventory(state, world)

        if cmd == "move":
            return self._handle_move(tgt, state, world)

        if cmd == "take":
            return self._handle_take(tgt, state, world)

        if cmd == "drop":
            return self._handle_drop(tgt, state, world)

        if cmd == "use":
            return self._handle_use(tgt, ind, state, world)

        if cmd == "save":
            return f"Salvataggio in slot '{tgt}' completato."

        if cmd == "load":
            return f"Caricamento da slot '{tgt}' completato."

        if cmd == "missions":
            return self._handle_missions(state, world)

        if cmd == "stats":
            return self._handle_stats(state, world)

        return f"Comando non riconosciuto: '{cmd}'. Digita 'help' per assistenza."

    # --- Handlers interni ------------------------------------------------

    def _handle_help(self) -> str:
        mappings = {
            "help": ["help", "aiuto"],
            "look": ["guarda", "look"],
            "inventory": ["inventario", "inventory"],
            "move": ["vai", "move"],
            "take": ["prendi", "take"],
            "drop": ["lascia", "drop"],
            "use": ["usa", "use"],
            "save": ["salva", "save"],
            "load": ["carica", "load"],
            "missions": ["missioni", "missions"],
            "stats": ["statistiche", "stats"],
            "exit": ["esci", "exit"]
        }
        lines = ["Comandi disponibili:"]
        for core_cmd, syns in mappings.items():
            lines.append(f"- {core_cmd}: {', '.join(syns)}")
        return "\n".join(lines)

    def _handle_look(self, target, state, world) -> str:
        room = world.rooms[state["current_room"]]
        if not target:
            return room.describe(state, world)
        if target in state["inventory"]:
            return world.items[target].description
        if target in room.items:
            return world.items[target].description
        return f"Non vedo '{target}' qui."

    def _handle_inventory(self, state, world) -> str:
        inv = state["inventory"]
        if not inv:
            return "L'inventario è vuoto."
        lines = ["Inventario:"]
        for iid in inv:
            item = world.items[iid]
            lines.append(f"- {item.names[0]}: {item.description}")
        return "\n".join(lines)

    def _handle_move(self, direction, state, world) -> str:
        room = world.rooms[state["current_room"]]
        if not direction or direction not in room.connections:
            return "Non puoi andare lì."
        state["current_room"] = room.connections[direction]
        dest = world.rooms[state["current_room"]]
        return f"Sei arrivato in {dest.name}."

    def _handle_take(self, iid, state, world) -> str:
        if not iid:
            return "Devi specificare un oggetto da prendere."
        room = world.rooms[state["current_room"]]
        if iid not in room.items:
            return f"Non vedo '{iid}' qui."
        room.items.remove(iid)
        state["inventory"].append(iid)
        return f"Hai raccolto {iid}."

    def _handle_drop(self, iid, state, world) -> str:
        if not iid:
            return "Devi specificare un oggetto da lasciare."
        if iid not in state["inventory"]:
            return f"Non hai '{iid}' nell'inventario."
        room = world.rooms[state["current_room"]]
        state["inventory"].remove(iid)
        room.items.append(iid)
        return f"Hai lasciato {iid}."

    def _handle_use(self, iid, ind, state, world) -> str:
        if not iid:
            return "Devi specificare un oggetto da usare."
        if iid not in state["inventory"]:
            return f"Non hai '{iid}' nell'inventario."
        return f"Hai usato {iid}."

    def _handle_missions(self, state, world) -> str:
        if not state["missions"]:
            return "Non ci sono missioni attive."
        lines = ["Missioni attive:"]
        for mid, st in state["missions"].items():
            title = world.missions[mid].title
            lines.append(f"- {title}: {st}")
        return "\n".join(lines)

    def _handle_stats(self, state, world) -> str:
        minutes = state.get("time", 0)
        return f"Tempo di gioco: {minutes//60}h {minutes%60}m"
