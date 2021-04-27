from core.models import action
from core import auth, helpers

from plugins.batfish.includes import batfish


class _batfish(action._action):

    # Map fields to pluginName.json (creates the flow box in conduct editor)

    src_ip = str()
    dst_ip = str()
    dst_port = str()
    BATFISH_SERVER = str()
    BATFISH_NETWORK = str()
    device_type = str()

    def doAction(self, data) -> dict:

        # Call helpers to make various pre-checks
        src_ip = helpers.evalString(self.src_ip, {"data": data["flowData"]})
        dst_ip = helpers.evalString(self.dst_ip, {"data": data["flowData"]})
        dst_port = helpers.evalString(self.dst_port, {"data": data["flowData"]})
        BATFISH_SERVER = helpers.evalString(self.src_ip, {"data": data["flowData"]})
        BATFISH_NETWORK = helpers.evalString(self.dst_ip, {"data": data["flowData"]})
        device_type = helpers.evalString(self.dst_port, {"data": data["flowData"]})

        # Call Batfish Includes
        b = batfish.batfish(
            src_ip, dst_ip, dst_port, BATFISH_SERVER, BATFISH_NETWORK, device_type
        )

        data = b.get_data_traceroutes()
        # data = list([b.get_data_traceroutes(), b.get_data_longest_match])

        # Return results
        if len(data) > 0:
            return {"result": True, "rc": 0, "data": data}
        else:
            return {"result": False, "rc": 404}

    def setAttribute(self, attr, value, sessionData=None):

        return super(_batfish, self).setAttribute(attr, value, sessionData=sessionData)
