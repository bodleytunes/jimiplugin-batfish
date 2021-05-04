from plugins.batfish.includes.batfish import batfish
from pybatfish.client.commands import bf_session, bf_init_snapshot, bf_set_network
from pybatfish.question import bfq
from pybatfish.question.question import load_questions
from pybatfish.datamodel.flow import HeaderConstraints


class BatfishOps(batfish):
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

        # generate dataplane
        #bf_generate_dataplane()

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
        # for n in node_list:
        #    longest_match = bfq.lpmRoutes(ip=dst_ip).answer().frame()

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
            node_list.append(node)

        return node_list
