# engine/core/parser.py

from types import SimpleNamespace

class Parser:
    """
    Converte la stringa immessa dall'utente in un'azione interna:
    - command: nome canonico del comando (es. "look", "take", "inventory")
    - target: oggetto/parametro (se presente)
    - indirect: oggetto indiretto per comandi tipo 'use' (se presente)
    Gestisce sinonimi in italiano e inglese.
    """

    # mappatura token -> comando canonico
    COMMAND_SYNONYMS = {
        "help": "help", "aiuto": "help",
        "look": "look", "guarda": "look",
        "inventory": "inventory", "inventario": "inventory",
        "move": "move", "vai": "move",
        "take": "take", "prendi": "take",
        "drop": "drop", "lascia": "drop",
        "use": "use", "usa": "use",
        "save": "save", "salva": "save",
        "load": "load", "carica": "load",
        "missions": "missions", "missioni": "missions",
        "stats": "stats", "statistiche": "stats",
        "exit": "exit", "esci": "exit",
    }

    def parse(self, line: str, state=None, world=None) -> SimpleNamespace:
        """
        line: stringa raw digitata dall'utente
        state, world: ignorati, ma accettati per compatibilità
        """
        parts = line.strip().lower().split()
        if not parts:
            return SimpleNamespace(command="help", target=None, indirect=None)

        cmd_token = parts[0]
        command = self.COMMAND_SYNONYMS.get(cmd_token, cmd_token)

        target = None
        indirect = None

        if len(parts) > 1:
            # gestiamo 'usa <oggetto> con <oggetto2>'
            if command == "use" and "con" in parts:
                idx = parts.index("con")
                target = " ".join(parts[1:idx])
                indirect = " ".join(parts[idx+1:])
            else:
                target = " ".join(parts[1:])

        return SimpleNamespace(command=command, target=target, indirect=indirect)
