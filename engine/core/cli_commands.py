#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
import json
import yaml

from engine.data.loader import load_world
from engine.core.game import Game

def init_project(project_name: str):
    """
    Scaffolding di un nuovo progetto di avventura.
    """
    project_dir = os.path.abspath(project_name)
    if os.path.exists(project_dir):
        print(f"Cartella '{project_name}' già esiste.")
        return

    print(f"Progetto inizializzato in '{project_dir}'.")
    # Crea struttura base
    os.makedirs(os.path.join(project_dir, 'config'), exist_ok=True)
    os.makedirs(os.path.join(project_dir, 'assets'), exist_ok=True)

    # world.yaml di default
    default_world = {
        'config': {
            'start_room': 'start',
            'intro_text': 'Benvenuto nella tua nuova avventura!'
        },
        'rooms': {
            'start': {
                'name': 'Stanza iniziale',
                'desc': 'Sei in una stanza vuota, ma piena di possibilità.',
                'connections': {},
                'items': []
            }
        }
    }
    with open(os.path.join(project_dir, 'config', 'world.yaml'), 'w') as f:
        yaml.dump(default_world, f, sort_keys=False)

    # items.json vuoto di default
    with open(os.path.join(project_dir, 'config', 'items.json'), 'w') as f:
        json.dump({}, f, indent=2)

    print(f"Esegui 'cd {project_name} && python3 -m engine.utils.cli run' per partire col gioco.")

def run_game(world_path: str = 'config/world.yaml'):
    """
    Carica il mondo e avvia la sessione di gioco.
    """
    if not os.path.isfile(world_path):
        world_path = os.path.join(os.getcwd(), world_path)

    if not os.path.isfile(world_path):
        print(f"File di world non trovato: {world_path}")
        return

    world = load_world(world_path)
    game = Game(world)
    game.run()

def test_project():
    """
    Esegue i test di unità e integrazione usando pytest.
    """
    ret = subprocess.call(['pytest', '-q'])
    sys.exit(ret)

def build_project():
    """
    Genera la distribuzione: sdist e wheel.
    """
    ret = subprocess.call([sys.executable, 'setup.py', 'sdist', 'bdist_wheel'])
    sys.exit(ret)

def package_project():
    """
    Crea un eseguibile standalone del progetto usando PyInstaller.
    """
    project_name = os.path.basename(os.getcwd())
    wrapper_path = os.path.join(os.getcwd(), 'src', 'main.py')
    entry_dir = os.getcwd()

    if not os.path.isfile(wrapper_path):
        print(f"Script di avvio non trovato: {wrapper_path}")
        return

    print("Creazione eseguibile con PyInstaller…")
    cmd = [
        "pyinstaller",
        "--clean", "--onefile",
        f"--add-data={entry_dir}/config:config",
        f"--add-data={entry_dir}/assets:assets",
        "-n", project_name,
        wrapper_path
    ]
    ret = subprocess.call(cmd)

    if ret != 0:
        print("Errore nella creazione dell'eseguibile.")
        return

    print(f"Eseguibile creato nella cartella 'dist/{project_name}'")
