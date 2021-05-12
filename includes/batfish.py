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


class Batfish:
    def __init__(self, NETWORK_NAME=None, host=None, snapshot_folder=None) -> None:
        self.NETWORK_NAME = "Firewalls"
        self.host = "10.12.12.134"
        self.snapshot_folder = snapshot_folder

    def init_batfish(self, host=None, snapshot_folder=None):

        bf_session.host = self.host
        bf_session.coordinatorHost = self.host

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
