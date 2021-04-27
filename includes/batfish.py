import os
from batfish_ops import BatfishOps

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
        BATFISH_SERVER: str,
        BATFISH_NETWORK: str,
    ) -> None:

        self.ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.dst_port = dst_port

        self.batfish_server = BATFISH_SERVER
        self.batfish_network = BATFISH_NETWORK

        # self.device_type = device_type
        self.device_type = "FIREWALL"

        self.dest_dir = str()
        self.snapshots_dir = os.path.join(self.ROOT_DIR, "snapshots")

        self.git_url = "http://10.12.10.4:3000/jon/forti-configs.git"

    def get_configs(self):
        # git checkout config location to ./snapshots/configs
        device_type = self.device_type

        if device_type == "FIREWALL":
            self.get_git_configs()

        elif device_type == "ROUTER":
            # do as above but get router configs
            # TODO: GET ROUTER
            print("get router")

    def get_git_configs(self):

        self.dest_dir = os.path.join(self.ROOT_DIR, "snapshots/configs")

        repo = git.Repo(self.dest_dir)
        try:
            # initially try a clone
            cloned_repo = Repo.clone_from(self.git_url, self.dest_dir)
        except GitCommandError:
            # if that fails, do a git pull
            origin = repo.remotes.origin
            origin.pull()

    def get_data(self):

        answers = self.return_routes()

        return answers

    def return_routes(self) -> dict:

        batfish_routes = {}

        # TODO - batfish queries
        bat_ops = BatfishOps(SNAPSHOT_PATH=self.snapshots_dir)
        answers = bat_ops.question_routing(self.src_ip, self.dst_ip, self.dst_port)

        # return routing results

        return answers

    def validate_net(self, net) -> str:
        # Validate networks/ip's
        # TODO - validate inputs

        return net

    def validate_port(self, port) -> int:
        # Validate ports
        # TODO - validate inputs
        return port


SRC_IP = "10.1.255.100"
# DST_IP = "10.3.255.100"
DST_IP = "8.8.8.8"
DST_PORT = "53"
APPLICATIONS = ["dns", "ssh"]
IP_PROTOCOLS = ["tcp", "udp"]

b = batfish(
    src_ip=SRC_IP,
    dst_ip=DST_IP,
    dst_port=DST_PORT,
    device_type=None,
    BATFISH_NETWORK=None,
    BATFISH_SERVER=None,
)
b.get_configs()
answers = b.get_data()
# print(answers)
