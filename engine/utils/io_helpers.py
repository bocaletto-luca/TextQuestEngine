#!/usr/bin/env python3
# engine/utils/io_helpers.py

import os
import sys
import json
import yaml
import time
from typing import Any, Optional, List
from colorama import init as colorama_init, Fore, Style

# Inizializza colorama per Windows
colorama_init(autoreset=True)

def clear_screen() -> None:
    """
    Pulisce il terminale.
    """
    os.system("cls" if os.name == "nt" else "clear")

def load_json(path: str) -> Any:
    """
    Carica e restituisce il contenuto di un file JSON.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_yaml(path: str) -> Any:
    """
    Carica e restituisce il contenuto di un file YAML.
    """
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def print_delayed(text: str, delay: float = 0.02, end: Optional[str] = "\n") -> None:
    """
    Stampa il testo con effetto “macchina da scrivere”.
    """
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    if end:
        sys.stdout.write(end)
        sys.stdout.flush()

def prompt_choice(prompt: str, choices: List[str]) -> str:
    """
    Richiede all’utente di scegliere tra le opzioni fornite.
    Ritorna la scelta valida (in minuscolo).
    """
    choice = ""
    options = "/".join(choices)
    while choice.lower() not in choices:
        choice = input(f"{prompt} ({options}): ").strip()
    return choice.lower()

def colored(text: str, color: str = "white") -> str:
    """
    Avvolge il testo con codici colore ANSI (tramite colorama).
    Colori disponibili: red, green, yellow, blue, magenta, cyan, white.
    """
    palette = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE
    }
    code = palette.get(color.lower(), Fore.WHITE)
    return f"{code}{text}{Style.RESET_ALL}"
