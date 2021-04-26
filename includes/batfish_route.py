import os
from batfish_ops import batfish_ops

# from pybatfish.client.commands import bf_session, bf_init_snapshot, bf_set_network
# from pybatfish.question import bfq
# from pybatfish.question.question import load_questions
# from pybatfish.datamodel.flow import HeaderConstraints
#
from git import Repo
from git import GitCommandError
import git


class batfish_route:
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

    def get_configs(self):
        # git checkout config location to ./snapshots/configs
        device_type = self.device_type

        if device_type == "FIREWALL":

            git_url = "http://10.12.10.4:3000/jon/forti-configs.git"
            self.dest_dir = os.path.join(self.ROOT_DIR, "snapshots/configs")

            repo = git.Repo(self.dest_dir)
            try:
                # initially try a clone
                cloned_repo = Repo.clone_from(git_url, self.dest_dir)
            except GitCommandError:
                # if that fails, do a git pull
                origin = repo.remotes.origin
                origin.pull()

        elif device_type == "ROUTER":
            # do as above but get router configs
            # TODO: GET ROUTER
            print("get router")

    def get_data(self):

        batfish_routes = self.return_routes()

        return batfish_routes

    def return_routes(self) -> dict:

        batfish_routes = {}

        # do batfish
        # TODO - batfish queries
        bat_ops = batfish_ops(SNAPSHOT_PATH=self.snapshots_dir)
        bat_ops.init_batfish()
        answers = bat_ops.question_batfish()

        # return routing results

        return batfish_routes

    def validate_net(self, net) -> str:
        # Validate networks/ip's
        # TODO - validate inputs

        return net

    def validate_port(self, port) -> int:
        # Validate ports
        # TODO - validate inputs
        return port


b = batfish_route(
    src_ip=None,
    dst_ip=None,
    dst_port=None,
    device_type=None,
    BATFISH_NETWORK=None,
    BATFISH_SERVER=None,
)
b.get_configs()
b.get_data()