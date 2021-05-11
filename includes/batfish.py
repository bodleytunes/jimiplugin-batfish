import os

from pybatfish.client.commands import (
    bf_generate_dataplane,
    bf_session,
    bf_init_snapshot,
    bf_set_network,
)
from pybatfish.question import bfq
from pybatfish.question.question import load_questions
from pybatfish.datamodel.flow import HeaderConstraints, PathConstraints


class BatFish:
    def __init__(
        self,
        src_ip: str,
        dst_ip: str,
        dst_port: int,
        device_type: str,
        batfish_server: str,
        batfish_network: str,
        snapshot_folder=None,
    ) -> None:

        self.ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.dst_port = dst_port

        self.batfish_server = batfish_server
        self.batfish_network = batfish_network

        # self.device_type = device_type
        self.device_type = "FIREWALL"

        self.dest_dir = str()
        # self.snapshot_folder = os.path.join(self.ROOT_DIR, "snapshots")


class BatfishOps:
    def __init__(
        self, NETWORK_NAME=None, BATFISH_SERVER=None, snapshot_folder=None
    ) -> None:
        self.NETWORK_NAME = "Firewalls"
        self.BATFISH_SERVER = "10.12.12.134"
        self.snapshot_folder = snapshot_folder

        # self.init_batfish()

    def init_batfish(self, BATFISH_SERVER=None, snapshot_folder=None):

        bf_session.host = self.BATFISH_SERVER
        bf_session.coordinatorHost = self.BATFISH_SERVER

        bf_set_network(self.NETWORK_NAME)

        # Initialize Batfish Snapshot
        bf_init_snapshot(snapshot_folder, name=self.NETWORK_NAME, overwrite=True)
        # Generate Dataplane
        bf_generate_dataplane()
        # Load Batfish Questions
        load_questions()

        self.bfq = bfq
        self.hc = HeaderConstraints
        self.pc = PathConstraints

    def question_routing_traceroute(
        self, src_ip, dst_ip, dst_port=None, applications=None
    ):

        # Get a list of all the nodes/devices
        node_list = self.get_all_devices()

        dst_port_list = list([dst_port])

        if dst_port is not None:

            properties = bfq.nodeProperties().answer().frame()
            print(properties)

            traceroutes = []

            ip_owners = bfq.ipOwners().answer().frame()
            print(ip_owners)

            # t = bfq.traceroute(startLocation="fortigate-vm64-kvm", headers=HeaderConstraints(dstIps=dst_ip, dstPorts=dst_port_list)).answer().frame()

            for device in node_list:

                traceroute = (
                    bfq.traceroute(
                        startLocation=device,
                        headers=HeaderConstraints(
                            dstIps=dst_ip, dstPorts=dst_port_list
                        ),
                    )
                    .answer()
                    .frame()
                )
                traceroutes.append(traceroute)

        answer = traceroutes

        return answer

    def question_routing_lm(self, src_ip, dst_ip):

        # Get a list of all the nodes/devices in question
        node_list = self.get_all_devices()

        answers_dict = {}

        longest_match = bfq.lpmRoutes(ip=dst_ip).answer().frame()
        for n in node_list:
            longest_match = bfq.lpmRoutes(ip=dst_ip).answer().frame()

        # Create new dictionary with keys for each of the nodes and zipped values that we are interested in.
        answers_dict = dict(
            zip(node_list, (zip(longest_match.Ip, longest_match.Network)))
        )

        return answers_dict

    def get_all_devices(self) -> list:
        nodes = bfq.nodeProperties().answer().frame()

        node_list = []
        # Get Node Strings
        for node in nodes["Node"].iloc:
            print(node)
            node_list.append(node)

        return node_list
