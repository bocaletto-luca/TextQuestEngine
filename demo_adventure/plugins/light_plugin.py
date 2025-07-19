# demo_adventure/plugins/light_plugin.py

from engine.plugins.base import PluginBase
from types import SimpleNamespace

class LightPlugin(PluginBase):
    """
    Plugin che gestisce il buio nella grotta e l'uso della torcia:
    - blocca la vista finché la torcia non è accesa
    - genera la gemma una volta illuminato
    """

    def on_pre_action(self, action: SimpleNamespace, state, world):
        # Prima di ogni comando, impedisce di vedere in grotta se torch_lit è False
        if action.command == "look" and state["current_room"] == "grotta":
            if not state.get("torch_lit", False):
                return "È troppo buio per vedere. Forse una torcia farebbe al caso tuo!"
        return None

    def on_command_use(self, action: SimpleNamespace, state, world):
        # Intercetta 'use torcia' (o 'usa torcia')
        if action.target == "torcia":
            state["torch_lit"] = True

            # Quando accendi la torcia, se non c'è ancora la gemma, la facciamo comparire
            grotta = world.rooms.get("grotta")
            if grotta and "gemma" not in grotta.items:
                grotta.items.append("gemma")

            return "Hai acceso la torcia! Un bagliore caldo illumina la stanza."
        return None
