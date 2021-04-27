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

    def get_data_traceroutes(self):
        answers_tr = self.return_traceroutes()
        return answers_tr

    def get_data_longest_match(self):
        answers_lm = self.return_longest_match()
        return answers_lm

    def return_traceroutes(self) -> dict:

        # TODO - batfish queries
        bat_ops = BatfishOps(SNAPSHOT_PATH=self.snapshots_dir)
        answers = bat_ops.question_routing(self.src_ip, self.dst_ip, self.dst_port)

        # return traceroutes results

        return answers

    def return_longest_match(self) -> dict:

        bat_ops = BatfishOps(SNAPSHOT_PATH=self.snapshots_dir)
        answers = bat_ops.question_routing_lm(self.src_ip, self.dst_ip)

        # return longest match results

        return answers

    def validate_net(self, net) -> str:
        # Validate networks/ip's
        # TODO - validate inputs

        return net

    def validate_port(self, port) -> int:
        # Validate ports
        # TODO - validate inputs
        return port
