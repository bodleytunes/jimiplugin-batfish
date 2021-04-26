from core.models import action
from core import auth, helpers

import pandas as pd

from plugins.batfish.includes import batfish_route


class _batfish_route(action._action):

    src_ip = str()
    dst_ip = str()
    dst_port = int()

    def do_action(self, data) -> dict:

        # Call helpers to make various pre-checks
        src_ip = helpers.evalString(self.src_ip, {"data": data["flowData"]})
        dst_ip = helpers.evalString(self.dst_ip, {"data": data["flowData"]})
        dst_port = helpers.evalString(self.dst_port, {"data": data["flowData"]})

        # Call Batfish Function
        batfish_route_checker = batfish_route.batfish_route(src_ip, dst_ip, dst_port)

        route_list = None
        route_list_answer = None

        # Return results
        if len(route_list) > 0:
            return {"result": True, "rc": 0, "data": route_list}
        else:
            return {"result": False, "rc": 404}
