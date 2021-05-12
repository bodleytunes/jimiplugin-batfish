from core import plugin, model


class _batfish(plugin._plugin):
    version = 1.3

    def install(self):
        # Register batfish Models

        model.registerModel(
            "remoteConnectBatfish",
            "_remoteConnectBatfish",
            "_action",
            "plugins.batfish.models.action",
        )
        model.registerModel(
            "batfishAccessCheck",
            "_batfishAccessCheck",
            "_action",
            "plugins.batfish.models.action",
        )
        return True

    def uninstall(self):
        # de-register batfish Models

        model.deregisterModel(
            "remoteConnectBatfish",
            "_remoteConnectBatfish",
            "_action",
            "plugins.batfish.models.action",
        )
        model.deregisterModel(
            "batfishAccessCheck",
            "_batfishAccessCheck",
            "_action",
            "plugins.batfish.models.action",
        )
        return True

    def upgrade(self, LatestPluginVersion):

        if self.version < 1.3:
            model.registerModel(
                "batfishAccessCheck",
                "_batfishAccessCheck",
                "_action",
                "plugins.batfish.models.action",
            )
        if self.version < 1.4:
            model.registerModel(
                "remoteConnectBatfish",
                "_remoteConnectBatfish",
                "_action",
                "plugins.batfish.models.action",
            )

        return True
