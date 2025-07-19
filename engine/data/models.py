# engine/data/models.py

from typing import Dict, List, Any


class Room:
    """
    Rappresenta una stanza del mondo.
    """
    def __init__(self, room_id: str, name: str, desc: str,
                 connections: Dict[str, str], items: List[str]):
        self.id = room_id
        self.name = name
        self.desc = desc
        self.connections = connections  # es. {"nord": "altra_stanza"}
        self.items = items[:]  # lista di item_id presenti in stanza

    @classmethod
    def from_dict(cls, room_id: str, data: Dict[str, Any]):
        return cls(
            room_id=room_id,
            name=data.get("name", room_id),
            desc=data.get("desc", ""),
            connections=data.get("connections", {}) or {},
            items=data.get("items", []) or []
        )

    def resolve_connections(self, rooms: Dict[str, "Room"]):
        """
        Validazione / eventuali riferimenti incrociati.
        """
        # (al bisogno si può controllare che ogni target esista in rooms)
        pass

    def describe(self, state: Dict[str, Any], world: "World") -> str:
        """
        Restituisce la descrizione della stanza, oggetti visibili e uscite.
        I plugin possono modificare world o state per far comparire/nascondere cose.
        """
        lines = [f"== {self.name} =="]
        lines.append(self.desc.strip())

        # Oggetti
        if self.items:
            visible = []
            for iid in self.items:
                if iid in world.items:
                    visible.append(world.items[iid].names[0])
            if visible:
                lines.append("\nOggetti visibili: " + ", ".join(visible))

        # Uscite
        if self.connections:
            ex = ", ".join(self.connections.keys())
            lines.append("Uscite: " + ex)

        return "\n".join(lines)


class Item:
    """
    Definizione di un oggetto raccoltabile/usabile.
    """
    def __init__(self, item_id: str, names: List[str], description: str,
                 weight: float, usable_on: List[str]):
        self.id = item_id
        self.names = names
        self.description = description
        self.weight = weight
        self.usable_on = usable_on or []

    @classmethod
    def from_dict(cls, item_id: str, data: Dict[str, Any]):
        return cls(
            item_id=item_id,
            names=data.get("names", []),
            description=data.get("description", ""),
            weight=data.get("weight", 0.0),
            usable_on=data.get("usable_on", []) or []
        )


class NPC:
    """
    NPC con dialoghi a scelta multipla.
    """
    def __init__(self, npc_id: str, name: str, location: str, dialogues: List[Dict]):
        self.id = npc_id
        self.name = name
        self.location = location
        self.dialogues = dialogues

    @classmethod
    def from_dict(cls, npc_id: str, data: Dict[str, Any]):
        return cls(
            npc_id=npc_id,
            name=data.get("name", npc_id),
            location=data.get("location", ""),
            dialogues=data.get("dialogues", []) or []
        )


class Mission:
    """
    Rappresenta una missione con requisiti e ricompense.
    """
    def __init__(self, mission_id: str, title: str, description: str,
                 requirements: Dict[str, List[str]], steps: List[str],
                 rewards: Dict[str, Any]):
        self.id = mission_id
        self.title = title
        self.description = description
        self.requirements = requirements or {}
        self.steps = steps or []
        self.rewards = rewards or {}

    @classmethod
    def from_dict(cls, mission_id: str, data: Dict[str, Any]):
        return cls(
            mission_id=mission_id,
            title=data.get("title", mission_id),
            description=data.get("description", ""),
            requirements=data.get("requirements", {}) or {},
            steps=data.get("steps", []) or [],
            rewards=data.get("rewards", {}) or {}
        )


class World:
    """
    Contiene stanze, oggetti, NPC, missioni e la configurazione di base.
    I valori start_room_id, start_time e initial_missions
    sono letti dal dict config passato al costruttore.
    """

    def __init__(self, config: Dict[str, Any] = None):
        cfg = config or {}
        # Defaults se non presenti
        self._start_room_id: str = cfg.get("start_room", "")
        self._start_time: int = cfg.get("start_time", 0)
        self.initial_missions: List[str] = cfg.get("initial_missions", []) or []

        self.rooms: Dict[str, Room] = {}
        self.items: Dict[str, Item] = {}
        self.npcs: Dict[str, NPC] = {}
        self.missions: Dict[str, Mission] = {}

        # intro_text può servire al Game
        self.intro_text: str = cfg.get("intro_text", "")

    @property
    def start_room_id(self) -> str:
        return self._start_room_id

    @property
    def start_time(self) -> int:
        return self._start_time
