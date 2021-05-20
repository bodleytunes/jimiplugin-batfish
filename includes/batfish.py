from pybatfish.client.commands import (
    bf_generate_dataplane,
    bf_session,
    bf_init_snapshot,
    bf_set_network,
)
from pybatfish.question import bfq
from pybatfish.question.question import load_questions
from pybatfish.datamodel.flow import HeaderConstraints, PathConstraints


class Batfish:
    def __init__(self, NETWORK_NAME=None, host=None, snapshot_folder=None):
        self.NETWORK_NAME = "Firewalls"
        self.host = host
        self.snapshot_folder = snapshot_folder

        self.hc = HeaderConstraints
        self.pc = PathConstraints

        self.bfq = bfq

        self.init_batfish()

    def init_batfish(self):

        bf_session.host = self.host
        bf_session.coordinatorHost = self.host

        bf_set_network(self.NETWORK_NAME)

        # Initialize Batfish Snapshot
        bf_init_snapshot(self.snapshot_folder, name=self.NETWORK_NAME, overwrite=True)
        # Generate Dataplane
        bf_generate_dataplane()
        # Load Batfish Questions
        load_questions()
