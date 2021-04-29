import os


# from plugins.batfish.includes import BatfishOps

from pybatfish.client.commands import bf_session, bf_init_snapshot, bf_set_network
from pybatfish.question import bfq
from pybatfish.question.question import load_questions
from pybatfish.datamodel.flow import HeaderConstraints

from git import Repo
from git import GitCommandError
import git


class batfish:
    def __init__(
        self,
        src_ip: str,
        dst_ip: str,
        dst_port: int,
        device_type: str,
        batfish_server: str,
        batfish_network: str,
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
        self.snapshots_dir = os.path.join(self.ROOT_DIR, "snapshots")

        self.git_url = "http://10.12.10.4:3000/jon/forti-configs.git"

        ## init
        self.get_configs()

    def get_configs(self):
        # git checkout config location to ./snapshots/configs
        device_type = self.device_type

        if device_type.upper() == "FIREWALL":
            self.get_git_configs()

        elif device_type.upper() == "ROUTER":
            # do as above but get router configs
            # TODO: GET ROUTER
            print("get router")
        elif device_type.upper() == "IPTABLES":
            # do as above but get server iptables configs
            # TODO: GET SERVER
            print("get server")

    def get_git_configs(self):

        self.dest_dir = os.path.join(self.ROOT_DIR, "snapshots/configs")

        repo = git.Repo(self.dest_dir)
        try:
            # initially try a clone
            cloned_repo = Repo.clone_from(self.git_url, self.dest_dir)
        except Exception:
            # if that fails, do a git pull
            origin = repo.remotes.origin
            origin.pull()

    def return_traceroutes(self):

        # batfish queries
        bat_ops = BatfishOps(SNAPSHOT_PATH=self.snapshots_dir)
        answers = bat_ops.question_routing_traceroute(
            self.src_ip, self.dst_ip, self.dst_port
        )

        return answers

    def return_longest_match(self):

        bat_ops = BatfishOps(SNAPSHOT_PATH=self.snapshots_dir)
        answers = bat_ops.question_routing_lm(self.src_ip, self.dst_ip)


        return answers

    def validate_net(self, net) -> str:
        # Validate networks/ip's
        # TODO - validate inputs

        return net

    def validate_port(self, port) -> int:
        # Validate ports
        # TODO - validate inputs
        return port


class BatfishOps:
    def __init__(
        self, NETWORK_NAME=None, BATFISH_SERVER=None, SNAPSHOT_PATH=None
    ) -> None:
        self.NETWORK_NAME = "Firewalls"
        self.BATFISH_SERVER = "10.12.12.134"
        self.SNAPSHOT_PATH = SNAPSHOT_PATH

        self.init_batfish()

    def init_batfish(self):

        bf_session.host = self.BATFISH_SERVER
        bf_session.coordinatorHost = self.BATFISH_SERVER

        bf_set_network(self.NETWORK_NAME)

        # Initialize Batfish Snapshot
        bf_init_snapshot(self.SNAPSHOT_PATH, name=self.NETWORK_NAME, overwrite=True)

        # Load Batfish Questions
        load_questions()

    def question_routing_traceroute(
        self, src_ip, dst_ip, dst_port=None, applications=None
    ):

        # Get a list of all the nodes/devices
        node_list = self.get_all_devices()

        dst_port_list = list([dst_port])

        if applications is not None:
            # todo - enter application as args
            print("hello world")

        elif dst_port is not None:

            # todo - lookup startLocation based on ip address matching to node

            traceroutes = []

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
