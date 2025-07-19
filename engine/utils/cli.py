#!/usr/bin/env python3
"""
TextQuestEngine CLI: punti di ingresso per scaffolding, esecuzione,
test, lint e packaging.
"""

import argparse
import sys
from engine.core.game import Game
from engine.core.cli_commands import init_project, run_game, test_project, build_project, package_project

def main():
    parser = argparse.ArgumentParser(
        prog="tqe",
        description="TextQuestEngine: Crea e gestisci avventure testuali in Python"
    )

    subparsers = parser.add_subparsers(title="Comandi", dest="command")

    # tqe init
    p_init = subparsers.add_parser("init", help="Scaffolding di un nuovo progetto")
    p_init.add_argument("path", type=str, help="Directory di destinazione")

    # tqe run
    p_run = subparsers.add_parser("run", help="Avvia il gioco in modalità interattiva")
    p_run.add_argument("--world", type=str, default="config/world.yaml", help="Percorso al file world")

    # tqe test
    p_test = subparsers.add_parser("test", help="Esegue test di unit e integrazione")
    p_test.add_argument("--focus", choices=["unit", "integration", "all"], default="all")

    # tqe lint
    p_lint = subparsers.add_parser("lint", help="Verifica stile e qualità del codice")

    # tqe build
    p_build = subparsers.add_parser("build", help="Genera la distribuzione (sdist & wheel)")

    # tqe package
    p_package = subparsers.add_parser("package", help="Crea eseguibile standalone")

    args = parser.parse_args()

    if args.command == "init":
        init_project(args.path)
    elif args.command == "run":
        run_game(world_path=args.world)
    elif args.command == "test":
        test_project(scope=args.focus)
    elif args.command == "lint":
        sys.exit(lint_project())
    elif args.command == "build":
        build_project()
    elif args.command == "package":
        package_project()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
