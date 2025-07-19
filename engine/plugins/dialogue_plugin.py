# engine/plugins/dialogue_plugin.py

from engine.plugins.base import PluginBase

class DialoguePlugin(PluginBase):
    """
    Plugin per gestire il comando 'parla' (talk) con gli NPC definiti in world.npcs.
    Tiene traccia dello stato di dialogo in state['variables'].
    """

    def register(self, dispatcher):
        # Si registra sull’evento command_talk generato dal Parser
        dispatcher.subscribe("command_talk", self.handle_talk)

    def handle_talk(self, action, state: dict, world) -> str | None:
        """
        action.target contiene l'id dell’NPC da invocare.
        world.npcs[npc_id].dialogues è una lista di nodi:
          { text: str, options: [{reply: str, next: int}, ...] }
        State conserva l'indice corrente in state['variables']['dialogue_<npc_id>'].
        """
        npc_id = action.target
        if not npc_id or npc_id not in world.npcs:
            return "Non vedo nessuno con cui parlare qui."

        npc = world.npcs[npc_id]
        var_key = f"dialogue_{npc_id}"
        idx = state["variables"].get(var_key, 0)

        # Se abbiamo finito i nodi, lo ringraziamo e usciamo
        if idx >= len(npc.dialogues):
            return f"{npc.name} non ha altro da dire in questo momento."

        node = npc.dialogues[idx]
        text = node.get("text", "")
        options = node.get("options", [])

        # Avanziamo il cursore di dialogo
        state["variables"][var_key] = idx + 1

        # Costruiamo l’output: testo + eventuali opzioni
        out_lines = [f"{npc.name} dice: \"{text}\""]
        if options:
            out_lines.append("Opzioni:")
            for i, opt in enumerate(options, 1):
                out_lines.append(f"  {i}. {opt.get('reply')}")

            out_lines.append(
                "Per rispondere digita: parla " + npc_id + " " + "<numero_opzione>"
            )

            # Se l'utente specifica un numero, possiamo gestirlo qui
            # (facoltativo: estendere parser per catturare indirect come il numero)

        return "\n".join(out_lines)
