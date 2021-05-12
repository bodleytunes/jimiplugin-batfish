from core.models import action
from core import auth, helpers

from plugins.batfish.includes import batfish
from plugins.batfish.includes.access_check import AccessCheck


class _remoteConnectBatfish(action._action):
    host = str()
    snapshot_folder = str()

    def doAction(self, data):
        host = helpers.evalString(self.host, {"data": data["flowData"]})
        """
        Instanciate a batfish AccessCheck() object using "batfish host" and "snapshot folder" as arguments.
    
        Args:
            data: accepts event data

            returns: Results and Return codes
        """

        # create instance of AccessCheck which will then init BatFishOps
        client = AccessCheck(
            host=host,
            snapshot_folder=self.snapshot_folder,
        )

        if client != None:
            data["eventData"]["remote"] = {}
            data["eventData"]["remote"] = {"client": client}
            return {"result": True, "rc": 0, "msg": "Initiated Batfish Session"}
        else:
            return {
                "result": False,
                "rc": 403,
                "msg": "Connection failed - {0}".format("General Protection Fault!"),
            }

    def setAttribute(self, attr, value, sessionData=None):
        if attr == "password" and not value.startswith("ENC "):
            self.password = "ENC {0}".format(auth.getENCFromPassword(value))
            return True
        return super(_remoteConnectBatfish, self).setAttribute(
            attr, value, sessionData=sessionData
        )


class _batfishAccessCheck(action._action):

    """
    * Connect to existing batfish AccessCheck() object
    *

    Args:
        * data: event data (flow data)
    Returns:
        * data: event data (flow data)
        * rc: return code
        * result: result
        * msg: Message
    """

    # input data

    src_ip = str()
    destination_ip = str()
    applications = list()
    nodes = list()

    def doAction(self, data):

        try:
            client = data["eventData"]["remote"]["client"]
        except KeyError:
            client = None

        if client:

            # Make the actual batfish query

            permit_results, deny_results, merged_results = client.get_results(
                src_ip=self.src_ip,
                destination_ip=self.destination_ip,
                applications=self.applications,
                nodes=self.nodes,
            )

            # !todo use __dict__ ?
            # data["eventData"]["remote"]["access_results"] = results
            data["eventData"]["remote"]["permit_results"] = permit_results
            # data["eventData"]["remote"]["deny_results"] = deny_results

            if (len(data["eventData"]["remote"]["permit_results"])) > 0:
                exitCode = 0
            else:
                exitCode = 255

            if exitCode == 0:
                return {
                    "result": True,
                    "rc": exitCode,
                    "msg": "Query Successful",
                    "data": data,
                    "errors": "",
                }
            else:
                return {
                    "result": False,
                    "rc": 255,
                    "msg": "General Protection Fault!",
                    "data": "",
                    "errors": "",
                }
        else:
            return {"result": False, "rc": 403, "msg": "No connection found"}

    def setAttribute(self, attr, value, sessionData=None):
        if attr == "password" and not value.startswith("ENC "):
            self.password = "ENC {0}".format(auth.getENCFromPassword(value))
            return True
        return super(_batfishAccessCheck, self).setAttribute(
            attr, value, sessionData=sessionData
        )
