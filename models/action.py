from core.models import action
from core import auth, helpers

from plugins.batfish.includes import batfish


class _batfish(action._action):

    # Map fields to pluginName.json (creates the flow box in conduct editor)

    src_ip = str()
    dst_ip = str()
    dst_port = str()
    batfish_server = str()
    batfish_network = str()
    device_type = str()
    snapshots_dir = str()

    def doAction(self, data) -> dict:

        # Call helpers to make various pre-checks
        src_ip = helpers.evalString(self.src_ip, {"data": data["flowData"]})
        dst_ip = helpers.evalString(self.dst_ip, {"data": data["flowData"]})
        dst_port = helpers.evalString(self.dst_port, {"data": data["flowData"]})
        batfish_server = helpers.evalString(self.batfish_server, {"data": data["flowData"]})
        batfish_network = helpers.evalString(self.batfish_network, {"data": data["flowData"]})
        device_type = helpers.evalString(self.device_type, {"data": data["flowData"]})
        snapshots_dir = helpers.evalString(self.snapshots_dir, {"data": data["flowData"]})


        # Call Batfish Includes
        b = batfish.batfish(
            src_ip, dst_ip, dst_port, batfish_server, batfish_network, device_type, snapshots_dir=snapshots_dir
        )

        # Get batfish data
        data = list([b.return_traceroutes(), b.return_longest_match()])

        # Return results to Jimi flow
        if len(data) > 0:
            return {"result": True, "rc": 0, "data": data}
        else:
            return {"result": False, "rc": 404}

    def setAttribute(self, attr, value, sessionData=None):

        return super(_batfish, self).setAttribute(attr, value, sessionData=sessionData)
