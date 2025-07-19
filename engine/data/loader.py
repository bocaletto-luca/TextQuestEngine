# engine/data/loader.py

import os
import json
import yaml
from engine.data.models import World, Room, Item, NPC, Mission

def load_world(world_path: str) -> World:
    """
    Carica il mondo da YAML e JSON:
    - config (start_room, start_time, initial_missions, intro_text)
    - items da items.json
    - rooms, NPC e missions da world.yaml
    """
    # 1. Leggi il file YAML
    with open(world_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}

    # 2. Config iniziale: passata al costruttore di World
    config = data.get('config', {}) or {}
    world = World(config)

    # 3. Carica items.json
    base_dir = os.path.dirname(world_path)
    items_file = os.path.join(base_dir, 'items.json')
    if os.path.isfile(items_file):
        with open(items_file, 'r', encoding='utf-8') as f:
            items_data = json.load(f) or {}
        for item_id, item_def in items_data.items():
            world.items[item_id] = Item.from_dict(item_id, item_def)

    # 4. Carica le stanze
    for room_id, room_def in (data.get('rooms') or {}).items():
        world.rooms[room_id] = Room.from_dict(room_id, room_def)

    # 5. Risolvi le connessioni tra stanze
    for room in world.rooms.values():
        room.resolve_connections(world.rooms)

    # 6. Carica NPC (opzionale)
    for npc_id, npc_def in (data.get('npcs') or {}).items():
        world.npcs[npc_id] = NPC.from_dict(npc_id, npc_def)

    # 7. Carica missioni (opzionale)
    for mission_id, mission_def in (data.get('missions') or {}).items():
        world.missions[mission_id] = Mission.from_dict(mission_id, mission_def)

    return world
