from pathlib import Path
import os
from distutils import dir_util

# from plugins.batfish.includes.helpers import generate_new_dict
from core.models import action
from core import auth, helpers

from plugins.batfish.includes.batfish import Batfish
from plugins.batfish.includes.queries.access_check import AccessCheck
from plugins.batfish.includes.queries.trace_route_check import TraceRouteCheck
from plugins.batfish.includes.queries.reachability_check import ReachabilityCheck

# from plugins.batfish.includes.queries.ip_owners import IpOwnersCheck
# from plugins.batfish.includes.queries.node_properties import NodePropertiesCheck


class _batfishConnect(action._action):
    host = str()
    snapshot_folder = str()

    def doAction(self, data):

        self.batfish_tmp_folder = "/tmp/batfish-configs"

        host = helpers.evalString(self.host, {"data": data["flowData"]})
        """
        * Instanciate a batfish Batfish().init() object using "batfish host" and "snapshot folder" initial as arguments.
    
        Args:
            data: accepts event/flow data
            returns: Results and Return codes
        """
        # Create instance of batfish

        # Folder checks - checks to see if key exists which would have been passed from an upstream git backup flow
        # if it exists it should use that as the source dst folder and also create a copy of it with the correct
        # structure for batfish "../snapshot/configs"
        try:
            self.check_dst_folder(data)
        except KeyError as e:
            print(f"Key doesn't exist: {e}")
            pass

        b_fish = self.get_batfish_object(host)

        if b_fish is not None:
            self.batfish_to_eventdata(data, b_fish)
            return self.get_rc_success()
        else:
            return self.get_rc_fail()

    def get_rc_fail(self):
        return {
            "result": False,
            "rc": 403,
            "msg": "Connection failed - {0}".format("General Protection Fault!"),
        }

    def get_rc_success(self):
        return {"result": True, "rc": 0, "msg": "Initiated Batfish Session"}

    def batfish_to_eventdata(self, data, b_fish):
        data["eventData"]["remote"] = {}
        data["eventData"]["remote"] = {"client": b_fish}

    def get_batfish_object(self, host):
        b_fish = Batfish(host=host, snapshot_folder=self.snapshot_folder)
        return b_fish

    def check_dst_folder(self, data):
        if data["eventData"]["backup_args"]["dst_folder"] is not None:
            orig_folder = data["eventData"]["backup_args"]["dst_folder"]
            # copy snapshot folder to correct location for batfish (basically append snapshot/config and move files)
            self.snapshot_folder = self._copy_snapshot_folder(orig_folder=orig_folder)

    def _copy_snapshot_folder(self, orig_folder: str):

        batfish_tmp_folder = self.batfish_tmp_folder

        # folder processing
        orig_folder = Path(orig_folder)
        # create target folder
        target_folder = os.path.join(batfish_tmp_folder, "snapshot/configs")

        # copy everything to target folder [/tmp/batfish-configs]/snapshot/config
        dir_util.copy_tree(orig_folder, target_folder)

        # return snapshot folder which  would be the parent folder
        # e.g. `/tmp/batfish-configs/snapshot/configs` becomes `/tmp/batfish-configs/snapshot`
        snapshot_folder = Path(target_folder).parent.absolute()

        return str(snapshot_folder)

    def setAttribute(self, attr, value, sessionData=None):
        if attr == "password" and not value.startswith("ENC "):
            self.password = "ENC {0}".format(auth.getENCFromPassword(value))
            return True
        return super(_batfishConnect, self).setAttribute(
            attr, value, sessionData=sessionData
        )


