from pybatfish.client.commands import bf_session, bf_init_snapshot, bf_set_network
from pybatfish.question import bfq
from pybatfish.question.question import load_questions
from pybatfish.datamodel.flow import HeaderConstraints


class batfish_ops:
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

    def question_routing(src_ip, dst_ip, dst_port):

        traceroutes = (
            bfq.traceroute(
                startLocation="fortigate-vm64-kvm__configs__spoke1.cfg",
                headers=HeaderConstraints(dstIps="8.8.8.8", applications=["dns"]),
            )
            .answer()
            .frame()
        )

        return answer
