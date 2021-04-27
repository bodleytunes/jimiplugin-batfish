from core import plugin, model


class _batfish(plugin._plugin):
    version = 1.0

    def install(self):
        # Register batfish Models
        model.registerModel(
            "batfish", "_batfish", "_action", "plugins.batfish.models.action"
        )
        return True

    def uninstall(self):
        # de-register batfish Models
        model.deregisterModel(
            "batfish", "_batfish", "_action", "plugins.batfish.models.action"
        )
        return True