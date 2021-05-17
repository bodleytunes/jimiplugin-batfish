from core.models import action
from core import auth, helpers

# from plugins.batfish.includes import batfish
from plugins.batfish.includes.batfish import Batfish
from plugins.batfish.includes.access_check import AccessCheck
from plugins.batfish.includes.route_check import RouteCheck
from plugins.batfish.includes.reachability_check import ReachabilityCheck


class _batfishConnect(action._action):
    host = str()
    snapshot_folder = str()

    def doAction(self, data):
        host = helpers.evalString(self.host, {"data": data["flowData"]})
        """
        * Instanciate a batfish Batfish().init() object using "batfish host" and "snapshot folder" initial as arguments.
    
        Args:
            data: accepts event/flow data
            returns: Results and Return codes
        """
        # Create instance of batfish
        b_fish = Batfish()
        b_fish.init_batfish(host=host, snapshot_folder=self.snapshot_folder)

        if b_fish != None:
            data["eventData"]["remote"] = {}
            data["eventData"]["remote"] = {"client": b_fish}
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
        return super(_batfishConnect, self).setAttribute(
            attr, value, sessionData=sessionData
        )


class _batfishAccessCheck(action._action):

    """
    * Connect to existing batfish Batfish() object
    * Create AccessCheck() and pass it the Batfish() client

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
    dst_ports = list()
    ip_protocols = list()
    nodes = list()

    def doAction(self, data):

        try:
            b_fish = data["eventData"]["remote"]["client"]
        except KeyError:
            b_fish = None

        if b_fish:

            # create instance of AccessCheck and pass original batfish object as initial arg
            ac = AccessCheck(b_fish=b_fish)

            # Make the actual batfish query

            (permit_results, deny_results, merged_results,) = ac.get_results(
                src_ip=self.src_ip,
                destination_ip=self.destination_ip,
                applications=self.applications,
                dst_ports=self.dst_ports,
                ip_protocols=self.ip_protocols,
                nodes=self.nodes,
            )

            # data["eventData"]["remote"]["access_results"] = results
            data["eventData"]["remote"]["permit_results"] = permit_results
            data["eventData"]["remote"]["deny_results"] = deny_results

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


class _batfishRouteCheck(action._action):

    """
    * Connect to existing batfish Batfish() object
    * Create RouteCheck() and pass it the Batfish() client

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
    start_node = str()
    start_interface = str()
    destination_ip = str()

    def doAction(self, data):

        try:
            b_fish = data["eventData"]["remote"]["client"]
        except KeyError:
            b_fish = None

        if b_fish:

            # create instance of AccessCheck and pass original batfish object as initial arg
            rc = RouteCheck(
                b_fish=b_fish,
                start_node=self.start_node,
                start_interface=self.start_interface,
            )

            # Make the actual batfish query

            results = rc.check(
                destination_ip=self.destination_ip,
            )

            data["eventData"]["remote"]["rc_results"] = results

            if (len(data["eventData"]["remote"]["rc_results"])) > 0:
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
        return super(_batfishRouteCheck, self).setAttribute(
            attr, value, sessionData=sessionData
        )


class _batfishReachabilityCheck(action._action):

    """
    * Connect to existing batfish Batfish() object
    * Create ReachabilityCheck() and pass it the Batfish() client

    Args:
        * data: event data (flow data)
    Returns:
        * data: event data (flow data)
        * rc: return code
        * result: result
        * msg: Message
    """

    # input data
    # src_ips = str()
    # applications = str()
    start_node = str()
    # start_interface = str()
    dst_ips = str()

    def doAction(self, data):

        try:
            b_fish = data["eventData"]["remote"]["client"]
        except KeyError:
            b_fish = None

        if b_fish:

            # create instance of AccessCheck and pass original batfish object as initial arg
            rc = ReachabilityCheck(
                b_fish=b_fish,
            )

            # Make the actual batfish query

            rr = rc.check(
                start_node=self.start_node,
                dstIps=self.dst_ips,
            )

            data["eventData"]["remote"]["rc_results"] = rr

            if (len(data["eventData"]["remote"]["rc_results"])) > 0:
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
        return super(_batfishReachabilityCheck, self).setAttribute(
            attr, value, sessionData=sessionData
        )
