from core import plugin, model


class _batfish(plugin._plugin):
    version = 1.8

    def install(self):
        # Register batfish Models

        model.registerModel(
            "batfishConnect",
            "_batfishConnect",
            "_action",
            "plugins.batfish.models.action",
        )
        model.registerModel(
            "batfishAccessCheck",
            "_batfishAccessCheck",
            "_action",
            "plugins.batfish.models.action",
        )
        model.registerModel(
            "batfishReachabilityCheck",
            "_batfishReachabilityCheck",
            "_action",
            "plugins.batfish.models.action",
        )
        model.registerModel(
            "batfishRouteCheck",
            "_batfishRouteCheck",
            "_action",
            "plugins.batfish.models.action",
        )
        return True

    def uninstall(self):
        # de-register batfish Models

        model.deregisterModel(
            "batfishConnect",
            "_batfishConnect",
            "_action",
            "plugins.batfish.models.action",
        )
        model.deregisterModel(
            "batfishAccessCheck",
            "_batfishAccessCheck",
            "_action",
            "plugins.batfish.models.action",
        )
        model.deregisterModel(
            "batfishReachabilityCheck",
            "_batfishReachabilityCheck",
            "_action",
            "plugins.batfish.models.action",
        )
        model.deregisterModel(
            "batfishRouteCheck",
            "_batfishRouteCheck",
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
        if self.version < 1.6:
            model.registerModel(
                "batfishConnect",
                "_batfishConnect",
                "_action",
                "plugins.batfish.models.action",
            )
        if self.version < 1.7:
            model.registerModel(
                "batfishReachabilityCheck",
                "_batfishReachabilityCheck",
                "_action",
                "plugins.batfish.models.action",
            )
        if self.version < 1.8:
            model.registerModel(
                "batfishRouteCheck",
                "_batfishRouteCheck",
                "_action",
                "plugins.batfish.models.action",
            )
        return True
