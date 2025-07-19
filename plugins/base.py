# engine/plugins/base.py

class PluginBase:
    """
    Base class per tutti i plugin.
    Il metodo register() viene invocato da Game._load_plugins()
    con il dispatcher, e qui intercettiamo i metodi on_* per
    registrarli sugli eventi e forniamo subscribe() per i plugin.
    """

    def register(self, dispatcher):
        # salvo il dispatcher per subscribe() manuale
        self.dispatcher = dispatcher

        # autogestione: cerco on_pre_action, on_post_action e on_command_xxx
        for attr in dir(self):
            if attr.startswith("on_pre_action"):
                dispatcher.subscribe("pre_action", getattr(self, attr))
            elif attr.startswith("on_post_action"):
                dispatcher.subscribe("post_action", getattr(self, attr))
            elif attr.startswith("on_command_"):
                cmd = attr[len("on_command_"):]
                dispatcher.subscribe(f"command_{cmd}", getattr(self, attr))

    def subscribe(self, event_name: str, callback):
        """
        Metodo helper per plugin: registra callback su event_name.
        Deve essere chiamato *dopo* register().
        """
        if not hasattr(self, "dispatcher"):
            raise RuntimeError("Plugin non registrato: subscribe() può essere usato solo dopo register().")
        self.dispatcher.subscribe(event_name, callback)