class _batfishAccessCheck(action._action):

    """
    Batfish Access Checker
    ----------------------
    Overview:
    * Create AccessCheck() and pass it the Batfish() client
    * Pass source and destination, ip protocol, ports and list of nodes to check as args to AccessCheck()


    Args:
        * data: event data (flow data)
    Returns:
        * data: event data (flow data)
        * rc: return code
        * result: result
        * accept_results: (dictionary showing which nodes are permitting the access)
        * deny_results: (list of denyresult objects that show nodes which were denied)
        * msg: Message
    """

    # input data

    src_ip = str()
    dst_ip = str()
    applications = list()
    dst_ports = str()
    ip_protocols = list()
    nodes = list()

    def doAction(self, data):

        try:
            b_fish = data["eventData"]["remote"]["client"]
        except KeyError:
            b_fish = None

        if b_fish:

            # create instance of AccessCheck and pass original batfish object as initial arg
            ac = self.get_access_check_instance(b_fish)

            # Make the actual batfish query and received the deny and accept results
            accept_results, deny_results = self.get_results(ac)

            # Create new fields in the data dictionary.  This is to allow for the returned data.
            self.create_accept_results_in_eventdata(data, accept_results)
            self.create_deny_results_in_eventdata(data, deny_results)

            if self.check_acceptresult_success(data):
                # remove batfish connection object
                return self.return_success(data, exitCode=0)
            else:
                return self.return_fail()
        else:
            return self.return_403()

    def return_403(self):
        return {"result": False, "rc": 403, "msg": "No connection found"}

    def check_acceptresult_success(self, data):
        return (len(data["eventData"]["batfish_access_query"]["accept_results"])) > 0

    def return_fail(self):
        return {
            "result": False,
            "rc": 255,
            "msg": "General Protection Fault!",
            "data": "",
            "errors": "",
        }

    def return_success(self, data, exitCode):
        # remove batfish connection object
        data["eventData"]["remote"] = {}

        return {
            "result": True,
            "rc": exitCode,
            "msg": "Query Successful",
            "data": data,
            "errors": "",
        }

    def create_deny_results_in_eventdata(self, data, deny_results):
        data["eventData"]["batfish_access_query"]["deny_results"] = {}
        data["eventData"]["batfish_access_query"]["deny_results"] = deny_results

    def create_accept_results_in_eventdata(self, data, accept_results):
        data["eventData"]["batfish_access_query"] = {}
        data["eventData"]["batfish_access_query"] = {"accept_results": accept_results}

    def get_access_check_instance(self, b_fish):
        # create instance of AccessCheck and pass original batfish object as initial arg
        ac = AccessCheck(b_fish=b_fish)
        return ac

    def get_results(self, ac):
        deny_results, accept_results = ac.get_results(
            src_ip=self.src_ip,
            dst_ip=self.dst_ip,
            applications=self.applications,
            dst_ports=self.dst_ports,
            ip_protocols=self.ip_protocols,
            nodes=self.nodes,
        )
        return accept_results, deny_results

    def setAttribute(self, attr, value, sessionData=None):
        if attr == "password" and not value.startswith("ENC "):
            self.password = "ENC {0}".format(auth.getENCFromPassword(value))
            return True
        return super(_batfishAccessCheck, self).setAttribute(
            attr, value, sessionData=sessionData
        )


class _batfishTraceRouteCheck(action._action):

    """
    * Connect to existing batfish Batfish() object
    * Create TraceRouteCheck() and pass it the Batfish() client

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
            self.get_batfish_object(data)
        except KeyError:
            b_fish = None

        if b_fish:

            rc = self.get_traceroute_check(b_fish)
            results_list = self.get_results(rc)

            self.results_to_eventdata(results_list, data)

            if (len(data["eventData"]["remote"]["traceroute_results"])) > 0:
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

    def results_to_eventdata(self, results_list, data):
        data["eventData"]["remote"]["traceroute_results"] = results_list

    def get_results(self, rc):
        results, results_list = rc.check(
            destination_ip=self.destination_ip,
            start_node=self.start_node,
            start_interface=self.start_interface,
        )
        return results_list

    def get_traceroute_check(self, b_fish):
        rc = TraceRouteCheck(
            b_fish=b_fish,
            start_node=self.start_node,
            start_interface=self.start_interface,
        )

        return rc

    def get_batfish_object(self, data):
        b_fish = data["eventData"]["remote"]["client"]

    def setAttribute(self, attr, value, sessionData=None):
        if attr == "password" and not value.startswith("ENC "):
            self.password = "ENC {0}".format(auth.getENCFromPassword(value))
            return True
        return super(_batfishTraceRouteCheck, self).setAttribute(
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
    src_ips = str()
    # applications = str()
    start_node = str()
    # start_interface = str()
    dst_ips = str()

    def doAction(self, data):

        try:
            b_fish = data["eventData"]["remote"]["client"]

        except BaseException as e:
            b_fish = None
            raise BaseException(f"error {e}")

        if b_fish:

            # create instance of AccessCheck and pass original batfish object as initial arg
            rc = ReachabilityCheck(
                b_fish=b_fish,
            )

            # Make the actual batfish query

            rr = rc.check(
                srcIps=self.src_ips,
                start_node=self.start_node,
                dstIps=self.dst_ips,
            )

            data["eventData"]["remote"]["trace_results"] = rc.trace_result
            data["eventData"]["remote"]["flow_results"] = rr.flow_result.__dict__

            if data["eventData"]["remote"]["rc_results"]:
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
