from core.models import action
from core import auth, helpers

from plugins.batfish.includes import batfish
from plugins.batfish.includes.access_check import AccessCheck


class _batfish(action._action):

    # Map fields to pluginName.json (creates the flow box in conduct editor)

    src_ip = str()
    dst_ip = str()
    dst_port = str()
    batfish_server = str()
    batfish_network = str()
    device_type = str()
    snapshot_folder = str()

    def doAction(self, data) -> dict:

        # Call helpers to make various pre-checks
        src_ip = helpers.evalString(self.src_ip, {"data": data["flowData"]})
        dst_ip = helpers.evalString(self.dst_ip, {"data": data["flowData"]})
        dst_port = helpers.evalString(self.dst_port, {"data": data["flowData"]})
        batfish_server = helpers.evalString(
            self.batfish_server, {"data": data["flowData"]}
        )
        batfish_network = helpers.evalString(
            self.batfish_network, {"data": data["flowData"]}
        )
        device_type = helpers.evalString(self.device_type, {"data": data["flowData"]})
        snapshot_folder = helpers.evalString(
            self.snapshot_folder, {"data": data["flowData"]}
        )

        # Call Batfish Includes
        b = batfish.batfishOps(
            src_ip,
            dst_ip,
            dst_port,
            batfish_server,
            batfish_network,
            device_type,
            snapshot_folder=snapshot_folder,
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


class _remoteConnectBatfish(action._action):
    host = str()
    snapshot_folder = str()

    def doAction(self, data):
        host = helpers.evalString(self.host, {"data": data["flowData"]})

        # create instance of AccessCheck which will then init BatFishOps
        ac = AccessCheck(
            host=host,
            snapshot_folder=self.snapshot_folder,
        )

        if ac != None:
            data["eventData"]["batfish"] = {"client": ac}
            return {"result": True, "rc": 0, "msg": "Initiated Batfish Session"}
        else:
            return {
                "result": False,
                "rc": 403,
                "msg": "Connection failed - {0}".format(ac.error),
            }

    def setAttribute(self, attr, value, sessionData=None):
        if attr == "password" and not value.startswith("ENC "):
            self.password = "ENC {0}".format(auth.getENCFromPassword(value))
            return True
        return super(_remoteConnectBatfish, self).setAttribute(
            attr, value, sessionData=sessionData
        )


class _batfishAccessCheck(action._action):

    # input data

    src_ip = str()
    destination_ip = str()
    applications = list()
    nodes = list()

    def doAction(self, data):
        try:
            ac = data["eventData"]["batfish"]["client"]
        except KeyError:
            ac = None

        if ac:

            # Make the actual batfish query
            exitCode, errors, results = ac.get_results(
                src_ip=self.src_ip,
                destination_ip=self.destination_ip,
                applications=self.applications,
                nodes=self.nodes,
            )

            data["eventData"]["batfish"]["access_results"] = results

            if exitCode != None:
                return {
                    "result": True,
                    "rc": exitCode,
                    "msg": "Command succesfull",
                    "data": data,
                    "errors": errors,
                }
            else:
                return {
                    "result": False,
                    "rc": 255,
                    "msg": ac.error,
                    "data": "",
                    "errors": "",
                }
        else:
            return {"result": False, "rc": 403, "msg": "No connection found"}
