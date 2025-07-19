import os
import json
import yaml
import builtins
import pytest
from pathlib import Path
from engine.core.game import Game

@pytest.fixture
def sample_world(tmp_path):
    """
    Crea una struttura di config minimale:
    - config/world.yaml
    - nessun file esterno (tutto in world.yaml)
    """
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()

    # World YAML con una stanza, un oggetto e nessun NPC o missione
    world_data = {
        "config": {
            "start_room": "start"
        },
        "rooms": {
            "start": {
                "name": "Stanza di Prova",
                "desc": "Sei in una stanza di test.",
                "coords": [0, 0],
                "connections": {},
                "items": ["item1"]
            }
        },
        "items": {
            "item1": {
                "names": ["item1"],
                "desc": "Oggetto di prova.",
                "weight": 0.1,
                "usable_on": []
            }
        },
        "npcs": {},
        "missions": {}
    }
    world_file = cfg_dir / "world.yaml"
    with open(world_file, "w", encoding="utf-8") as f:
        yaml.safe_dump(world_data, f)
    return world_file

def test_game_flow(tmp_path, sample_world, monkeypatch, capsys):
    # Prepara séquence di input: guarda, inventario, prendi item1, inventario, esci
    inputs = ["guarda", "inventario", "prendi item1", "inventario", "esci"]
    monkeypatch.setattr(builtins, "input", lambda prompt="": inputs.pop(0))

    # Crea e carica il gioco
    game = Game()
    game.load_world(str(sample_world))

    # Esegui il loop: si fermerà su 'esci'
    game.run()

    # Cattura l’output su stdout
    out = capsys.readouterr().stdout

    # Verifiche principali
    assert "Stanza di Prova" in out
    assert "Sei in una stanza di test." in out

    # Dopo inventario iniziale
    assert "L'inventario è vuoto." in out

    # Dopo prendi item1
    assert "Hai raccolto item1" in out

    # Successiva inventario con item1
    assert "Inventario:" in out and "item1: Oggetto di prova." in out

    # Alla fine il messaggio di uscita
    assert "Grazie per aver giocato" in out
